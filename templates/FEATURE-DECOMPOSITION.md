# Decompose a project into features

Begin with user outcomes and failure journeys. Identify the owning system, required provider contracts and the smallest independently reviewable increment. A feature is not “all backend” or “make the app premium”; it has a specific result and evidence.

## Candidate families

Use only families justified by the brief. Each may yield zero, one or several specs.

| Family | Questions that define the feature | Likely owner |
|---|---|---|
| Foundation/setup | What repeatable local environment enables the first journey? | Owning implementation system |
| Identity/session | Who can sign in, recover access and end a session? | Backend plus separate consumers |
| Authorization | Which actor may do which operation on which object? | Trusted service owner |
| Data lifecycle | What is created, changed, retained, deleted and restored? | Data owner |
| Primary workflow | What task can the user complete from start to finish? | Domain owner and presentation consumer |
| Search/query | What scale, filters, ordering and pagination are necessary? | API/data owner |
| Files | What formats, sizes, permissions and lifecycle apply? | File service owner |
| Communication | Who receives which message, and what happens on delivery failure? | Domain/communication owner |
| Public experience | What information and conversion journey does the audience need? | Web |
| Account/settings | What preferences and lifecycle actions can users control? | Separate owner and consumer specs |
| Reporting | Which data, permissions, formats and provenance are required? | Data/report owner |
| Offline/platform | What happens without connectivity or with denied permissions? | Mobile or relevant client |
| AI assistance | What useful bounded task, evaluation and tool permissions exist? | AI with trusted API contracts |
| Tool exposure | Which existing capability needs an external tool interface? | MCP or adapter owner |
| Operations | How are faults diagnosed and recovered? | Relevant service and infra |
| Release verification | Which cross-system journeys prove release readiness? | QA/infra |

## Split and order

Do not force equal spec counts across layers. Merge a provider contract before dependent consumer implementation. Keep cross-system documentation synchronization on the provider branch while giving consumer production behavior its own spec. A bug belongs to its owning feature unless it introduces a separate outcome.

## Check coverage

For every requirement, point to a spec and acceptance criterion. For every spec, point back to a requirement or justified enabling dependency. Remove speculative specs with no owner or source. Confirm dependency edges have no cycles and that release-critical operational work is planned.
