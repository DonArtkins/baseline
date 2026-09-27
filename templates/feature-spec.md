# Feature {{ID}} — {{TITLE}}

## Outcome

State the user-visible behavior and why it matters. Identify the owning system and the requirement/source IDs. Status belongs to the owning tracker.

## Context to read first

Link the brief, relevant context files, canonical contracts, decisions, approved diagrams and applicable skills. Include source versions for third-party interfaces.

## Dependencies

List `system:NN` prerequisites, merged contract versions and any open questions. Distinguish implementation dependencies from review or release gates.

## Files owned and separation of concerns

List production paths this feature owns, consumer documentation it must synchronize and explicit exclusions. Keep domain, presentation, infrastructure and intelligence responsibilities separate.

## Setup and initialization

Give exact verified commands, versions, environment variable names (never values), synthetic fixtures and expected readiness checks. Mark commands not yet verified.

## Contracts and data

Define new/changed routes, payloads, errors, authorization, events, schemas, tool IDs, config or design tokens through canonical documents. State `No contract change` only after checking the scope. Link approved ERD before schema implementation.

## UI and experience

If applicable, link reference IDs, approved wireframe/version, component contracts and required responsive/interaction states. Otherwise state why this section does not apply.

## Implementation plan

Describe the smallest reviewable sequence, including error/recovery paths. Do not begin production code before the concrete scope is approved.

## Security and privacy

Identify trust boundaries, input validation, permissions, sensitive data, logging and relevant abuse cases. Link the threat model and required verification.

## Docker and deployment

State local/CI/production effects, services/config/migrations, rollout and rollback. `No deployment change` is valid with a reason. Do not create containers merely to fill this section.

## Acceptance criteria

- [ ] Replace with a binary user behavior criterion and its verification method.
- [ ] Define relevant failure/denial/recovery behavior and evidence.
- [ ] Verify contract consumers and documentation alignment.
- [ ] Record required test/build/lint/security results and limitations.

## Verification evidence

| Criterion | Command/manual procedure | Revision/environment | Pass/fail/skip | Evidence |
|---|---|---|---|---|
| Not yet defined | Not run | Not available | NOT RUN | None |

## Approval and operator gates

| Gate | Applicable? | OPEN/CLOSED/NOT-APPLICABLE | Evidence |
|---|---|---|---|
| Implementation plan | Yes | OPEN | Actual user approval required |
| ERD/schema | Decide | OPEN | Approve before schema code if applicable |
| UI design | Decide | OPEN | Approve before UI code if applicable |
| Migration apply/release | Decide | OPEN | Separate environment authorization |

## Deviations and review

Record deviation ID, trigger, prior plan, decision, tests and affected documents. Link bug/review records. Do not mark acceptance complete before evidence exists.
