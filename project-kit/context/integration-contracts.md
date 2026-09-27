# Integration contracts

Status: UNFILLED. Canonical contract records live in [docs/contracts](../../docs/contracts/README.md).

## Registry

| Contract ID | Owner | Canonical document | Consumers | Compatibility/version |
|---|---|---|---|---|
| None yet | To decide | Create after discovery | To identify | To decide |

Register REST/GraphQL interfaces, events, jobs, tool IDs, auth claims, env names, ports, design tokens and shared error shapes only when the project needs them. Track names and semantics, not credential values.

## Consumer alignment

Each consumer links the authoritative version and lists supported operations, errors and known gaps. An unavailable provider capability remains an explicit blocker; a mock is not proof the capability exists.

## Change procedure

Use [contract sync](../../docs/planning/CONTRACT-SYNC.md), record affected paths in the target's `.baseline/change.json` (generated per project; absent in the template master), update consumers in the same branch, and include compatibility/rollback tests. Keep retired values only in clearly historical migration records.
