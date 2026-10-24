# Usage

## Load the prompt

1. Open `PROMPT.md`.
2. Copy everything below the YAML front matter into the agent's system prompt field.
3. Keep the module identifiers: reviews, docs and the linter refer to them.

Nothing else is required. The prompt names no tools, so it works in any runtime that can read files
and run commands; missing capabilities degrade explicitly (M6).

## Check the kit before trusting it

```bash
python tools/prompt_lint.py          # exit 0 = the document is structurally complete
python tools/prompt_lint.py --json   # machine-readable findings
```

## What a correct answer looks like

```text
## Answer
<the deliverable>

## Evidence
- claim — path:line / URL / command output

## Assumptions
- assumption — consequence if wrong

## Open questions
- what could not be determined, and why it matters

## Next step
<one action with its command>

gate 11/11
```

Three worked versions, in three unrelated domains, are in `examples/EXAMPLES.md`.

## First five minutes with a new subject

1. Let the agent write the Task Card. If it cannot name the subject in one sentence, it has not
   understood the request.
2. Let it write the Domain Card. If the skill set would fit any project, it is generic and useless —
   ask for the "must verify" facts specifically.
3. Read the gate line. A missing gate line means the gate was skipped.
4. Only then read the deliverable.
