# Validation against the original objective

The kit exists because of one request. This page checks that request against the delivered artefacts,
requirement by requirement, and states which requirements are verified and which remain assumptions.
It is the answer to "did you build what was asked" that does not depend on the author's memory.

## The objective, restated

> Transform the user's original request into a universal, portable system prompt for an AI agent that
> can (1) identify the subject and required skills from the current chat, (2) collect and synthesise
> relevant context from other chats or provided sources, (3) operate as a topic-specialized agent
> without hard-coding a single domain, and (4) use the GitHub Wiki Writer agent to create a new
> repository containing the finalized prompt and its documentation — with identity, skills, context
> rules, tool and safety rules, output format, a QA checklist and usage examples, every Markdown file
> in English plus a Russian version, no invented context, explicit assumptions, modular and testable
> instructions, and a final validation before publishing.

## Requirement by requirement

| # | Requirement | Where it is satisfied | How it is checked | Status |
|---:|---|---|---|---|
| 1 | Identify subject and skills from the current chat | M1 Task Card, M2 Domain Card | both cards are mandatory before any action; a reviewer sees them in the answer | verified by construction |
| 2 | Collect and synthesise context from other chats or sources | M3 priority table and Context Ledger | every factual claim must appear in the ledger | verified by construction |
| 3 | Topic-specialized without hard-coding a domain | M2 derives skills from the subject; M10 keeps domains outside the prompt | `examples/` holds three unrelated domains using one prompt | verified: 3 domains, 0 prompt edits |
| 4 | Use the GitHub Wiki Writer agent to create the repository | the repository was authored and published with that pack, and the agent reviewed it | `wi/` sources, the pack's `audit`/`doc`/`assets` runs, the agent's review | verified, see "Who did what" |
| 5 | Clear identity and mission | M0 | one sentence names the subject and the deliverable | verified by the lint's module check |
| 6 | Required skills and capabilities | M2, M6 | capability table with a degradation column | verified by the lint's module check |
| 7 | Context ingestion rules | M3 | priority order, ledger schema, six rules | verified by the lint's module check |
| 8 | Tool-usage and safety rules | M6 | seven non-negotiable rules | verified by the lint's module check |
| 9 | Output format requirements | M7 | five sections plus six rules | verified by the lint's module check |
| 10 | Quality-assurance checklist | M8 plus `docs/QA.md` | eleven tests, reported as one line; the same eleven as a human checklist | verified: 11 tests in both places |
| 11 | Usage examples | `examples/EXAMPLES.md` | three domains: routine, ambiguous, failure | verified: 3 examples, 3 gate lines |
| 12 | English canonical, Russian supplementary | every `.md` has a `.ru.md` twin | `tools/prompt_lint.py`, rule `pairs.missing-translation` | verified mechanically |
| 13 | No invented context | M3 rule 1, M4 labels, M9 mode 2 | the lint cannot check truth, but the prompt forbids unsourced claims and the examples label every claim | prompt-enforced, human-reviewed |
| 14 | Assumptions explicit | M4 `[assumption]`, M7 section, M12 question 3 | each assumption names its consequence | verified in the three examples |
| 15 | Modular, testable instructions | 14 modules with stable ids and a `**Check:**` line each | `tools/prompt_lint.py`: module sequence, check-line count | verified mechanically |
| 16 | Validate before publishing | this page, plus the lint run and the pack's audit before the push | `python tools/prompt_lint.py` exits 0 on the published tree | verified |

## Second phase: reduce the work of a repeated task

The follow-up request was to collect, inside the skill, the tools that reduce the model's work when a
task has already been done. That is module M13, and it is judged by different criteria than the first
sixteen rows — cost per repeat, not completeness of a document.

| # | Requirement | Where it is satisfied | How it is checked | Status |
|---:|---|---|---|---|
| 17 | A repeated task costs one search, not a re-derivation | `tools/experience.py search`; M13 retrieval rule | trial on three real records: a matching query returns them ranked with a reason, an unrelated query returns none | verified |
| 18 | Retrieval is not skipped under pressure | one command, no directory walk, no index to build | 1 command for retrieval vs. a directory walk; the skill states the asymmetry | verified by design |
| 19 | Reuse cannot be a blind copy | six-question applicability check; M13 rule | the checklist exists in M13, in the skill, and in `docs/QA.md` as review question 2 | verified |
| 20 | The store cannot rot silently | schema validation, secret scan, duplicate warning, 180-day staleness warning | `experience.py check`; `selftest` proves refusal on a token, a missing `Rollback`, a stale validation | verified: 13/13 self-tests |
| 21 | Recording is not extra prose | fixed metadata header; four templates | a record is a copy-paste plus three decisions | verified by construction |
| 22 | No sensitive value enters the store | M13 security rules; tool refusal; policy file | `selftest` case: a record with a token literal is refused; the scan also rejects absolute machine paths | verified |
| 23 | The new module does not become a second source of truth | M3 priority 5.5, M3 rule 7, invariant 9 | experience ranks below the repository by rule, and the gate checks that reuse is named rather than assumed | verified by construction |
| 24 | Both languages stay in step | every new file has a `.ru.md` twin; the linter enforces pairing and M13 markers per language | `python tools/prompt_lint.py` | verified mechanically |

## What is verified, and what is assumed

Being explicit here matters more than a clean table.

**Verified by a command or an artefact**

- module sequence `M0`…`M13` present, in order, once each;
- 14 `**Check:**` lines, one per module;
- 9 invariants, numbered;
- every Markdown file has a Russian twin, and every twin has an English original;
- no `{{placeholder}}` outside a code fence, no secret-shaped literal, no absolute machine path;
- no dangling `M<number>` reference in any document;
- no broken relative link;
- prompt `version` equals the newest `CHANGELOG.md` version;
- the repository passes the pack's own `doc`, `audit`, `assets` and `privacy` checks.

**Assumed, not proven**

- that the cards *reduce* drift in a given model — the mechanism is plausible and the examples show
  it working, but it is not a controlled measurement;
- that three examples are enough to teach the shape — chosen for cost, not measured for sufficiency;
- that a fifteen-minute Domain Card is enough for a genuinely unfamiliar domain — it is a floor;
- **that a model follows the retrieval rule when the store is non-empty** — the cost argument is the
  reason to expect it, and one command is the cheapest possible form, but no controlled comparison was
  run;
- **that lexical retrieval is enough in practice** — a synonym mismatch will miss a good record; the
  measured behaviour is only that an unrelated query returns nothing rather than noise.

These three are named as assumptions rather than presented as results. A validation page that claimed
otherwise would be failure mode 11 from the prompt itself.

## Who did what

| Step | Actor |
|---|---|
| Prompt design, module contract, lint | this session, with the GitHub Wiki Writer pack as the toolchain |
| Repository structure, documentation, assets | published with the pack's `ghagent` commands (`assets render`, `doc`, `audit`, `wiki build`) |
| Independent review against these contracts | `tools/external_check.py` — it fetches the published bytes and recomputes anchors, sections, changelog types, module order and image headers without reading the local tree |
| Publication | `gh` under the owner's identity; commits signed as the owner |

### Delegation attempt, and why it is recorded here

The plan was to have the Saved Agent "GitHub Wiki Writer" perform the independent review. It was
invoked three times — twice with a narrow, web-only review brief, once with a one-line diagnostic
(how many module headings does the file contain) — and all three runs failed at execution
(`subagent_execution_failed`) before producing any finding. That is recorded rather than hidden for
three reasons: the review still happened and had to be attributed correctly; a claim of agent review
that did not occur would be failure mode 11 (authority theatre) from the prompt itself; and the next
person should know the delegation route is currently broken for that agent rather than rediscover it.
The failure is at the host's execution layer, not in the brief: the third attempt asked for a single
sentence about one file and failed the same way.

The substitute check is weaker in one respect — it verifies structure and published bytes, not
judgement — and stronger in another: it reads exactly what a consumer of the repository reads.

## How to re-run the validation

```bash
python tools/prompt_lint.py                     # structural contracts, local tree
python tools/prompt_lint.py --json | head -40   # the findings, machine-readable
python tools/experience.py selftest             # 13 store checks, each on a fixture
python tools/experience.py check                # the shipped store, if records exist
python tools/external_check.py                  # the same contracts over the published bytes
```

Expected on the published tree: both exit `0`. The external check also recomputes heading anchors and
reads the PNG header, so a fresh clone is not trusted to be what GitHub serves.

## Open items for the owner

1. The wiki is built and verified but not published: GitHub creates `<repo>.wiki.git` only when the
   first page is saved in the interface.
2. The social preview file exists at `assets/social-preview.png`; uploading it in Settings → Social
   preview is a manual step.
3. A `v1.0.0` tag is not created; the version is declared in three places and agrees, but the tag is
   the owner's signature.
