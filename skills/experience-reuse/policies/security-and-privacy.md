# Security, privacy, retention

The store holds knowledge about work, not the work's confidential content. Three risks are real:
a secret pasted into a record, a customer's data preserved forever, and an outdated recipe that keeps
being trusted.

## What may never be stored

| Never | Why |
|---|---|
| Credentials: passwords, tokens, API keys, private keys, cookies, session ids | a record is copied, indexed and published; a secret in it never comes back |
| Personal data: names, e-mails, phone numbers, addresses of people | the store is not a CRM and has no lawful basis |
| Customer content: database rows, documents, correspondence | the shape of a solution is reusable, the content is not |
| Internal hostnames, IP addresses, internal paths | they leak topology and rot quickly |
| Unverified output | a guess with a schema is worse than no record |

## Placeholders

| Placeholder | Replaces |
|---|---|
| `<HOST>` | any hostname or IP |
| `<USER>` | any account name |
| `<PATH>` | any absolute path, especially machine-specific |
| `<API_KEY>`, `<TOKEN>` | any credential |
| `<CUSTOMER>`, `<PROJECT>` | any organization or repository name that is not public |
| `<DB>` | any database name |

The tool enforces part of this: `experience.py add` refuses a record containing a token-shaped
literal or an absolute machine path. That is a floor. It cannot tell a real hostname from a
placeholder, so a human reads the record before it is published.

## Sensitivity levels

Every record that touches private context declares a level in its body, under a `## Sensitivity`
heading:

| Level | Meaning | Allowed where |
|---|---|---|
| `public` | no private context; safe in a public repository | anywhere |
| `internal` | mentions a private project shape without identifying it | a private store only |
| `restricted` | mentions a named organization or environment | not stored; keep it in the private system of record |

A record at `restricted` is a note to yourself that the store is the wrong place.

## Retention

| Rule | Reason |
|---|---|
| Records are deprecated, never deleted | the audit trail is what makes the store trustworthy; a silent deletion brings the wrong approach back |
| `status: deprecated` plus `superseded_by: <id>` | the reader is redirected instead of stopped |
| `last_verified_at` older than 180 days produces a warning | a validation from last year does not describe this year |
| `last_verified_at` is set only after a real revalidation | otherwise the field lies and the next agent believes it |
| A superseded recipe stays readable | it explains why the new one exists |

## Revalidation

Revalidation means: run the recipe's validation again in the current environment. If it fails, the
record becomes `deprecated` and the failure goes into a `failure` record linked to it. Marking
`validated` after reading the record is not revalidation — reading proves nothing about the
environment.
