# Install

One installer, three runtimes, and one honest rule: a step that only a human can do is written as a
human step.

```bash
git clone https://github.com/paulmann/agent-prompt-kit.git
cd agent-prompt-kit
python tools/install.py --runtime autoclaw2 --check
python tools/install.py --runtime autoclaw2 --write
```

| Runtime | The command | The model does | The human does |
|---|---|---|---|
| AutoClaw2 | `/agent-prompt-kit` | writes the skill and the command file into the profile | reloads so the resource snapshot is rebuilt |
| HARNESS | `/agent-prompt-kit` | creates the whole workspace directory | one click: add the directory as a workspace |
| SagaAI | — | pastes `PROMPT.md` as the operating contract | as the runtime requires |

`--check` writes nothing and reports the registration state, not just the files. In HARNESS the click
remains open after a successful install; in AutoClaw2 the report stays `NOT READY` until the resource
manifest contains the entry.

Full mechanics, the measured paths and the trap table: `docs/INSTALL.md` in the repository.
