# Usage

## Load the prompt in three steps

1. Open [`PROMPT.md`](https://github.com/paulmann/agent-prompt-kit/blob/main/PROMPT.md).
2. Copy everything **below the YAML front matter** — the front matter is metadata for the maintainers,
   not instructions for the agent.
3. Paste it into the system prompt field of the agent, or into the rules file the runtime reads.

Nothing else is required. The prompt names no tools, so a missing capability degrades explicitly (M6):
the agent says which one is absent instead of pretending it worked.

## Check the kit before trusting it

```bash
python tools/prompt_lint.py            # exit 0 = the document is structurally complete
python tools/prompt_lint.py --json     # the same findings, machine-readable
python tools/experience.py selftest    # the store refuses what it claims to refuse
```

Measured on a fresh clone:

```text
PASS: 0 error(s), 0 warning(s)
13/13 experience checks passed
```

The linter is a structural gate, not a judgement about content: it proves that every module exists,
carries a `**Check:**` line, has its Russian twin, and that cross-references resolve. Judgement is
covered by `docs/QA.md` in the repository.

## What a finished answer looks like

```markdown
## Answer
<the deliverable itself, without preamble>

## Evidence
- claim — path:line / URL / command output

## Assumptions
- assumption — what changes if it is wrong

## Open questions
- what could not be determined, and why it matters

## Reused experience
- record id — applicability verdict (match | adapted | rejected) — what was adapted

## Next step
<one action, with its command>

gate 12/12
```

`## Reused experience` appears only when the store actually produced something used; the gate line
appears always.

## Four checks before you read the deliverable

| Check | Fails when |
|---|---|
| the subject is named in one sentence | the answer addresses a neighbouring, easier question |
| a gate line is present | the answer looks auditable and is not |
| every assumption names its consequence | "probably fine" without a cost if it is not |
| the out-of-scope part is written down | half the request was silently dropped |

## First ten minutes with a new subject

1. Let the agent write the **Task Card** (M1). If it cannot name the subject in one sentence, it has not
   understood the request — stop it there, it is cheaper than reading three pages of the wrong work.
2. Let it write the **Domain Card** (M2). A skill set that would fit any project is generic and
   useless; ask for the facts marked "must verify" specifically.
3. Watch the first **verification** (M5). It must compare the output against an expectation written
   *before* the action, not adjust the expectation afterwards.
4. Read the gate line, then the deliverable.

At most one clarifying question is allowed, and only if the gap blocks all progress (M1 rule 3). Every
other gap goes into `Unknowns` and into `## Assumptions`.

## When the agent skips a step, name the module

Module identifiers are the interface, not decoration:

| Symptom | Say |
|---|---|
| a plausible answer with no sources | "M3 and M4: where is the context ledger, and which claims are labelled?" |
| work started without understanding the request | "M1: write the Task Card first" |
| the answer is confident about code nobody read | "M4 rule 3: `I could not check` is allowed" |
| something irreversible was done quietly | "M6 rules 2–3: sandbox first, or ask" |
| the gate line is missing | "M8: run the gate and report it as one line" |
| the same work is about to be redone | "M13: search the store before planning" |

## Irreversible actions

Deletion, overwrite, migration, publish, send: the prompt requires a sandbox reproduction with a decoy
that must survive, a dry run where the tool offers one, and an explicit approval (M6). If an agent
skips that, the answer is not "mostly right" — it is not accepted, whatever the rest of it looks like.

Next: [Module map](02-Modules.md) for what each module verifies, or [Install](03-Install.md) to put the
command palette entry in place.
