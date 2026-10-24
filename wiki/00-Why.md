# Why this repository exists

## The expensive run is the second one

A hard task gets done well. The agent reads the schema before writing SQL, finds the one column that
did not exist, runs the command that proves the export is byte-identical, and hands over an answer
with the reasoning still attached. It took hours and a lot of tokens, and it was worth it.

Three weeks later the same class of work arrives — another endpoint, another report, another export.
A fresh window opens. It contains the new request and nothing else. So the work is derived again:
the same schema discovery, the same dead ends, the same "let me check whether the column exists",
the same questions to the user, the same near-miss. Same hours, same tokens, same probability of the
same mistake. The first run produced a good answer; it did not produce anything the second run could
start from.

That is the whole problem, and it is not about model quality. It is about what survives the session.

## Why a chat cannot carry it

Five mechanisms, all of them ordinary:

| What is lost | Why |
|---|---|
| the path | the answer states the conclusion; the steps that produced it stay in the transcript |
| the verification | "it works" survives, the command that proved it does not — so it cannot be re-run |
| the acceptance criterion | it lived in the agent's head, so the next agent invents a different one |
| the vocabulary | the terms that took two rounds to pin down are not written down anywhere |
| the negatives | what was tried and did not work is the cheapest knowledge to reuse, and it is never recorded |

The request itself survives — and it is the least informative artefact of a finished task. Starting
from the request again means starting from the beginning again.

## What the kit does instead

Three artefacts, each with a home on disk:

1. **Two cards** (M1, M2). Subject, deliverable, success, unknowns, out of scope; then practitioner,
   vocabulary, skills, the facts a specialist would never assert from memory, definition of done.
   Twenty minutes of writing that turns "make it better" into a bounded job.
2. **An environment** (M10). A directory: `AGENTS.md` with the rules for this class of work,
   `DOMAIN-CARD.md` with the acceptance criterion inside it, a skill with the procedure, `examples/`,
   and `memory/` for records. Registered in the runtime, so the next window can list it.
3. **A store with one retrieval command** (M13). Prior tasks, recipes, artifacts and recorded failures
   as Markdown records, searched with `python tools/experience.py search "<the task's own words>"`.
   Ranked, with the reason for each rank printed next to the hit.

The design decision behind point 3 is worth stating, because it is the difference between a rule and a
wish. "Consult your experience" costs a model a directory walk and a guess. "Run one command that
returns the three best candidates with their applicability" costs one command. Under pressure only the
second one is followed — so the kit ships the command, not the exhortation.

## What gets cheaper, and what does not

| Round | Cost | Note |
|---|---|---|
| first | **higher than a plain answer** | cards, environment files, one verified record |
| second and later | lower than a fresh derivation | one search, an applicability check, an adaptation |
| reuse without the check | **higher than starting over** | a stale recipe applied to a changed environment costs the rework plus the wrong turn |

So the kit is not free, and it is not automatic. It pays when a class of work repeats; it loses when
it is applied to a one-off, which is exactly why M13 says "do not retrieve for trivial requests".

The expected saving is stated in tool calls, not in prose: retrieval is one command, re-derivation is
dozens. That claim is checkable by anyone, which is the point of the next section.

## How to prove it on your own work

Do not take the argument on faith. Run it as an experiment on a class of work that has already
happened at least twice:

1. **Pick the class**, not the task. "Add a nullable column to a reporting endpoint", not "add
   `paid_at` to `orders`".
2. **Measure the plain round.** Without an environment: number of commands run, number of tool calls,
   number of questions asked of the user, number of drafts rejected, wall-clock minutes.
3. **Build the environment** from that round ([Environment](04-Environment.md)), record one recipe
   ([Experience](05-Experience.md)), register it, then start a fresh window from the handoff prompt.
4. **Measure the same five numbers.** Compare, and write the result into the environment itself.

If the second round is not cheaper, that is a finding rather than a failure: usually the record is too
specific (it describes the instance, not the class), or its applicability line admits cases it should
reject. Fix the record; do not conclude that the approach does not work.

## Where the limits are

- **It does not make the model smarter.** It changes what the model is given and what it must write
  down before the answer is accepted.
- **Experience is a hypothesis, never authority** (invariant 9). Repository, attached material and an
  explicit instruction outrank any record; a stale record loses to current evidence, always.
- **Registration may be a human step.** In AutoClaw2 the skill appears only after a reload; in HARNESS
  the workspace appears after one click. The kit names that step instead of pretending the folder is
  live (gate 12).
- **The store degrades if misused.** Record everything and retrieval finds nothing; record secrets or
  machine paths and the store becomes a liability. Both are refused by `experience.py check`.
- **A gate line is not a proof.** It is a claim by the agent that a human can audit, item by item.

## Signals that you need it

Any two of these, and an environment is cheaper than another round of derivation:

- the same review comment arrives in a second project;
- a column or a signature is looked up again because it was wrong from memory last time;
- "as we discussed earlier" refers to a window nobody can open;
- a checklist is re-derived from scratch, slightly differently, each time;
- a good answer exists and cannot be found.

Next: [Usage](01-Usage.md) to load the prompt, or [Environment](04-Environment.md) if you already have
a finished session worth keeping.
