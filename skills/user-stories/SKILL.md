---
name: user-stories
description: "Write, review, split, and refine user stories following Mike Cohn's methodology from User Stories Applied. Covers INVEST criteria, story format, splitting patterns, acceptance criteria, estimation, prioritization, and antipatterns."
triggers:
  - "/user-stories"
  - "write user stories"
  - "review user stories"
  - "split this story"
  - "write acceptance criteria"
  - "story workshop"
  - "help me with user stories"
---

# User Story Skill

Write, review, split, and refine user stories following Mike Cohn's methodology from *User Stories Applied* (Addison-Wesley, 2004).

## Invocation

```
/user-stories write [context]          — draft stories from a description or feature idea
/user-stories review [story or list]   — evaluate stories against INVEST, flag problems
/user-stories split [story]            — break an epic into smaller implementable stories
/user-stories acceptance [story]       — write acceptance criteria for a story
/user-stories workshop [product idea]  — run a full story-gathering exercise
```

---

## Core Concept

A user story is **a placeholder for a conversation**, not a specification. It has three parts:

- **Card** — a short written description of functionality (the artifact)
- **Conversation** — discussion between customer, developers, and users that adds detail
- **Confirmation** — acceptance tests that define when the story is done

The card is the least important element. Stories exist to trigger conversations at the moment they matter, not to document everything upfront.

---

## Story Format

**Standard template:**

```
As a [user role],
I want [action or capability],
so that [benefit or goal].
```

**Examples:**

Good:
```
As a job seeker,
I want to search for open positions by location and salary,
so that I only see jobs I'm willing to consider.
```

Bad (no user value, describes implementation):
```
As a developer,
I want the system to connect to the database through a connection pool,
so that performance is improved.
```

If users wouldn't care about the story, it's not a user story. Technical infrastructure can usually be reframed:
- Instead of: "System uses connection pooling"
- Write: "A user can get search results in under 2 seconds" (the reason connection pooling matters)

**When "so that" can be omitted:** When the benefit is obvious and the team already understands the value. Don't force it if it becomes awkward.

---

## INVEST: Six Qualities of a Good Story

Every story should be checked against these criteria. Use INVEST as a review checklist.

### Independent
Stories should not depend on each other. Dependencies make prioritization and scheduling difficult.

- **Problem:** "A user can pay with Visa" depends on "A user can enter payment info"
- **Fix:** Write each to be independently implementable. The payment entry story shouldn't be a blocker.

When dependencies are unavoidable, surface them explicitly and try to merge or restructure.

### Negotiable
The card is not a contract. Details are negotiable. The written description should be just enough to remember the story — details belong in conversation, not on the card.

If someone is writing paragraph-length requirements on a card, they're over-specifying. Use a physically small card to enforce this discipline.

### Valuable
Every story must deliver value to users or customers. If the customer wouldn't notice or care if the story was skipped, it's not valuable enough to prioritize.

Business value drives prioritization. Cost (estimate) modifies it. A highly desired story may drop in priority when its true cost is visible.

### Estimable
Developers must be able to estimate the story. If they can't, it means the story is:
- Too large (break it down)
- Too vague (clarify through conversation)
- Requires knowledge the team doesn't have yet (write a spike story first)

Vague stories like "Users can use the system efficiently" are not estimable because "efficiently" is undefined.

### Small
Stories should be completable by one developer or pair in half a day to two weeks. Stories that would take longer are **epics** and must be split before they can be planned into an iteration.

The sizing goal:
- Small enough to fit in an iteration
- Large enough to deliver meaningful value
- Not so small that overhead exceeds value

### Testable
Every story needs acceptance tests. A story without a test has no definition of done.

Untestable stories signal problems:
- "A user must never have to wait long" — "never" and "wait long" are both untestable
- Better: "80% of search results appear in under 2 seconds"

---

## Writing Stories: Rules and Heuristics

**Do:**
- Write from the user's perspective, using the user's language
- Keep cards short — write the minimum needed to remember what to build
- Use specific user roles rather than generic "user" where they're meaningfully different
- Write stories for soon-to-build features small and specific
- Write distant features as larger epics — they'll be detailed closer to implementation
- Identify acceptance tests at the same time as writing the story or just before coding

**Don't:**
- Include UI layout or design decisions on the card — UI should emerge through conversation
- Write compound stories that bundle multiple unrelated operations
- Specify implementation details ("the system shall use a B-tree index")
- Front-load detail for features scheduled months out (requirements will change)
- Let the requirements document become the goal instead of the delivered software

**Compound story smell:** "A user can add, edit, and delete resumes" — split into three stories, one per operation.

**UI premature-specification smell:** "A user can search using a form with three dropdown fields and a text input" — the card shouldn't describe the UI. Write "A user can search by location, salary range, and job title" and let the UI emerge.

---

## User Roles and Personas

Before writing stories, identify who will use the system.

**Creating user roles:**
1. Brainstorm all types of users (job seeker, employer, recruiter, admin, guest...)
2. Identify defining attributes for each (experience level, frequency, goals, technical comfort)
3. Group similar types together
4. Narrow to the most important roles for this project
5. For each key role, optionally create a **persona** (a named individual: "Teresa — experienced sailor who orders parts every month")

Personas make stories more concrete. Instead of "a user can search," you think about what Teresa specifically needs. Personas help teams write stories that address real user goals rather than imagined ones.

**Write stories by role.** A search feature might generate different stories for different roles:
- "A first-time job seeker can search without creating an account"
- "A returning job seeker can search using saved criteria"
- "A corporate recruiter can search a resume database by keyword and location"

---

## Story Gathering: Elicitation Techniques

### Story-Writing Workshop (Most Effective)

Bring together: customer, developers, and real users if possible.

1. **Identify user roles** (20-30 minutes on first run)
2. **Assign a persona to each role** — give them names and attributes
3. **For each persona, brainstorm stories** — what does Teresa need to do? What does she want to accomplish?
4. **Use a low-fidelity prototype** (hand-sketched screens, simple navigation diagram) to trigger discussion
5. **Write one story per card** — physically write on index cards, one story per card

This generates 30-80 stories in a half-day session. It also creates shared understanding across the team.

### User Interviews

- Interview real users, not just proxies (managers speaking for users often distort needs)
- Ask **context-free, open-ended questions**: "What kind of performance is required?" not "Is speed important?"
- Context-free questions don't imply an assumed answer
- Open-ended questions generate richer responses than yes/no questions

### Observation

Watch users interact with existing systems or paper prototypes. Useful when users can't articulate their needs. Reveals workflows and pain points not mentioned in interviews.

### Questionnaires

Useful for reaching many users. Effectiveness depends on question quality — same principles as interviews (context-free, open-ended). Follow up on vague answers.

**Key principle:** Don't try to identify every story before starting. Start with enough to plan the first 1-2 iterations. Discover more stories throughout the project. When new stories appear, the customer prioritizes them by removing equivalent work from the plan.

---

## Splitting Stories

Large stories (epics) must be split to fit iterations. Use these patterns:

### 1. Compound Story Split (most common)
The story bundles multiple operations that can be done independently.

```
BEFORE: "A user can add, edit, and delete resumes"
AFTER:
  - "A user can add a resume"
  - "A user can edit a resume"
  - "A user can delete a resume"
```

Split by operation (add/edit/delete/view), by data type (education/work history/publications), or by user role.

### 2. Variation Split
The story covers multiple scenarios or parameter options that each represent meaningful work.

```
BEFORE: "A user can search for jobs by any combination of location, salary, title, and date"
AFTER:
  - "A user can search for jobs by keyword"
  - "A user can filter results by location"
  - "A user can filter results by salary range"
  - "A user can filter results by date posted"
```

### 3. Spike + Implementation Split
Use when the story has high uncertainty — the team can't estimate it because the approach is unknown.

```
BEFORE: "A company can pay for a job posting with a credit card"
  (team has never integrated payment processing)
AFTER:
  - "Spike: Investigate credit card processing options" [TIMEBOX: 3 days]
  - "A company can pay with a credit card" [estimated after spike completes]
```

A spike story always has a **timebox** — a fixed maximum time. Spikes are never estimated in story points because their output is information, not working software.

### 4. Performance Split
Separate the basic functional story from its performance constraint.

```
BEFORE: "A user can search magazine articles quickly"
AFTER:
  - "A user can search magazine articles" [story]
  - Constraint card: "80% of searches return in under 2 seconds" [constraint, not a story]
```

### When to stop splitting

Split to fit iterations, not to capture every detail. If you find yourself splitting to record edge cases or field-level variations, you're splitting too much. Those belong in acceptance tests and conversations, not separate story cards.

"You have to rely on your gut feel." — Cohn

---

## Acceptance Criteria (Acceptance Tests)

Acceptance tests define **done**. They are written by the customer (often with developer help) and capture the assumptions behind the story.

### When to write them
- At story-writing time when you know the scenario
- During a brief meeting at the start of each iteration before coding begins
- During coding when a new edge case surfaces

Writing tests before coding is critical — it forces explicit thinking about edge cases before implementation.

### Format
Write as a list of scenarios and expected outcomes:

```
Story: "A user can purchase a book with a credit card"

Acceptance tests:
✓ Valid Visa — purchase completes
✓ Valid AmEx — rejected (not accepted)
✓ Expired card — rejected with message
✓ Card over limit — rejected with message
✓ Billing address different from shipping address — user can enter both
✓ Billing same as shipping — user can indicate with a checkbox
✓ Missing card number digits — rejected with validation message
```

### Questions to ask when writing tests
- What else do programmers need to know?
- What am I assuming about how this will work?
- What would a bad implementation look like?
- What edge cases am I not thinking of?

### Automation
Aim for 99% automation. Most acceptance tests can and should be automated. Tests that require human observation (e.g., usability tests) are the exception, not the rule. Automate early — code changes frequently in iterative development and automated tests catch regressions immediately.

---

## Non-Functional Requirements (Constraints)

Performance, security, scalability, portability, and similar requirements don't fit the user story format. Write them as **constraint cards**.

**Mark the card "Constraint" and make it measurable:**

```
Constraint: 80% of database searches return results in under 2 seconds
Constraint: The system supports peak concurrent load of 50 users
Constraint: The system runs on Windows, Mac, and Linux
Constraint: The system achieves 99.9% uptime
Constraint: The software predicts game winners with at least 55% accuracy
```

**Not acceptable (untestable):**
```
The system must be fast.
The system will be easy to use.
The system must never lose data.
```

Constraints don't get estimated or scheduled like stories. They do get acceptance tests:
- Constraint: "80% of searches under 2 seconds" → Automate 100 searches, measure, verify 80 pass
- Constraint: "Supports 50 concurrent users" → Run load test with 50 virtual users

Run constraint tests regularly (ideally every build) to catch regressions early.

---

## Estimating Stories

### Story Points
Story points are a relative measure of size/complexity/effort. They are relative to the team, not absolute:
- "This story is twice the size of that 2-point story, so it's 4 points"
- Story points from one team cannot be compared to another team's

Teams choose their own scale. Common: Fibonacci numbers (1, 2, 3, 5, 8, 13, 21) to express increasing uncertainty at larger sizes.

### Planning Poker
Collaborative estimation process:
1. Customer and developers discuss the story (customer clarifies, developers ask questions)
2. Each developer secretly writes their estimate
3. All reveal simultaneously
4. If estimates diverge, each explains their reasoning
5. Discuss until the team understands why estimates differ
6. Re-estimate until convergence

**Customer's role:** Answer questions and clarify scope. Do NOT estimate. Do NOT express shock at estimates — this undermines honesty.

**If an estimate seems way off:** Customer can reframe — "I think I'm asking for something simpler than what you're imagining. All I need is X, not Y."

### Velocity
Velocity = story points completed per iteration. Used for release planning.

Three ways to get initial velocity:
1. Historical data from a similar past project
2. Educated guess
3. Run one iteration and measure

Velocity is team-specific. Don't compare across teams.

---

## Prioritization

The customer owns prioritization. Developers own estimation. Neither does the other's job.

### Must / Should / Could / Won't

Sort stories into four buckets:

| Category | Meaning |
|----------|---------|
| **Must Have** | Required for release — system is unacceptable without these |
| **Should Have** | Important but not critical if the deadline is tight |
| **Could Have** | Nice to have, low impact if deferred |
| **Won't Have (this release)** | Explicitly deferred — important to document |

**Process:**
1. Customer sorts all stories into the four piles
2. Sum estimates for Must-Have stories
3. If total fits in release capacity, add Should-Have stories until full
4. Whatever doesn't fit becomes a future release

**Juicy bits first.** Default to highest-value stories, not risk mitigation. If a risky story might invalidate a significant chunk of work, bring it to the customer's attention — they may choose to prioritize it higher.

**When new stories appear mid-project:** Customer can insert them by removing stories of equivalent size from the remaining plan.

---

## Common Antipatterns

| Problem | Signal | Fix |
|---------|--------|-----|
| Stories too large | Can't fit in an iteration, hard to estimate | Split using compound/variation/spike patterns |
| Stories too small | Dozens of trivial stories, planning overhead exceeds value | Merge related fine-grained stories |
| Compound stories | One story mixes unrelated operations | Split by operation, data type, or user role |
| UI specified too early | Card describes form layout, button placement | Remove UI from card; discuss UI during development |
| Untestable stories | "Users find the system easy to use," "system is fast" | Rewrite with measurable criteria, or make it a testable constraint card |
| Details on the card | Cards run out of room | Use smaller cards; move details to acceptance tests and conversations |
| Stories written too far ahead | Detailed stories for work 3+ months out | Keep distant stories as epics; detail just before iteration planning |
| Customer won't prioritize | Avoids making decisions | Frame as "the team needs your priorities to plan"; make clear the project lead takes final responsibility |
| Interdependent stories | Planning is difficult, everything depends on everything | Restructure stories to be more independent; merge where needed |

---

## Quick Reference: Story Review Checklist

Before accepting a story into planning:

- [ ] Written from the user's perspective (not the system's or developer's)
- [ ] Has a clear user role (not just "user" when roles differ meaningfully)
- [ ] Expresses a specific action and a clear benefit
- [ ] Can be estimated by the developers
- [ ] Small enough to fit in one iteration (or split if not)
- [ ] Does not depend on another unscheduled story
- [ ] Has at least a rough idea of acceptance tests
- [ ] Does not include UI layout details
- [ ] Technical/infrastructure value is connected to user value
- [ ] Nonfunctional requirements are on separate constraint cards, not embedded in the story

---

## Example: Full Story Set for a Job Posting Site

**User roles:** Job Seeker, Employer, Admin

**Selected stories:**

```
[Job Seeker]
As a job seeker, I want to search for open positions by keyword, so that I find relevant jobs.
As a job seeker, I want to filter search results by location, so that I only see jobs I can commute to.
As a job seeker, I want to save a search and receive email alerts, so that I don't have to check manually.
As a returning job seeker, I want to log in and see my saved searches, so that I can pick up where I left off.

[Employer]
As an employer, I want to post a job listing with title, description, and salary range, so that job seekers can find my opening.
As an employer, I want to view a list of applicants for each posting, so that I can manage my pipeline.

[Admin]
As an admin, I want to deactivate expired job listings, so that seekers don't apply to closed positions.

[Constraint]
Constraint: Search results appear in under 2 seconds for 95% of queries.
Constraint: The system supports up to 200 concurrent users.
```

*Skill grounded in: User Stories Applied by Mike Cohn (Addison-Wesley, 2004)*
