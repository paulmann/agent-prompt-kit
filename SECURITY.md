# Security policy

## Scope

This repository ships a prompt and a linter — no service, no network calls, no credentials. The
security surface is therefore narrow, but two risks are real:

| Risk | Why it matters | Mitigation |
|---|---|---|
| A prompt that instructs an agent to disclose secrets | the prompt is copied into other systems, so a bad rule propagates | M6 rule 5 forbids reading, printing or echoing secrets; `docs/QA.md` item 7 checks it |
| A prompt that normalises irreversible actions | copy-paste damage in someone else's repository | M6 rules 2–3: sandbox first, dry run by default, explicit approval |
| A linter that silently passes | a green check over an empty tree is the failure the kit exists to prevent | the linter reports `0 findings` only after running every check; a missing `PROMPT.md` is a usage error, not a pass |

## Reporting

Use the private channel: the **Security** tab → **Report a vulnerability**. Do not open a public issue.

Include: the file and line, the text of the rule you consider unsafe, and the scenario in which an
agent following it would cause harm. A prompt vulnerability is a rule that produces damage when
obeyed — that is the standard this document should be judged by.

Expect an answer within seven days. Accepted reports are fixed in `PROMPT.md` and `PROMPT.ru.md` in
one commit, with a `Security` entry in the changelog.

## Supported versions

| Version | Supported |
|---|---|
| 1.0.x | yes |
| < 1.0.0 | no |

## What the kit never does

- It makes no network requests. The linter reads local files only.
- It stores and prints no credentials; it has no code path that could.
- It does not execute repository content. There is nothing to execute but the linter itself.
