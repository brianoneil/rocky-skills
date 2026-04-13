# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A single publishable skill for the `npx skills` ecosystem. Users install it with:

```sh
npx skills add boneil/rocky-skills --skill rocky -a claude-code
```

## Structure

```
skills/
└── rocky/
    └── SKILL.md    # The skill definition — frontmatter + instructions
```

The `skills` CLI discovers skills by scanning `skills/` for subdirectories containing `SKILL.md`. No build step, no package.json needed.

## Skill Frontmatter Rules

- `name` — slug used by `npx skills add --skill <name>`
- `description` — must be third-person: "This skill should be used when the user says '/rocky'..." Include specific trigger phrases here; this is what determines when the skill auto-loads.
- No other frontmatter fields are required by the skills CLI.

## Benchmark Harness

```
benchmarks/
├── harness.py       # main script
├── cases.json       # 7 test prompts across debugging, code-review, architecture, how-to
├── requirements.txt # anthropic SDK
└── results/         # timestamped JSON output from each run
```

**Setup (first time):**
```sh
python3 -m venv benchmarks/.venv
benchmarks/.venv/bin/pip install -r benchmarks/requirements.txt
```

**Run benchmarks:**
```sh
export ANTHROPIC_API_KEY=...

benchmarks/.venv/bin/python benchmarks/harness.py                  # run + print summary
benchmarks/.venv/bin/python benchmarks/harness.py --update-readme  # run + update README.md
benchmarks/.venv/bin/python benchmarks/harness.py --model claude-sonnet-4-6
```

**How it works:** Each test case runs through Claude twice — once baseline (no system prompt), once with the Rocky skill injected as the system prompt. A third LLM call (haiku as judge) scores the Rocky output on directness, vocabulary, accuracy, and overall compliance (1–10 each). Results are saved as JSON in `benchmarks/results/` and optionally written into the README between `<!-- BENCHMARKS_START -->` / `<!-- BENCHMARKS_END -->` markers.

## Publishing

Push to GitHub. The install command becomes:

```sh
npx skills add <github-owner>/rocky-skills --skill rocky -a claude-code
```

No npm publish needed.
