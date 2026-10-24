---
name: experience-reuse
description: Retrieve prior work before planning and record it after verifying, so a task that was already done costs one search instead of a re-derivation. Ships a searchable store, record schemas, a validating CLI and a staleness policy. Load when a task resembles something already done — or when a completed task is likely to repeat.
license: MIT
version: 1.0.0
tools: [tools/experience.py]
---

# Skill: experience reuse

## Purpose

A task that has already been done should cost one search, not a re-derivation. This skill gives an
agent a store of prior work — what was asked, what worked, what failed — plus the single command that
retrieves it and the rules that keep the store from becoming a second source of truth.

The economics are the reason the skill exists:

| Situation | Without the store | With the store |
|---|---|---|
| The same migration task, three months later | rediscover schema, retry a failed approach, re-verify | `search` returns the recipe and the known failure in one call |
| A failure that took two hours to diagnose | rediscovered by trial | retrieved in seconds, with the working alternative |
| Handing work to another agent | a summary in a chat that is never read again | a record with metadata, applicability and validation |

Retrieval must be cheap or it will not happen. That is why the store is a CLI over plain Markdown
files: one command, ranked candidates, and the reason each one ranked where it did.

## When to activate

- The Task Card resembles earlier work: same technology, same kind of deliverable, same environment.
- A task is known to recur: migrations, release steps, documentation passes, incident diagnostics.
- The user says "we did this before", "as last time", "same as the other repo".
- A failure is being diagnosed that feels familiar.
- After a successful non-trivial task, to decide whether it is worth recording.

## When not to activate

- Trivial requests: retrieval would cost more than the task.
- Tasks whose context is entirely new: no prior work can exist yet.
- Anything where the prior record would outrank current evidence. It never does — see
  *Applicability* below.

## Inputs

| Input | Source | Required |
|---|---|---|
| The current Task Card | `PROMPT.md` M1 | yes |
| A search query in the task's own words | derived from the Task Card | yes |
| The store | `memory/` in the working repository, or a path given by the user | yes, else degrade |
| The current environment facts | files, versions, schema | yes, for the applicability check |

## Outputs

1. **A retrieval line** in the answer: how many candidates, which were used, which were rejected and
   why. "No relevant experience" is a valid, useful output.
2. **An applicability verdict** per reused record: match, adapted, or rejected — with the reason.
3. **A record proposal** after a successful task, when the result is reusable and non-sensitive.

## Workflow

```bash
# 1. store present? one command, no directory walk
python tools/experience.py check

# 2. retrieve before planning — query in the task's words, not in the store's vocabulary
python tools/experience.py search "add nullable column to php list endpoint" --limit 5

# 3. read the best candidate fully, not just the ranking line
python tools/experience.py show php-add-column-to-endpoint

# 4. after a verified task, propose a record and validate it
python tools/experience.py add drafts/my-task.md      # refuses an invalid or leaky record

# 5. deprecate, never delete
python tools/experience.py deprecate old-recipe --by new-recipe
```

Order matters: `search` before `plan`, `add` only after `verify`. A record written before
verification is a guess with a schema.

## Retrieval rules

1. **Query in the task's words.** "Add expiry date to accounts list" beats "database schema
   modification task". The index is lexical and honest about it.
2. **Read the top candidate, do not trust the rank.** The score is a filter, not a verdict.
3. **A failure record changes the plan before a recipe does.** Knowing what did not work is cheaper
   than knowing what did.
4. **Stop at three candidates.** If the third one is not relevant, the store has no answer for this
   task; say so and proceed.
5. **Report the miss.** "No relevant experience" tells the next reader the store needs a record.

## Applicability checklist

A retrieved record may be reused only after all six pass. This is the module-level rule M13 in
`PROMPT.md`, restated as a checklist because it is the step that gets skipped.

| # | Check | Fails when |
|---:|---|---|
| 1 | Goal matches the recorded goal | the record solved a neighbouring problem |
| 2 | Environment matches: versions, runtime, OS, paths | the recipe needs a tool the current environment lacks |
| 3 | Permissions match | the old approach needed admin rights the current task does not have |
| 4 | Its assumptions still hold | the schema, API or contract changed since |
| 5 | Its validation covers the current acceptance condition | it proved "the page renders", you need "the export is byte-identical" |
| 6 | No security or compliance rule now forbids it | the old approach stored a credential in a config file |

Any failure means: adapt and state the adaptation, or reject and say why. Silence is not an option —
an unstated adaptation is indistinguishable from a blind copy.

## Record templates

| Type | File | Use when |
|---|---|---|
| Task record | `templates/task-record.md` | a task produced a reusable outcome; links to the other three |
| Recipe | `templates/recipe.md` | the same approach will very likely apply again |
| Artifact | `templates/artifact.md` | a file, config, script or checklist can be adapted instead of regenerated |
| Failure record | `templates/failure-record.md` | a failure was non-obvious, recurring, or expensive to rediscover |

Sanitised examples: `examples/recipe.md`, `examples/failure-record.md`, `examples/task-record.md`.
They contain placeholders, not real hosts or credentials — the store's own `check` fails on a secret.

## Security and privacy

Non-negotiable, and enforced by the tool where it can be:

1. Never store credentials, tokens, private keys, cookies, session identifiers or password values.
2. Redact hostnames, IP addresses, customer names and personal data to `<HOST>`, `<IP>`, `<CUSTOMER>`,
   `<USER>`, `<PATH>`, `<API_KEY>`.
3. Store the *shape* of a solution, not the content of a customer's database.
4. A public repository receives sanitised examples only.
5. `experience.py add` refuses a record containing a token-shaped literal or an absolute machine path.
   That check is a floor, not a review: a human still reads the record before it is published.

Retention and deprecation: `policies/security-and-privacy.md`.

## Anti-patterns

| Anti-pattern | Why it is worse than no store |
|---|---|
| Blind copy of a recipe | the cheapest way to reproduce an old bug in a new repository |
| Storing the transcript instead of the procedure | unreadable, unsearchable, and it carries private context |
| Recording every task | the store becomes noise, retrieval stops finding anything, the agent stops searching |
| Silent deletion of an outdated record | the audit trail disappears and the same wrong approach returns |
| Marking `validated` without a real revalidation | the status lies, and the next agent trusts it |
| Two stores (one per agent) | two truths, one of them stale, and nobody knows which |

## Definition of done

- Retrieval ran before planning, and its result is stated in the answer, including when it was empty.
- Every reused record has an explicit applicability verdict: match, adapted, or rejected.
- The adaptation is named: what changed and why.
- If a record was created, it passes `experience.py check` with zero errors.
- No secret, hostname or personal datum entered the store.

## Verification

```bash
python tools/experience.py selftest      # 13 checks: retrieval, refusal, staleness, deprecation
python tools/experience.py check         # schema, secrets, duplicates, missing validation
```
