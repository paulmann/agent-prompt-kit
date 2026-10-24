# Worked examples

Three domains, one shape. Each example shows what the agent must produce before answering — a Task
Card and a Domain Card — then a compressed answer with labels and a gate line. Module references
point at `PROMPT.md`.

## Example A — legacy PHP admin panel

**Request (abridged).** "The panel lists hosting accounts without the expiry date. Add it."

```text
TASK CARD
Subject:        self-hosted PHP panel for a registrar account
Deliverable:    the expiry date rendered in the accounts table and returned by the list endpoint
Audience:       two operators who use the panel daily
Success looks:  the column shows a date for 100% of rows that have one in the database
Constraints:    PHP 8.x, no new dependencies, existing tests must stay green
Unknowns:       whether "expiry" lives in the accounts table or is derived
Out of scope:   redesign of the table, sorting, exports

DOMAIN CARD
Practitioner:    backend engineer maintaining an internal admin panel
Core vocabulary: migration, endpoint, presenter, scope, idempotent sync
Skill set:       schema reading; request flow; template rendering; test hygiene
Must verify:     the real column name; whether the field is nullable; whether the
                 endpoint is cached
Sources of truth: migrations, the schema of the live table, the endpoint source
Typical failure: writing SQL against remembered column names
Definition of done: the endpoint returns "expires_at" and the table renders it, with
                 the existing suite green
Anti-patterns:   widening SELECT *; formatting dates in the template; adding a
                 migration without a rollback path
```

Answer, compressed:

```text
## Answer
Add "expires_at" to the accounts endpoint and render it as an ISO date column.
[fact] `accounts` has `paid_till` (DATE, nullable) — migrations/2026_03_accounts.sql:14
[fact] the list endpoint selects an explicit column list — src/Http/Accounts.php:61
[inference] `paid_till` is the "expiry" the operators mean, since no other date column exists
[assumption] rows with NULL should render "—" rather than an empty cell; if wrong, only the
             display changes, not the query

## Evidence
- column name and nullability — migrations/2026_03_accounts.sql:14
- explicit select list — src/Http/Accounts.php:61
- test that covers the endpoint — tests/AccountsTest.php:88

## Assumptions
- NULL means "no expiry set" — consequence: the column shows "—" for legacy rows

## Open questions
- whether the panel is cached per session; if it is, the date may lag by a request

## Next step
php tools/lint.php && php backend/tests/run.php     # expected: 0 failures

gate 12/12
```

## Example B — Windows service with a WinForms configurator

**Request (abridged).** "Add a security audit button to the MikroTik page."

```text
TASK CARD
Subject:        Windows service plus a WinForms configurator for network devices
Deliverable:    a button that requests a security audit over IPC and shows the report
Audience:       network administrators running the configurator
Success looks:  the report renders, the service stays healthy, the IPC contract test passes
Constraints:    append-only IPC command ids; no breaking change to the wire format
Unknowns:       whether a suitable IPC command already exists
Out of scope:   remediation, scheduling, export formats

DOMAIN CARD
Practitioner:    senior .NET engineer owning both the service and its UI
Core vocabulary: IPC command registry, long operation timeout, DTO, grid export, service identity
Skill set:       IPC contract discipline; async UI handling; test suite hygiene; log semantics
Must verify:     the next free command id; whether the dispatcher has a timeout registry;
                 whether the grid must be attached to the clipboard/export helper
Sources of truth: the IPC enum, the dispatcher, the UI test that counts async handlers
Typical failure: adding an id that collides, or registering a long command without a timeout
Definition of done: the command id is unique and documented, the timeout registry lists it,
                 the grid export test passes, the service restarts clean
Anti-patterns:   calling the service from the UI thread; treating a log line as proof of health
```

Answer, compressed:

```text
## Answer
Add IPC command 95 "GetSecurityAudit" (append-only), register it as a long operation, and
wire the button through the existing async handler wrapper.
[fact] highest used command id is 94 — Service/Ipc/IpcCommand.cs:31
[fact] long operations are listed in a registry with a test — Service/Ipc/IpcConstants.cs:12
[fact] all UI async handlers go through SafeAsyncHandler — Configurator/Pages/MikroTikPage.cs:204
[inference] the audit can take up to 45 s, so it must be a long operation
[assumption] no existing audit command exists; if one does, reuse it instead of adding 95

## Evidence
- command id ceiling — Service/Ipc/IpcCommand.cs:31
- timeout registry — Service/Ipc/IpcConstants.cs:12
- async handler policy — Configurator/Pages/MikroTikPage.cs:204

## Assumptions
- the audit is a new capability — consequence: one more command to document and test

## Open questions
- whether the service identity differs from the configurator's; a read-only device account
  may be enough

## Next step
dotnet test RdpAudit.sln -c Release --no-build -p:Platform=x64   # expected: all green

gate 12/12
```

## Example C — documentation product

**Request (abridged).** "Our wiki is unreadable; make it a real documentation set."

```text
TASK CARD
Subject:        the documentation surface of one GitHub repository
Deliverable:    a wiki with navigation, resolving links and a changelog that parses
Audience:       operators who already found the repository
Success looks:  every page reachable from navigation, every link resolves, no orphan page
Constraints:    flat wiki namespace; no relative images; English canonical, ru as translation
Unknowns:       whether the wiki repository already exists on the server
Out of scope:   a marketing site, search engine optimisation, blog posts

DOMAIN CARD
Practitioner:    documentation engineer for developer tools
Core vocabulary: anchor, flat namespace, sidebar, footer, comparison link, canonical page
Skill set:       markdown rendering rules; anchor computation; changelog semantics; link resolution
Must verify:     the platform's image limits; the anchor algorithm; whether a wiki page is
                 addressable without an extension
Sources of truth: GitHub documentation, the rendered table of contents, the changelog standard
Typical failure: a green link check that never resolved an anchor
Definition of done: build and verify clean, dry-run publication reviewed, navigation covers
                 every page, both language sets present
Anti-patterns:   hand-writing a table of contents; deleting foreign pages "for tidiness"
```

Answer, compressed:

```text
## Answer
Eight canonical pages plus eight translations, ordered by a manifest; internal links lose
".md"; the footer carries absolute links only.
[fact] a wiki page is addressed without an extension — measured on a live wiki sidebar
[fact] a relative image cannot work: the wiki is a separate repository — GitHub documentation
[fact] the platform accepts PNG/JPG/GIF under 1 MB for a social preview — GitHub documentation
[inference] the existing 12 pages are unreachable because the sidebar lists 6 of them
[assumption] the wiki repository is not created yet; if it is, publish directly and skip
             the first-page step

## Evidence
- wiki mechanics — GitHub documentation, "About wikis"
- anchor rules and the em-dash case — GitHub documentation plus a live table of contents
- image limits — "Customizing your repository's social media preview"

## Assumptions
- the first publication needs one page saved in the interface — consequence: one manual step

## Open questions
- whether the team wants the wiki indexed; that needs GitHub Pages instead

## Next step
python <pack>/tools/ghagent.py wiki build && ... wiki verify     # expected: 0 errors

gate 12/12
```

## What the three examples have in common

| Element | Why it is there |
|---|---|
| A declared subject in one phrase | prevents domain drift (M2) |
| Three to five "must verify" facts | separates a specialist from a confident generalist |
| One acceptance condition a reviewer can test | makes "done" falsifiable |
| One labelled assumption with its consequence | keeps honesty without paralysis |
| A single next action with an expected result | makes the answer actionable |
| A gate line | makes the answer auditable (M8) |

None of the three examples required editing the prompt. That is the claim the kit makes: a new domain
costs one card, one examples entry and one acceptance line (M10).
