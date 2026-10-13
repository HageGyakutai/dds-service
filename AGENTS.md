# dds-service engineering rules

Work only in this repository. Preserve its actual stack and public contracts.


## Shared Error Handling Standard 1.0.0 (mandatory)

All new and changed error mechanisms use **Typed Domain/Application Exceptions + Centralized Exception Translation**.
Read `docs/error-handling-standard.md` and the repository-specific `docs/error-handling-adoption.md` before changing error behavior.
Keep domain/application independent of FastAPI, HTTP and API schemas. Retain existing compatible base classes.
Own exception classes, public code catalog and centralized transport handlers within this repository;
use the existing locations recorded in the adoption document rather than duplicate implementations.
Preserve existing status/body/messages, OpenAPI, WWW-Authenticate, Retry-After and security headers.
New namespaced codes must not silently rename legacy codes; contract changes require a separate task.
Redact secrets and validation inputs. Unknown HTTP failures return safe 500; correlate safe logs with validated request IDs.
Never swallow cancellation, shutdown or resource-cleanup errors. Workers classify retryable/terminal/unknown failures without HTTP statuses.
Contract/security tests and AST-aware import boundaries are mandatory where applicable; preserve all existing checks.
Run locked Ruff, MyPy, Pytest, integration/security and the canonical full local Quality Gate.
Policy documentation is not proof of runtime compliance. Keep incomplete/unvalidated PRs Draft.
No feature/PR automatic CI; no merge without owner approval and their full local gate on the exact final SHA.

## Existing stack compatibility

Actual pyproject uses Python 3.13, Black/Flake8/MyPy/Pytest, not Ruff. Retain existing checks. Adding pinned Ruff or a canonical full script is a separate tooling task; no formatter/linter migration is included.
