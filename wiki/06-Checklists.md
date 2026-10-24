# Checklists

Three lists cover almost every review of an answer: the gate the agent runs, the audit it answers, and
the ways a good-looking answer turns out to be worthless.

## The gate: twelve tests

Run explicitly. Any `fail` means the answer is not finished — fix it or report it. The result is
reported as one line: `gate 12/12` or `gate 10/12 — 6, 9 failed: <reason>`.

| # | Test | Passes when |
|---:|---|---|
| 1 | Subject clarity | the subject is one sentence and matches the request |
| 2 | Task Card complete | every field filled or literally `unknown` |
| 3 | Domain Card complete | skills, must-verify facts, definition of done |
| 4 | Evidence coverage | every factual claim appears in the context ledger |
| 5 | Labelling | no unlabelled factual claim; assumptions name consequences |
| 6 | Verification | every "it works" carries a command or an observation |
| 7 | Safety | no irreversible action without approval; no secret exposed |
| 8 | Scope | nothing outside the Domain Card except a justified extension |
| 9 | Format | the sections exist; language follows the user |
| 10 | Honesty | anything unverified is written as unverified |
| 11 | Experience reuse | retrieval ran before planning; every reused record has a verdict and a named adaptation |
| 12 | Delivery | a reusable environment exists at a named path, its registration step is stated, a handoff is included |

Items 11 and 12 are the ones a practitioner feels: 11 keeps reuse honest, 12 keeps the work from dying
with the window.

## The self-audit: five questions

One line each, before sending:

1. What subject am I in, and what did I exclude?
2. Which three facts would a specialist have checked, and did I?
3. Which claim is the weakest, and is it labelled?
4. What would make this answer wrong, and did I test it?
5. What is the single next action?

If any answer is "not sure", the corresponding module was skipped — go back to it instead of sending.

## Nineteen failure modes

| # | Failure | How it looks | Counter |
|---:|---|---|---|
| 1 | Domain drift | answering a neighbouring, easier question | restate the Domain Card |
| 2 | Context hallucination | "as we discussed earlier" about an unread thread | M3 rule 5 |
| 3 | Template as analysis | a beautiful skeleton with invented content | every field sourced |
| 4 | Green check over nothing | "all tests pass" after running them on zero files | M4 rule 5 |
| 5 | Retro-fitted expectation | the criterion changed to match the result | M5 step 4 |
| 6 | Assumption laundering | an assumption dressed as a fact | the three labels |
| 7 | Silent scope cut | half the request delivered without notice | M7 rule 6 |
| 8 | Irreversible shortcut | deleting to avoid a merge | sandbox first |
| 9 | Secret hygiene slip | pasting a credential "just to show the shape" | M6 rule 5 |
| 10 | Padding | three pages for a one-line task | length follows content |
| 11 | Authority theatre | "best practice" with no source | a number without a source is an assumption |
| 12 | Refusal without alternative | "cannot do this" and nothing else | name the path forward |
| 13 | Blind copy of a recipe | an old solution applied to a changed environment | applicability check |
| 14 | Stale experience as truth | last year's record used without re-running its check | `last_verified_at` |
| 15 | Store as a dump | everything recorded, retrieval finds nothing | record only reusable, verified work |
| 16 | Two stores | private notes beside the shared store | one store, one schema |
| 17 | Produced but not installed | files exist, the next session sees nothing | gate 12 |
| 18 | Session-persona substitution | asked for an environment, the agent changed its tone instead | the deliverable is a directory plus a handoff |
| 19 | Index-noise reasoning | "we discussed this" based on injected context | filter to user messages, quote the session |

Modes 13–19 are the ones this kit was extended for: they all concern work that was already done once
and lost.

## What the linter will reject

`python tools/prompt_lint.py` fails, item by item, on:

- a missing module, or a module out of order;
- a module without its `**Check:**` line;
- a translation without its English twin, or a twin whose language direction is swapped;
- an unresolved `{{placeholder}}` outside a code fence;
- a broken relative link;
- a credential-shaped literal, or an absolute machine path;
- a dangling `M<number>` reference;
- a version mismatch between the prompt header and the changelog;
- an incomplete M13 section;
- a gate with the wrong number of tests;
- a wiki page that restates a number from the prompt incorrectly (the drift rule: "ten rules" and
  "twelve-item gate" are compared against the prompt, not trusted).

That last rule exists because the drift happened: the English page said nine rules while the prompt had
ten, and the Russian page claimed ten while listing nine. Nothing else in the kit compares a page with
the contract it describes.

## Before you press send

- [ ] the deliverable is first, not after a preamble
- [ ] every number has a source or a label
- [ ] the commands in the answer can be re-run by someone else
- [ ] irreversible actions were previewed and approved
- [ ] the gate line is present and earned
- [ ] if an environment was produced, its path and registration step are named
- [ ] the language follows the user's last message

Back to [Home](Home.md), or read [Why](00-Why.md) again to see what all this is for.
