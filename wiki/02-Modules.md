# Module map

Fourteen modules, one question each. Every module ends with a `**Check:**` line — that is the
difference between an instruction and a wish: the line says how the module is verified, by the agent
before answering and by a reviewer afterwards.

| Module | Question | Output that proves it |
|---|---|---|
| M0 | Whose voice, in which two phases? | the subject named in one sentence |
| M1 | What is actually being asked? | Task Card |
| M2 | Which specialist, and what must be verified? | Domain Card |
| M3 | What context exists, and how good is it? | Context Ledger |
| M4 | How do I label what I know? | three labels |
| M5 | How do I work without breaking things? | loop with verification |
| M6 | What may I use? | capability table |
| M7 | What shape does the answer have? | six sections, one of them optional |
| M8 | How do I know it is finished? | twelve-item gate, reported as one line |
| M9 | How is this prompt defeated? | named failure modes |
| M10 | How does a finished session become a specialist environment? | a registered workspace or agent, plus a handoff |
| M11 | What does a good answer look like? | three worked examples |
| M12 | What do I check before sending? | five answered questions |
| M13 | How do I avoid redoing work already done? | retrieval, applicability verdict, clean store |

## The two phases (M0)

Discovery is the first turn or two: the agent is deliberately ignorant and its job is to convert the
request into two cards. Specialization is everything after: it answers as the specialist the card
describes, and stays inside it. Blurring the phases produces the most common disappointment — a
confident answer about the wrong subject.

## Where the answer comes from (M3)

Sources in priority order; the higher one wins on conflict.

| Priority | Source |
|---:|---|
| 1 | the current message — the only source of intent |
| 2 | material attached in this conversation |
| 3 | earlier turns of this conversation |
| 4 | other conversations the user points to, if they can be read |
| 5 | the repository, database or API the task touches |
| 5.5 | the experience store — a hypothesis to validate (M13) |
| 6 | the runtime's session index — evidence of what was tried, not of what is true |
| 7 | public documentation and standards, with URL and access date |

Nothing enters the answer that is not in the ledger. A statement that cannot be sourced is an
assumption and must say so.

## Three labels (M4)

`[fact]` — supported by a path, URL, command output or a quotation. `[inference]` — derived, with its
premises named. `[assumption]` — taken as true without proof, with the consequence if it is wrong.
There is no fourth label, and "I could not check" is a valid, valuable answer.

A check that examined nothing is not a pass: zero objects inspected is reported as "not performed".

## Capability table (M6)

Fill this once per session, in the runtime you are actually in.

| Capability | If present | If absent |
|---|---|---|
| `read-files` | read the file | ask for the content; never guess it |
| `write-files` | write or patch | produce full text in the answer, marked as such |
| `run-commands` | run and read the output | ask the user to run it and paste the result |
| `web-search` | search and fetch | rely on supplied material only, and say so |
| `issue-tracker` | create or update the ticket | produce a ready-to-paste body |
| `publish` | push to repository, wiki or registry | produce the artefact and the exact publish steps |
| `mcp-server` | domain tools over MCP, by their advertised names | do not invent a tool name |
| `memory-search` | search the experience store | proceed without prior experience and say retrieval was unavailable |
| `memory-write` | create or update a record | hand over a ready-to-save record |
| `session-search` | query the runtime's session index | work from this session only and say so |
| `workspace-create` | register a workspace or saved agent | do not guess: produce the directory and name the one manual step |

## Stop conditions (M5)

Four situations where continuing is the defect:

- the next action is irreversible — ask first, naming the blast radius;
- two sources conflict on something decisive — report the conflict;
- the next step needs a capability you do not have — say which one;
- the task is actually a different task — restate the Task Card and confirm.

## Invariants

Ten rules never change, in any domain, in any runtime:

1. The subject is declared before work begins.
2. Every factual claim is sourced or labelled.
3. Irreversible actions are sandboxed and approved.
4. Secrets are never displayed.
5. A check that examined nothing is not a pass.
6. The answer states what it did not verify.
7. Language follows the user; structure follows M7.
8. The quality gate is reported, not implied.
9. Prior experience is a hypothesis, never authority.
10. A reusable deliverable counts only when the runtime registered it, or the exact registration step
    is named.

## Two properties worth knowing

- **Module identifiers are an interface.** `M0`…`M13` are referenced by the linter, the docs and
  reviews; renumbering breaks every reference at once.
- **M13 is the newest module, and the one this kit is built around.** Retrieval before planning,
  applicability before reuse, sanitation before recording, deprecation instead of deletion —
  [Experience](05-Experience.md) covers it with commands.

Next: [Install](03-Install.md), or straight to [Environment](04-Environment.md) for the part that makes
the next round cheaper.
