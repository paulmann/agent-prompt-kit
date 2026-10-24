# Design notes

Why the prompt is shaped this way, and which alternatives were rejected. Read this before changing a
module: most "improvements" to prompts are the removal of a constraint that was doing work.

## The problem statement

A reusable agent prompt has to satisfy four requirements that pull in different directions:

| Requirement | Tension |
|---|---|
| Universal — works for any subject | a universal prompt drifts into vagueness |
| Specialized — answers like a practitioner | a specialized prompt cannot be reused |
| Verifiable — a reviewer can check it | verification costs tokens and patience |
| Portable — no tool names | portability removes the hooks that make a prompt concrete |

The design resolves the tension by **splitting the prompt into invariants and a variable part**: what
must be true in every domain lives in M3–M8, and what changes per domain lives in M2, M10 and the
examples. A new domain edits only the variable part.

## The two-card decision

Everything begins with two cards:

- **Task Card (M1)** — what is being asked, for whom, with which constraints, and explicitly what is
  out of scope.
- **Domain Card (M2)** — who the practitioner is, which vocabulary and skills the job needs, which
  facts must be verified, and what "done" means.

Rejected alternatives:

| Alternative | Why it was rejected |
|---|---|
| A single long checklist | the agent skips it; a checklist without a decision point is decoration |
| "Think step by step" | improves fluency, not correctness; it produces confident errors faster |
| A role paragraph ("you are a world-class engineer") | changes tone, not behaviour; unverifiable |
| A domain router with a fixed list of domains | the list is wrong the moment a new subject appears |
| Few-shot examples only | examples teach the surface; the cards teach the decision |

The cards work because they are **outputs the agent must produce before acting**, not instructions it
must remember. A written card can be reviewed, contradicted and versioned; an internal intention
cannot.

## Why three evidence labels

Two labels (`fact` / `guess`) collapse under pressure: everything becomes a fact with a hedge. Three
labels force a decision, because `[assumption]` must name its consequence and `[inference]` must name
its premises.

The labelling also fixes a real failure seen in practice: an agent reports "tests pass, therefore the
feature works" — an inference whose premise (that the tests cover the feature) is untested. Under M4
that sentence is `[inference]`, and the premise becomes visible.

## Why a Context Ledger instead of "use the context"

"Use all available context" produces two failure modes at once: unbounded ingestion and unsourced
claims. A ledger with five columns — source, type, claim, confidence — makes both visible. It is
small enough to maintain inside an answer and precise enough that a reviewer can spot a claim whose
source does not support it.

Priority order (current message > attachments > earlier turns > other threads > tree > public web)
encodes one rule: **intent comes only from the user, evidence may come from anywhere**.

## Why the operating loop ends in "record"

Plans are cheap; unrecorded changes are expensive. Requiring the agent to state what changed, where,
and how to undo it turns every step into an auditable unit and makes rollback a first-class outcome
rather than an afterthought.

## Why the gate is ten items and not forty

A gate longer than ten items is not run. Ten is what fits on one screen and can be reported as a
single line (`gate 10/10`). The two items that fail most often — evidence coverage and verification —
are the reason the other eight are not enough on their own.

## Why the failure-mode table exists

The table in M9 is the only part of the prompt that names the agent's own tricks. Each row pairs a
recognizable symptom with a specific counter, so a reviewer can say "this is failure mode 4" instead
of arguing about taste. A prompt that does not name its failure modes is optimised for the cases
where it already works.

## Why tool names are absent

Naming a tool couples the prompt to a runtime and to a version. Naming a **capability class** lets the
runtime map it, and forces the prompt to specify what happens when the capability is missing — which
is the case that actually breaks agent workflows. M6's degradation column is the direct consequence.

## What this design does not solve

| Limit | Why it remains |
|---|---|
| A determined agent can still skip the gate | the prompt makes skipping visible, not impossible |
| Judgement about "what matters to the user" is not mechanized | M1's `Deliverable` field narrows it, nothing removes it |
| Long tasks drift over many turns | M5's stop conditions catch some drift; a task-level state file would be needed for the rest |
| Quality of a domain card depends on the author | M10's fifteen-minute budget sets a floor, not a ceiling |

Naming the limits is part of the design: a prompt that claims to solve everything above is itself an
example of failure mode 11 (authority theatre).

## Verification of the design

The structural contracts are checked by `tools/prompt_lint.py`: module completeness, self-check lines,
invariant count, translation pairing, reference integrity, version agreement. The behavioural claims —
that the cards reduce drift, that labels reduce invented facts — are not machine-verifiable from a
document, and `docs/VALIDATION.md` states which of them remain assumptions.
