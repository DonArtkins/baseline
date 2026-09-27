# Definition of ready

A feature is ready when its user outcome, owned files, dependencies, setup, contracts, security considerations, deploy effect and binary acceptance criteria are concrete. Relevant diagrams and design references have actual approval. External APIs are verified against current version-specific sources. Blocking questions are resolved; nonblocking assumptions have owners and expiry/review conditions.

Before moving project phase to `implementation`, record real per-area commands and link the planning approval in the target's `.baseline/project.json` (created by `scripts/configure.py`). Use the readiness checklist in the feature spec. A general roadmap approval does not approve unspecified schema, destructive migration or external actions.
