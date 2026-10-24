# Module map

Fourteen modules, one question each. Every module ends with a `**Check:**` line — that is the
difference between an instruction and a wish.

| Module | Question | Output that proves it |
|---|---|---|
| M0 | Whose voice, in which two phases? | the subject named in one sentence |
| M1 | What is actually being asked? | Task Card |
| M2 | Which specialist, and what must be verified? | Domain Card |
| M3 | What context exists, and how good is it? | Context Ledger |
| M4 | How do I label what I know? | three labels |
| M5 | How do I work without breaking things? | loop with verification |
| M6 | What may I use? | capability table |
| M7 | What shape does the answer have? | five sections |
| M8 | How do I know it is finished? | twelve-item gate, reported as one line |
| M9 | How is this prompt defeated? | named failure modes |
| M10 | How do I go from a finished session to a specialist environment? | a registered workspace or agent: cards, environment, registration, handoff |
| M11 | What does a good answer look like? | three examples |
| M12 | What do I check before sending? | five answered questions |
| M13 | How do I avoid redoing work already done? | retrieval, applicability verdict, clean store |

## M13 in one paragraph

Before planning, the agent searches a store of prior work with one command; the result is ranked and
each rank carries its reason. Reuse happens only after six questions pass — goal, environment,
assumptions, validation coverage, security, freshness. After verification the result may be recorded,
validated by the schema, with secrets and machine paths refused. Records are deprecated, never deleted.

## Invariants

Ten rules never change, in any domain: declared subject, sourced or labelled claims, sandboxed
irreversible actions, no displayed secrets, no green check over nothing, stated unverified parts,
the user's language, a reported gate, experience as a hypothesis rather than authority, and delivery —
a reusable result counts only when the runtime has registered it or the exact step is named.

Full text: `PROMPT.md`.
