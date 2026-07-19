# DailyCheckIn context

## Purpose

DailyCheckIn executes multiple independent account automation providers and aggregates their results into configured notification channels. This fork adds a GitHub Actions runner while retaining the upstream Docker, QingLong, Synology, and local execution paths.

The fork is an operational extension of `Sitoi/dailycheckin`, not a replacement framework. Fork-specific behavior should stay small, testable, and easy to distinguish during upstream synchronization.

## Execution model

- A **Runner** selects an execution environment and schedule. GitHub Actions, Docker, QingLong, Synology, and local execution are separate runners over the same core.
- A **Provider** is one automation integration registered by `dailycheckin.configs.checkin_map` and implemented under `dailycheckin/<provider>/`.
- An **Account item** is one provider-specific configuration object. A provider may process multiple account items in one run.
- **Materialization** is the temporary conversion of `DAILYCHECKIN_CONFIG_JSON` into a permission-restricted `config.json` for the process. The file is runtime state, never repository data.
- A **Check-in result** is the provider's human-readable account outcome. Core execution aggregates results and sends them through configured notification channels.
- A **Supplementary run** is the second Beijing-time execution window. Providers may query remote state and skip work already completed earlier that day.

## Authority boundaries

- Provider APIs, retry behavior, and provider result semantics: provider implementation and tests.
- Provider configuration fields and acquisition instructions: `docs/pages/settings/`.
- GitHub Actions schedule, permissions, secret materialization, and operations: `.github/workflows/daily-checkin.yml`, its contract tests, and `docs/github-actions.md`.
- Provider registration and supported task names: `dailycheckin/configs.py`.
- Human project overview and installation routes: `README.md` and the documentation site under `docs/pages/`.
- Work planning and unresolved decisions: GitHub Issues, not this file.

## Stable constraints

- GitHub Actions uses one repository secret named `DAILYCHECKIN_CONFIG_JSON`; secret contents must not appear in commits, artifacts, summaries, or logs.
- The checked-in workflow has read-only repository permissions, bounded execution time, non-cancelling concurrency, and cleanup guarded by `if: always()`.
- Scheduled times are expressed in `Asia/Shanghai`. The current contract is 00:01 and 17:01 Beijing time.
- Provider failures must remain attributable to a provider/account. Strict CI mode may return non-zero only after all configured accounts have been attempted.
- Provider concurrency is not globally safe. It must be provider-specific, bounded, opt-in where risk exists, and retain a serial fallback.
- Hosted CI verifies repository behavior; real provider runs verify external API behavior. Neither substitutes for the other.

## Fork-specific changes

- GitHub Actions secret materialization and strict exit behavior.
- Beijing-time primary and supplementary schedules.
- Resilience fixes for notification and selected providers.
- Tieba status-aware supplementary skipping, optional bounded concurrency, and display-name fallback.

When synchronizing upstream, preserve these behaviors or explicitly replace them with equivalent upstream functionality.
