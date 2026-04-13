#!/usr/bin/env python3
"""
Rocky Skill Benchmark Harness

Measures token efficiency and Rocky compliance by running test prompts
through Claude with and without the Rocky skill, then uses an LLM judge
to evaluate quality.

Usage:
    python benchmarks/harness.py                    # run benchmarks, print summary
    python benchmarks/harness.py --update-readme    # run + write results to README.md
    python benchmarks/harness.py --model claude-sonnet-4-6  # use different model
"""

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import anthropic

ROOT = Path(__file__).parent.parent
SKILL_PATH = ROOT / "skills" / "rocky" / "SKILL.md"
CASES_PATH = Path(__file__).parent / "cases.json"
RESULTS_DIR = Path(__file__).parent / "results"
README_PATH = ROOT / "README.md"

BENCHMARK_START = "<!-- BENCHMARKS_START -->"
BENCHMARK_END = "<!-- BENCHMARKS_END -->"

DEFAULT_MODEL = "claude-haiku-4-5-20251001"
JUDGE_MODEL = "claude-haiku-4-5-20251001"


# ── Data ──────────────────────────────────────────────────────────────────────

@dataclass
class CaseResult:
    case_id: str
    category: str
    baseline_output_tokens: int
    rocky_output_tokens: int
    reduction_pct: float
    directness_score: int   # 1-10: avoids pleasantries / hedging
    vocabulary_score: int   # 1-10: uses Rocky speech patterns
    accuracy_score: int     # 1-10: preserves all technical info
    compliance_score: int   # 1-10: overall Rocky compliance
    judge_notes: str


# ── Skill loading ─────────────────────────────────────────────────────────────

def load_skill_system_prompt() -> str:
    """Load SKILL.md body, stripping YAML frontmatter."""
    text = SKILL_PATH.read_text()
    if text.startswith("---"):
        end = text.index("---", 3)
        return text[end + 3:].strip()
    return text.strip()


# ── API calls ─────────────────────────────────────────────────────────────────

def call(
    client: anthropic.Anthropic,
    prompt: str,
    model: str,
    system: str | None = None,
) -> tuple[str, int, int]:
    """Call Claude. Returns (response_text, input_tokens, output_tokens)."""
    kwargs: dict = {
        "model": model,
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        kwargs["system"] = system

    resp = client.messages.create(**kwargs)
    return resp.content[0].text, resp.usage.input_tokens, resp.usage.output_tokens


JUDGE_SYSTEM = """\
You are evaluating whether an AI response correctly follows "Rocky mode" —
the speech patterns of Rocky, an alien engineer from Project Hail Mary.

Rocky rules (summary):
- Short, direct sentences. No filler.
- No pleasantries ("Sure, happy to help!")
- No hedging ("it might be worth considering")
- Drop articles (a, an, the) in full/ultra mode
- Repeat words for emphasis: "Good good good." "Bad bad bad."
- Technical terms stay exact — Rocky is an engineer, not stupid.
- Code blocks written normally.

Respond with JSON only — no explanation outside the JSON object."""

JUDGE_TEMPLATE = """\
Question:
{prompt}

Baseline response (normal Claude, no persona):
{baseline}

Rocky response (should follow Rocky rules above):
{rocky}

Evaluate the Rocky response. Return this exact JSON shape:
{{
  "directness_score": <1-10>,
  "vocabulary_score": <1-10>,
  "accuracy_score": <1-10>,
  "compliance_score": <1-10>,
  "notes": "<one concise sentence>"
}}"""


def judge(
    client: anthropic.Anthropic,
    prompt: str,
    baseline: str,
    rocky: str,
) -> dict:
    """Use LLM as judge to score Rocky compliance."""
    judge_prompt = JUDGE_TEMPLATE.format(
        prompt=prompt, baseline=baseline, rocky=rocky
    )
    response, _, _ = call(client, judge_prompt, JUDGE_MODEL, system=JUDGE_SYSTEM)

    match = re.search(r"\{.*\}", response, re.DOTALL)
    if not match:
        raise ValueError(f"Judge returned non-JSON:\n{response[:300]}")
    return json.loads(match.group())


# ── Benchmark runner ──────────────────────────────────────────────────────────

def run_benchmarks(model: str) -> list[CaseResult]:
    client = anthropic.Anthropic()
    rocky_system = load_skill_system_prompt()
    cases = json.loads(CASES_PATH.read_text())
    results: list[CaseResult] = []

    for case in cases:
        cid = case["id"]
        prompt = case["prompt"]
        print(f"  [{cid}]  ", end="", flush=True)

        baseline_text, _, baseline_out = call(client, prompt, model)
        rocky_text, _, rocky_out = call(client, prompt, model, system=rocky_system)

        reduction = (baseline_out - rocky_out) / baseline_out * 100 if baseline_out else 0
        print(f"baseline={baseline_out}  rocky={rocky_out}  reduction={reduction:.0f}%  ", end="", flush=True)

        scores = judge(client, prompt, baseline_text, rocky_text)
        print(f"compliance={scores['compliance_score']}/10")

        results.append(CaseResult(
            case_id=cid,
            category=case["category"],
            baseline_output_tokens=baseline_out,
            rocky_output_tokens=rocky_out,
            reduction_pct=round(reduction, 1),
            directness_score=scores["directness_score"],
            vocabulary_score=scores["vocabulary_score"],
            accuracy_score=scores["accuracy_score"],
            compliance_score=scores["compliance_score"],
            judge_notes=scores["notes"],
        ))

    return results


# ── Metrics ───────────────────────────────────────────────────────────────────

def summarize(results: list[CaseResult]) -> dict:
    n = len(results)
    return {
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "model": DEFAULT_MODEL,
        "case_count": n,
        "avg_token_reduction_pct": round(sum(r.reduction_pct for r in results) / n, 1),
        "avg_compliance_score": round(sum(r.compliance_score for r in results) / n, 1),
        "avg_accuracy_score": round(sum(r.accuracy_score for r in results) / n, 1),
        "avg_directness_score": round(sum(r.directness_score for r in results) / n, 1),
        "avg_vocabulary_score": round(sum(r.vocabulary_score for r in results) / n, 1),
        "total_baseline_tokens": sum(r.baseline_output_tokens for r in results),
        "total_rocky_tokens": sum(r.rocky_output_tokens for r in results),
    }


# ── README rendering ──────────────────────────────────────────────────────────

def render_section(summary: dict, results: list[CaseResult]) -> str:
    run_date = summary["run_at"]
    n = summary["case_count"]
    reduction = summary["avg_token_reduction_pct"]
    compliance = summary["avg_compliance_score"]
    accuracy = summary["avg_accuracy_score"]
    directness = summary["avg_directness_score"]

    lines = [
        f"<!-- last run: {run_date} · {n} cases · model: {summary['model']} -->",
        "",
        "## Benchmarks",
        "",
        f"Tested across {n} real-world prompts (debugging, code review, architecture, how-to).",
        "Each prompt runs through Claude with and without the Rocky skill. An LLM judge scores Rocky compliance.",
        "",
        "| Metric | Result |",
        "|--------|--------|",
        f"| Output token reduction | **{reduction}%** |",
        f"| Rocky compliance | **{compliance}/10** |",
        f"| Technical accuracy | **{accuracy}/10** |",
        f"| Directness (no hedging) | **{directness}/10** |",
        "",
        "<details>",
        "<summary>Per-case breakdown</summary>",
        "",
        "| Case | Category | Baseline tokens | Rocky tokens | Reduction | Compliance | Notes |",
        "|------|----------|-----------------|--------------|-----------|------------|-------|",
    ]
    for r in results:
        lines.append(
            f"| `{r.case_id}` | {r.category} "
            f"| {r.baseline_output_tokens} "
            f"| {r.rocky_output_tokens} "
            f"| {r.reduction_pct:.0f}% "
            f"| {r.compliance_score}/10 "
            f"| {r.judge_notes} |"
        )
    lines += [
        "",
        "</details>",
        "",
        f"*Run `python benchmarks/harness.py --update-readme` to refresh. Last updated {run_date}.*",
    ]
    return "\n".join(lines)


def update_readme(section: str):
    readme = README_PATH.read_text()

    if BENCHMARK_START in readme:
        start = readme.index(BENCHMARK_START)
        end = readme.index(BENCHMARK_END) + len(BENCHMARK_END)
        readme = readme[:start].rstrip("\n") + "\n\n" + readme[end:].lstrip("\n")

    readme = readme.rstrip("\n") + "\n\n" + BENCHMARK_START + "\n" + section + "\n" + BENCHMARK_END + "\n"
    README_PATH.write_text(readme)
    print(f"  README updated.")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Rocky skill benchmark harness")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model to use for test runs")
    parser.add_argument("--update-readme", action="store_true", help="Write results into README.md")
    parser.add_argument("--out", help="Override results output path (.json)")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    print(f"Rocky benchmark — model: {args.model}\n")
    results = run_benchmarks(args.model)
    summary = compute_summary = summarize(results)
    summary["model"] = args.model

    print("\n── Summary ──────────────────────────────────────────")
    print(f"  Cases:              {summary['case_count']}")
    print(f"  Token reduction:    {summary['avg_token_reduction_pct']}%")
    print(f"  Rocky compliance:   {summary['avg_compliance_score']}/10")
    print(f"  Technical accuracy: {summary['avg_accuracy_score']}/10")
    print(f"  Directness:         {summary['avg_directness_score']}/10")
    print(f"  Total baseline:     {summary['total_baseline_tokens']} tokens")
    print(f"  Total rocky:        {summary['total_rocky_tokens']} tokens")

    RESULTS_DIR.mkdir(exist_ok=True)
    out_path = Path(args.out) if args.out else RESULTS_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps({"summary": summary, "results": [asdict(r) for r in results]}, indent=2))
    print(f"\n  Saved: {out_path}")

    if args.update_readme:
        section = render_section(summary, results)
        update_readme(section)


if __name__ == "__main__":
    main()
