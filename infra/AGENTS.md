# Infra agent instructions

Read [root AGENTS](../AGENTS.md) first. This is an optional reference kit; use it when the target needs infra planning. Never force it onto a project that does not need it.

## Ownership

Environments, build/release delivery and recovery. Production paths belong to this system. Do not write another system's implementation while working this spec; synchronize affected contracts and consumer documentation through the root process.

## Read next

Read this kit's progress tracker, owning numbered feature spec, architecture, stack contract, integrations, code standards and test strategy. Read `environment.md` and `deployment-targets.md` when relevant. Consult root skills and the local skill before implementation. UI work also reads inspiration and approved design artifacts.

## Local gates

No runtime stack or commands are selected. Record the target's real `checks` and `security` commands in that target's `.baseline/project.json` (created by `scripts/configure.py`) before implementation. Local tests are owned here; cross-system journeys can be owned by QA.

## Delivery

Follow root approval, branch, contract sync and tracker-before-push rules. A drafted spec is not shipped behavior. Record exact evidence and open operator gates; keep delivery history out of this file.
