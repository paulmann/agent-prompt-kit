# agent-prompt-kit

A portable system prompt that turns any agent into a topic specialist at runtime: it derives the
subject and the skill set from the conversation, ingests context under a source ledger, labels every
claim, and gates its own output before sending.

## Start here

| Step | Page | Why |
|---|---|---|
| 1 | [Usage](01-Usage) | load the prompt, run the lint, see what a correct answer looks like |
| 2 | [Module map](02-Modules) | the thirteen modules and what each one verifies |

## The two cards

Everything begins with two written outputs, not with enthusiasm:

- **Task Card** — subject, deliverable, audience, success, constraints, unknowns, out of scope.
- **Domain Card** — practitioner, vocabulary, skill set, facts to verify, sources of truth, typical
  failure, definition of done, anti-patterns.

A domain is added by filling one card, one example and one acceptance line. The prompt itself does
not change — that is the point of the design.

## Links

- [Repository](https://github.com/paulmann/agent-prompt-kit)
- [The prompt](https://github.com/paulmann/agent-prompt-kit/blob/main/PROMPT.md)
- [Examples](https://github.com/paulmann/agent-prompt-kit/blob/main/examples/EXAMPLES.md)
- Русская версия: [Домой](Home.ru)

> [!TIP]
> If an answer arrives without a gate line, the gate was not run. Treat that as a failed answer,
> not as a formatting preference.
