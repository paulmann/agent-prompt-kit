# agent-prompt-kit

A portable system prompt that makes an agent a specialist in the subject in front of it — and, when
the same class of work repeats, leaves behind a working environment the next session starts from
instead of from zero.

Fourteen modules, ten invariants, a twelve-item gate reported as one line. No tool names inside: each
capability is resolved by the runtime (M6), so the same text runs in AutoClaw2, HARNESS, SagaAI or any
agent that can read files and run commands.

## The problem it exists for

Good work done once is usually paid for twice. The next window does not know what was tried, which
column names were real, which command proved the result — so an analogous task costs the same time,
tokens and mistakes as the first one.

The answer here is not "remember harder". It is an artefact: a directory with rules, a domain card, an
acceptance criterion, worked examples and a store of prior work, registered in the runtime so that the
next session can actually see it. Mechanism and limits: [Why](00-Why.md).

## Start here

| # | Page | What you get |
|---:|---|---|
| 1 | [Why](00-Why.md) | why a second run costs as much as the first, and what makes it cheaper |
| 2 | [Usage](01-Usage.md) | load the prompt, run the checks, recognise a finished answer |
| 3 | [Module map](02-Modules.md) | the fourteen modules, the invariants, the capability table |
| 4 | [Install](03-Install.md) | AutoClaw2, HARNESS, SagaAI: what the model does, what a human must do |
| 5 | [Environment](04-Environment.md) | turn a finished session into a registered workspace |
| 6 | [Experience](05-Experience.md) | the store, one retrieval command, and what it refuses |
| 7 | [Checklists](06-Checklists.md) | the gate, the nineteen failure modes, the traps |

## Two outputs

| Output | When | Where it lives |
|---|---|---|
| an answer | every task | this conversation |
| a specialist environment | the work is done and will repeat | a directory the runtime registers, named by path |

## Verify it in two commands

```bash
git clone https://github.com/paulmann/agent-prompt-kit.git
cd agent-prompt-kit
python tools/prompt_lint.py          # PASS: 0 error(s), 0 warning(s)
python tools/experience.py selftest  # 13/13 experience checks passed
```

Both exit `0` on a fresh clone: the first checks the document, the second checks that the store
refuses what it claims to refuse. What the linter rejects item by item is in
[QA.md](https://github.com/paulmann/agent-prompt-kit/blob/main/docs/QA.md).

## What it is not

- **Not a memory product.** The store holds written Markdown records you decided to write, not
  embeddings of your conversations.
- **Not a domain prompt.** A domain never enters the prompt body; it lives in a Domain Card (M2) and
  in the environment (M10). The prompt body does not change when you add a specialty.
- **Not a guarantee.** The gate is run by the agent and read by a human. A gate line nobody ran is the
  first failure mode the kit names (M9).
- **Not installed until the runtime knows about it.** Files on disk are not an environment (M10
  step 4).

## Links

- [Repository](https://github.com/paulmann/agent-prompt-kit)
- [The prompt](https://github.com/paulmann/agent-prompt-kit/blob/main/PROMPT.md)
- [Three worked examples](https://github.com/paulmann/agent-prompt-kit/blob/main/examples/EXAMPLES.md)
- [Changelog](https://github.com/paulmann/agent-prompt-kit/blob/main/CHANGELOG.md)
- Русская версия: [Домой](Home.ru.md)

> [!TIP]
> An answer without a gate line was not gated. Treat it as an unfinished answer, not as a formatting
> preference — and say which module was skipped (M8) instead of re-asking the whole task.
