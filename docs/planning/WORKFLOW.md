# The planning and delivery workflow

## 1. Discover

Read the brief and binding inputs. Identify users, workflows, constraints, success measures and unknowns. Convert vague requests into examples: who acts, on what, with which permission, and what should happen if it fails. Keep requirements traceable to sources.

## 2. Research

Ask focused questions. Use social posts to discover ideas and authoritative material to verify mechanisms and limitations. Record alternatives and why a choice fits this project. Use the [knowledge-base guide](../../research/knowledge-base/README.md) to retain reusable learning outside project-specific decisions.

## 3. Design the system

Select the necessary systems. Document ownership, interfaces, security boundaries and operational failure paths. Design data and migrations before schema code. Select infrastructure from budget and measured needs, not from a maximal architecture checklist. Produce reviewed diagrams and ADRs.

## 4. Design the experience

Catalogue references, choose a visual direction, extract tokens, define component states, map screens to user journeys and validate accessibility/responsiveness. Use [the inspiration workflow](../design/FROM-INSPIRATION-TO-SYSTEM.md). Approve wireframes and the resulting system before UI implementation.

## 5. Decompose into features

Use one numbered spec per independently reviewable outcome in each owning system. Start with foundations only when a real consumer needs them. Each spec includes setup, ownership, dependencies, contracts, deploy impact, tests and binary acceptance criteria. Do not generate hundreds of speculative specs to imitate a large project.

## 6. Order and approve

Build the dependency graph and roadmap. Validate that a consumer never precedes its required provider contract. Create initial trackers and record approvals against specific versions. Resolve blocking questions; keep future uncertainty visible without preventing unrelated authorized work.

## 7. Implement one spec

Cut a feature branch from the fetched remote default branch. Read the owning context and current API docs. Work within owned paths, verify important behavior and failure modes, synchronize contracts, and record deviations. Keep evidence and status current.

## 8. Review, release and learn

Run local gates and CI; review findings against evidence; update the tracker before push. Merge and deploy only within authorization. Verify release and rollback procedures separately. Feed reusable lessons back into the knowledge base as reviewed guidance; do not turn every local fix into a universal rule.
