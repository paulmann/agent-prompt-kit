# Install

One installer, three runtimes, and one honest rule: a step only a human can perform is written as a
human step, not as "the agent did it".

```bash
git clone https://github.com/paulmann/agent-prompt-kit.git
cd agent-prompt-kit
python tools/install.py --runtime autoclaw2 --check    # writes nothing, reports the state
python tools/install.py --runtime autoclaw2 --write    # installs the skill and the command
```

No dependencies beyond the Python standard library.

## What the two calls do

| Call | Effect |
|---|---|
| `--check` | inspects the skill directory, the command file and the runtime's resource manifest; prints the revision, the counts of skills and prompts, the resolved paths, and a verdict |
| `--write` | copies the skill and writes the prompt file, backing up anything it replaces |
| `--runtime harness` | creates the workspace directory for HARNESS instead of the AutoClaw2 profile |
| `--runtime sagai` | **refuses**: the registration path is not measured, and the installer does not guess |

A verdict of `READY` means the files exist **and** the manifest contains them. That second half is the
one that matters: a file that is not in a resource revision is invisible to the model.

## Per runtime

| Runtime | The command | The model does | The human does |
|---|---|---|---|
| AutoClaw2 | `/agent-prompt-kit` | writes the skill directory and the command file into the profile | reloads, so the resource snapshot is rebuilt |
| HARNESS | `/agent-prompt-kit` | creates the whole workspace directory with its files | one click: add the directory as a workspace |
| SagaAI | — | pastes the body of `PROMPT.md` as the operating contract | whatever that runtime requires |

Two measured details, both easy to get wrong:

- **The resource snapshot is fixed at session start.** After `--write`, the command appears in the
  palette only in a new session (or after a reload). In the session where you installed it, it is not
  there — that is not a failed install.
- **The click in HARNESS stays open after a successful install.** The installer can create the
  directory; only the application can register it. The same applies to a saved agent: an agent that
  exists as files and is not registered is not an environment (M10 step 4, gate 12).

## Verify after installing

```bash
python tools/install.py --runtime autoclaw2 --check    # expect READY (autoclaw2)
```

Then, in a **new** session:

1. the command `/agent-prompt-kit` is listed;
2. asking it to "write a Task Card for this request" produces the card, not a description of cards;
3. an answer to any small task ends with a gate line.

If step 3 fails, the install is fine and the prompt was not loaded. Fix the second, not the first.

## Traps

| Trap | Symptom | Action |
|---|---|---|
| Installing into the wrong profile | `--check` reports `READY`, the command is absent | check the resolved skill root printed by `--check` |
| Expecting the command in the same session | palette unchanged right after `--write` | start a new session |
| Treating `--write` as registration | files exist, nothing is visible | `--check` must say `READY`, not just "written" |
| Installing for a second runtime by hand | two divergent copies of the skill | run the installer for that runtime and let it own the files |
| Hand-editing the installed skill | the repository and the profile drift, silently | edit the repository, reinstall, re-check |
| Assuming SagaAI works like the other two | a directory appears, nothing is registered | paste the prompt into the system prompt field as the contract |

## Uninstall

Remove the skill directory and the command file named by `--check`, then reload. Nothing else on the
machine is touched: the installer writes only into the runtime profile it selected.

Next: [Environment](04-Environment.md) — the part that turns an install into cheaper repeat work.
