# Domain docs

This is a single-context repository.

## Before changing domain behavior

- Read the root `CONTEXT.md`.
- Read relevant records under `docs/adr/` if that directory exists.
- Read the affected provider implementation, configuration page, and tests.

## Layout

```text
/
├── CONTEXT.md
├── docs/adr/       # accepted decisions, created only when needed
└── dailycheckin/   # core and provider implementations
```

Use `CONTEXT.md` for stable vocabulary and authority boundaries. Use an ADR for an accepted decision whose rationale matters across future changes. Use GitHub Issues for proposals, investigations, and unresolved work.

Do not create ADRs merely to record implementation history. Git commits and provider tests already own that evidence.

If a proposed change conflicts with an ADR, identify the conflict instead of silently replacing the decision.
