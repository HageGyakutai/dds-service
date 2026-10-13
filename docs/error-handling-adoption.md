# Error handling adoption — dds-service

Audit: 2026-10-13; integration baseline `main` at `a9ff5f21a7f552258daf0e395ac5de074f9fd616`.
Status: **policy proposal; runtime changes not implemented in this PR**.
This is a scoped audit of the listed files, not a complete error/client inventory.

## Baseline

Django/DRF app, not a FastAPI microservice. CashflowRecord.clean()/save() use Django ValidationError; CashflowRecordForm.clean() preserves field-level messages and add_error semantics. These framework adapters are intentional existing boundaries, not defects solely because they use Django. No AGENTS.md existed. There is no claim of a pure application hierarchy or central DRF catalog yet.

Observed locations: apps/transactions/models/cashflow_record.py; apps/transactions/forms.py; apps/transactions/views/; config/.

## Adapted mandatory target

[Shared Error Handling Standard 1.0.0](error-handling-standard.md):
**Typed Domain/Application Exceptions + Centralized Exception Translation**.

For new extracted application policies, typed core errors must be framework-independent. Translate them through a central Django/DRF transport policy while retaining form.add_error, field keys, HTML pages, redirects and JSON endpoint contracts. Never install FastAPI handlers in Django. Keep Django model/form validation at framework adapters. Do not rewrite the working ORM/form architecture merely to rename layers.

Actual pyproject uses Python 3.13, Black/Flake8/MyPy/Pytest, not Ruff. Retain existing checks. Adding pinned Ruff or a canonical full script is a separate tooling task; no formatter/linter migration is included.

## Compatibility and privacy

Preserve current statuses, JSON/HTML/CLI contracts, messages/field keys, auth/retry/security headers and OpenAPI where present.
No forced JSON/RFC 9457 conversion. Contract changes require a separate owner-approved task.
No cross-repository runtime dependency. Redact secrets; validate/bound correlation identifiers; never suppress cancellation or cleanup failure.
Unknown HTTP failures must remain safe 500; workers retain explicit terminal/retryable/unknown outcomes.

## Pending work and acceptance

Complete the class/raise-site/client/status/body/header or CLI-exit table first.
Add failure/contract/secrecy regression tests, then minimally adapt the existing architecture.
Add AST-aware transport import checks where meaningful. Preserve every existing test and gate.
Run the actual locked checks and real integrations before exact-SHA acceptance.

Existing check commands / applicable verification:

```bash
uv sync --locked --extra dev
uv run --locked black --check .
uv run --locked flake8
uv run --locked mypy apps config
uv run --locked pytest
```

Checks have not run for this docs-only proposal. Docker/live-provider validation remains unverified.
Keep PR Draft; owner approval and applicable local Quality Gate on final SHA are required before merge.
No CI workflow changes.
