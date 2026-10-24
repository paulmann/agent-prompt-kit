# QA checklist

The eleven tests of M8 turned into a review procedure for a human. Use it on an answer the agent
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
| 11 | Did retrieval run, and is every reused record judged? | a solution applied without saying where it came from | a `Reused experience` entry with id, verdict and adaptation |

The answer must end with the gate line. If it is missing, that is finding #10 by itself: the agent
did not run its own gate.

## Reviewing a reused solution

A reused solution is the easiest place for a defect to enter unnoticed, because it arrives
pre-formatted. Three questions, in order:

1. **Was it retrieved before the plan, or afterwards as a justification?** The `Reused experience`
   section appears before the plan, or the reuse is a rationalization.
2. **Is the applicability verdict specific?** "Matches" without naming the environment facts that were
   checked is not a verdict.
3. **Is the adaptation named?** If the record was used unchanged in a different environment, the
   adaptation is the thing that must be justified — or the reuse refused.

## Reviewing a change to the prompt

```bash
python tools/prompt_lint.py          # must exit 0
```

| Check | Why |
|---|---|
| Module identifiers unchanged | they are an interface for reviews and tooling |
| M13 stays whole: store, tool, skill, eleven gate rows | a half-implemented module reads as complete and is not |
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
