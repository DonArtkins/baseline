# Contract synchronization

A contract includes names and behavior: routes, fields, enum values, auth claims, event delivery guarantees, error semantics, env keys, service ports, tool schemas and shared visual tokens.

## Required process

1. Identify the owner, canonical document and every consumer before changing the interface.
2. Compare old and new shapes, permissions, errors and compatibility. Decide migration/rollout order.
3. Update the owning spec, canonical contract, relevant contexts and affected consumer specs. Update AGENTS when boundaries or workflow change.
4. Implement owner code and tests; consumer production changes use their own approved specs, while documentation synchronization stays with the contract change.
5. Search for stale names and assumptions, including future specs and setup guides. Preserve historical records only when labelled as such.
6. Test provider behavior and consumer expectations. Record results, gaps and rollback.
7. Update trackers and the target's change manifest (`.baseline/change.json`, generated per project) before commit/push.

## Mechanical versus semantic evidence

The gate checks declared required paths and contract records in the actual staged/committed snapshot. It cannot infer all API semantics, authenticate an approval, or prove a list of consumers is complete. Reviewers must verify the manifest against the diff. Use schemas, generated clients or contract tests once the stack is known.

Mark `contract_changed: false` only after inspecting the change. When true, `contract_docs` and `consumer_docs` must contain affected existing paths. For a contract with no consumers, explain this in `no_consumers_reason`. A checked manifest does not authorize a breaking release.
