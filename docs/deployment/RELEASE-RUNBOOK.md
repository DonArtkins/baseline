# Release and rollback runbook

Status: TEMPLATE; commands must be filled and tested for the chosen deployment.

## Before release

Identify revision/artifact, target environment, owner, dependency versions, config changes, backup/recovery evidence and approved migration plan. Run the declared release gates and confirm access to rollback mechanisms.

## Release

Write exact commands only after the platform is selected and verified. Record expected output and a stop condition for each step. Separate deployment from database migration and external notifications.

## Verify

Exercise a representative authorized user journey, health checks, error signals and data correctness. Record timestamps and revision. A successful build or process start alone is not release verification.

## Roll back

State which artifact/config can revert, which data changes cannot, and how to recover. Test the recovery path in an isolated environment before relying on it.
