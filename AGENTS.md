# DailyCheckIn agent rules

`README.md` is the human entrypoint. Read `CONTEXT.md` before changing execution behavior, and use the routed authority below instead of duplicating facts.

## Scope and authorities

- Provider implementations live under `dailycheckin/<provider>/`; configuration examples live under `docs/pages/settings/`.
- GitHub Actions operation, schedule, and secret handling are owned by `docs/github-actions.md`.
- Stable execution concepts and fork boundaries are owned by `CONTEXT.md`.
- GitHub issue operations are owned by `docs/agents/issue-tracker.md`; domain-document routing is owned by `docs/agents/domain.md`.
- `README.md` stays a concise human overview. Do not copy provider runbooks or Agent rules into it.

## Safety boundaries

- Never commit `config.json`, cookies, tokens, raw workflow logs, notification credentials, or materialized secret values.
- Keep the fork's GitHub Actions runner independent from Docker, QingLong, Synology, and AuroraOps execution paths.
- Do not enable upstream publishing workflows (`Deploy`, Docker publishing, or PyPI publishing) for this fork unless explicitly requested.
- Preserve the Beijing schedule contract and the second daily run as a supplementary opportunity unless the user requests a scheduling change.
- Provider acceleration must remain bounded and configurable. Preserve provider-specific rate limits and a safe serial fallback.
- A candidate or upstream change is not accepted until fork-specific tests and hosted Quality checks pass.

## Change routing

- Provider behavior: read its implementation, settings page, and relevant tests first. Add regression tests for changed status, retry, or result semantics.
- Actions behavior: read `.github/workflows/daily-checkin.yml`, `scripts/materialize_config.py`, `tests/test_actions_support.py`, and `docs/github-actions.md`.
- Core execution: read `dailycheckin/main.py`, `dailycheckin/configs.py`, and `CONTEXT.md`; preserve legacy runners unless the change explicitly targets them.
- Upstream synchronization: compare against the `upstream` remote and keep fork-only changes identifiable; do not overwrite them during merges.
- Documentation: keep each fact at one authority and link to it from other audiences.

## Validation

Use the locked environment and avoid rewriting `uv.lock` during unrelated work:

```bash
UV_CACHE_DIR=/tmp/dailycheckin-uv-cache uv run --frozen python -m compileall -q dailycheckin scripts
UV_CACHE_DIR=/tmp/dailycheckin-uv-cache uv run --frozen python -m unittest discover -s tests -v
git diff --check
```

For Actions changes, hosted `Quality checks` on `suainam/dailycheckin` is the final CI authority. A real check-in run is required when behavior depends on provider responses or repository secrets.

## Agent skills

### Issue tracker

Work for this fork is tracked in GitHub Issues. See `docs/agents/issue-tracker.md`.

### Domain docs

This is a single-context repository. See `docs/agents/domain.md`.
