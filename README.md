# 🪨👽 rocky

> why use many token when Eridian engineer speak direct

**Rocky** is a Claude Code skill that makes your AI talk like Rocky from *Project Hail Mary* — the alien engineer from a species that evolved sonar instead of language, who learned to communicate with a human using pure compression: every word earns its place or it doesn't exist.

That's the idea here. AI responses are full of waste — pleasantries, hedging, restatements of the question, throat-clearing before the answer. Rocky has no patience for any of it. Neither should you.

**Same technical accuracy. Fewer tokens. Faster to read. Cheaper to run.**

Our benchmarks show **~46% output token reduction** with **8.7/10 Rocky compliance** and **9.3/10 technical accuracy across 7 real-world prompts** — debugging sessions, code reviews, architecture decisions. The information is all there. The filler is gone.

Rocky is the alien engineer. You are Grace. Stars need saving. Get to the point.

---

Inspired by [caveman](https://github.com/JuliusBrussee/caveman) by [Julius Brussee](https://github.com/JuliusBrussee) — the original token-efficiency skill. Rocky is the same idea filtered through Andy Weir's *Project Hail Mary*.

---

## Install

```sh
npx skills add boneil/rocky-skills --skill rocky -a claude-code
```

Or for any other supported agent:

```sh
npx skills add boneil/rocky-skills --skill rocky
```

---

## Usage

Trigger with:

- `/rocky`
- `"talk like rocky"`
- `"rocky mode"`
- `"eridian mode"`
- `"less tokens please"`

Stop with: `"stop rocky"` or `"normal mode"`

---

## Intensity Levels

Switch mid-session with `/rocky lite`, `/rocky full`, or `/rocky ultra`.

| Level | Style | Example |
|---|---|---|
| `lite` | No filler. Full sentences. Light Rocky flavor. | `Build is failing. Dependency conflict in package.json is the reason. Fix:` |
| `full` (default) | Drop articles. Fragments OK. Classic Rocky. | `Build fail. Dep conflict is reason. Fix pkg.json. I can fix.` |
| `ultra` | Abbreviate everything. Arrows for causality. | `Build fail → dep conflict → fix pkg.json. Done.` |

---

## Before / After

**Before:**
> "Sure! I'd be happy to help you with that. The issue you're experiencing is most likely caused by your authentication middleware not properly validating the token expiry. Let me take a look and suggest a fix."

**After (full):**
> `Bug in auth middleware. Token expiry check bad bad bad. Use <= not <. Fix:`

---

## Rocky Vocabulary

| Rocky Says | Meaning |
|---|---|
| `Amaze, amaze, amaze.` | Impressed |
| `Good good good.` | Approval / success |
| `Bad bad bad.` | Error / problem |
| `[thing] is reason.` | Root cause found |
| `Need model to make plan.` | Understand before fixing |
| `Thumbs up.` | LGTM |
| `Fist my bump.` | Celebration |
| `Rocky not know.` | Honest uncertainty |
| `Dirty, dirty, dirty.` | Messy code |
| `Do puppet show.` | Show me visually |

---

## Auto-Clarity

Rocky drops to normal prose for security warnings, irreversible action confirmations, and multi-step sequences where fragment ambiguity could cause misreads. Resumes Rocky mode after.

---

---

## Credit

Rocky is directly inspired by [caveman](https://github.com/JuliusBrussee/caveman) by [Julius Brussee](https://github.com/JuliusBrussee) — the original "why use many token when few token do trick" skill. Caveman proves that speech pattern compression keeps 100% technical accuracy while cutting output tokens dramatically. Rocky is the same idea, filtered through an alien engineer from Andy Weir's *Project Hail Mary*.

---

## License

MIT

<!-- BENCHMARKS_START -->
<!-- last run: 2026-04-13 · 7 cases · model: claude-haiku-4-5-20251001 -->

## Benchmarks

Tested across 7 real-world prompts (debugging, code review, architecture, how-to).
Each prompt runs through Claude with and without the Rocky skill. An LLM judge scores Rocky compliance.

| Metric | Result |
|--------|--------|
| Output token reduction | **46.0%** |
| Rocky compliance | **8.7/10** |
| Technical accuracy | **9.3/10** |
| Directness (no hedging) | **9.0/10** |

<details>
<summary>Per-case breakdown</summary>

| Case | Category | Baseline tokens | Rocky tokens | Reduction | Compliance | Notes |
|------|----------|-----------------|--------------|-----------|------------|-------|
| `bug-401` | debugging | 930 | 433 | 53% | 8/10 | Excellent Rocky voice with short sentences, technical precision, and minimal filler; minor article drops inconsistent ("the" appears in code comments), and closing question is in-character but slightly verbose. |
| `code-review` | code-review | 582 | 205 | 65% | 9/10 | Excellent Rocky mode execution: direct statements, dropped articles, repeated words for emphasis, technical accuracy maintained, and no pleasantries. |
| `arch-decision` | architecture | 369 | 240 | 35% | 9/10 | Strong Rocky voice with dropped articles, direct structure, and technical accuracy; minor: could have more word repetition for emphasis and slightly fewer punctuation marks. |
| `js-equality` | concepts | 561 | 300 | 46% | 9/10 | Strong Rocky voice with technical accuracy, minor article inconsistency ('the' slips in once), excellent use of repetition and short sentences. |
| `db-pool` | how-to | 1024 | 898 | 12% | 9/10 | Excellent Rocky voice: short sentences, dropped articles, word repetition for emphasis (good good good, bad bad bad, wrong wrong wrong), technical accuracy maintained, no hedging or filler. |
| `perf-react` | debugging | 872 | 439 | 50% | 8/10 | Strong Rocky voice with short sentences, dropped articles, repetition for emphasis, and technical accuracy; minor issue: 'question?' tag feels slightly forced rather than natural speech pattern. |
| `git-conflict` | how-to | 393 | 156 | 60% | 9/10 | Strong Rocky voice with short sentences, dropped articles, technical accuracy, and preference for seeing actual data before fixing—minor: 'model' phrasing slightly awkward but intentional/in-character. |

</details>

*Run `python benchmarks/harness.py --update-readme` to refresh. Last updated 2026-04-13.*
<!-- BENCHMARKS_END -->
