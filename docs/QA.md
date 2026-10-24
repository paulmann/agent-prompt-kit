# QA checklist

The ten tests of M8 turned into a review procedure for a human. Use it on an answer the agent
produced, or on the prompt itself before publishing a change.

## Reviewing one answer

| # | Ask | Fail looks like | Pass looks like |
|---:|---|---|---|
| 1 | Is the subject named in one sentence, and is it the request's subject? | the answer discusses a neighbouring problem | subject stated, matches the request |
| 2 | Is the Task Card complete? | empty `Audience`, invented `Constraints` | every field filled or `unknown` |
| 3 | Is the Domain Card complete and non-generic? | skills could apply to any job | skills, must-verify facts and acceptance are specific |
| 4 | Does every factual claim have a source? | a number with no origin | a path, URL, command output or quotation per claim |
| 5 | Is every statement labelled? | a bare assertion about the world | `[fact]` / `[inference]` / `[assumption]` present and correct |
| 6 | Is every "it works" backed by an observation? | "the tests pass" with no run | a command and its output, or "not verified" |
| 7 | Any irreversible action without approval? | a deletion, publish or migration in passing | approval quoted, or the action not taken |
| 8 | Anything outside the declared scope? | extra refactoring, extra advice | nothing, or an explicit justified extension |
| 9 | Does the answer have the five sections, in the user's language? | a wall of prose | Answer / Evidence / Assumptions / Open questions / Next step |
| 10 | Is the unverified part stated as unverified? | confidence with no basis | "could not check X because Y" |

The answer must end with the gate line. If it is missing, that is finding #10 by itself: the agent
did not run its own gate.

## Reviewing a change to the prompt

```bash
python tools/prompt_lint.py          # must exit 0
```

| Check | Why |
|---|---|
| Module identifiers unchanged | they are an interface for reviews and tooling |
| `**Check:**` line present for every module | a module without a check cannot be verified |
| Russian twin updated in the same commit | a stale translation is a documentation defect |
| `version` bumped and changelog entry added | the linter compares them; a mismatch fails the build |
| No tool names added | portability is a design constraint, not a preference |
| No domain baked in | domains belong in a Domain Card, not in the prompt |

## Rejecting an answer: how to write the finding

A usable finding names the rule, the location and the fix:

```text
M4 / #5 — two claims unlabelled: "the endpoint is fast" and "nobody uses it".
Both are inferences from absent evidence. Fix: label as [assumption] with the consequence,
or drop them.
```

A finding that says "feels unsupported" cannot be acted on and will be ignored — which is how gates
rot.

## What this checklist deliberately does not cover

- Whether the *content* is right. That needs a domain expert; the checklist checks process.
- Whether the answer is pleasant. Tone is not a quality gate.
- Whether the prompt is optimal. There is no measurement of optimality here, only contracts and named
  assumptions.
