# Starter topics — first draft to research

A new knowledge base starts empty. Work this list top-down: one short note per topic using [the knowledge-note template](../../templates/knowledge-note.md) (question, short answer, when it applies, alternatives, sources, verification exercise, open uncertainty, last-reviewed date). Skip what your work never touches; add what it keeps asking for.

## Core (write these first)

1. API error design — error shape, status mapping, retryable vs fatal.
2. AuthN/Z defaults — sessions vs tokens, permission checks placement, failure behavior.
3. Data validation — where boundaries validate, how errors surface.
4. Testing minimum — what every feature proves before review (unit, contract, journey).
5. Logging and redaction — what to log, what never to log, secret handling.
6. Configuration and environments — env vs files, per-environment matrix, migration order.

## Engineering (as your stack demands)

7. Your framework's data fetching — caching, invalidation, failure states.
8. State ownership — which layer owns which state, single source per fact.
9. Migrations — additive-first order, rollback story, destructive-change approval.
10. CI gates — lint, test, security commands that actually run per change.

## Delivery

11. Branch and release flow — one spec per branch, tracker before push, merge order.
12. Review disposition — reproduce, classify, fix-or-dispute with evidence.

Each finished note goes in the shared base under `core/`, `engineering/`, or `decisions/`; project-specific details stay in their project. See [organization](ORGANIZATION-AND-RETRIEVAL.md) and [maintenance](MAINTENANCE-AND-PROJECT-USE.md).
