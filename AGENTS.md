# Agent instructions — baseline

## What this template is

A portable planning-first workflow, not a fixed app scaffold. It adapts to the
target project's existing folders, language, and coding standards — new, existing,
legacy, single-app, web, mobile, python, monorepo, or microservices. Do not force
a rigid structure onto the target. The permanent template layout is exactly:

`AGENTS.md`, `START-HERE.md`, `README.md`, `package.json`,
`docs/`, `project-kit/`, `research/`, `templates/`, `scripts/`,
`infra/` + `qa/` (optional reference kits), `bugs/`, `inspo/`,
`.agents/skills/`, `.github/`, `.husky/`, `.coderabbit/`.

There is no `.baseline/` in the master, no `backend/ web/ mobile/ ai/ mcp/`,
no `prompts/ diagrams/ examples/`, and no fixed `--systems` list.
Generated projects receive project-owned files only (their own `AGENTS.md`,
`README.md`, `planning/` starter) — no workflow files, manifests, or dependencies.
`.baseline/` is workflow-repo-internal gated-branch state, never written into projects.

## Reading order (follow this order)

1. The user's current request + `START-HERE.md` path A (new) or B (existing).
2. `README.md` repository map (exact layout above).
3. `research/project-brief.md`, `research/open-questions.md`, `research/sources/REGISTER.md`.
4. `project-kit/context/`: product-context, system-map, stack-contract,
   integration-contracts, code-standards, progress-tracker. For infra-heavy work
   also `infra/project-kit/`; for test strategy also `qa/project-kit/`. These are
   reference kits — fill only what the target needs.
5. `docs/planning/WORKFLOW.md`, then APPROVALS, BRANCH-POLICY, CONTRACT-SYNC,
   DEFINITION-OF-READY/DONE as relevant to the task.
6. Target project's own files as-is (its folders, README, configs, code).
   Never rename/restructure target source to match this template.
7. `research/knowledge-base/README.md` by topic (shared KB lives next to the
   generated projects at `~/Projects/Workflows/my-knowledge-base/`). Relevant `.agents/skills/`.
   For UI, `inspo/` + `docs/design/`.

Build a short reading map first. Read bodies, not just filenames. Report what was
inaccessible. Do not claim a full codebase review from an index.

## How to use baseline

### A. New project

1. Run `python3 scripts/configure.py --name <slug>` (asks what you are building
   in your own words; `--areas` / `--stack` are free text, e.g. `--areas "mobile app"`).
   This creates `~/Projects/Workflows/<slug>/` with project-owned files only:
   `AGENTS.md` about that project, `README.md` with a file index, a `project-kit/`
   (context plus feature specs), `docs/`, `research/`, `bugs/` starters, and — when
   areas are given — one folder per layer, each with its own `AGENTS.md`,
   `README.md` index, and project kit. Plus the shared KB at `~/Projects/Workflows/my-knowledge-base/`.
   No workflow files, no manifests,
   no dependencies — the project's feature specs own those and the AI executes them.
2. Fill `project-kit/context/product-context.md` in the new project. Keep unknowns open.
3. Let the AI plan and spec inside the new project using its own `AGENTS.md`.
   Runtime files (`package.json`, lockfiles, containers, migrations) are created
   only when a feature spec orders them.
4. `git init -b main` in the new project when ready. The `npm install` / Husky /
   `check.py` tooling belongs to this workflow repo, not to generated projects.

### B. Existing / legacy project plug-in (primary use-case)

1. Run `python3 scripts/configure.py --existing /path/to/app --name <slug> --areas "<folders you care about>"`.
   Only missing project-owned starter files are created (own `AGENTS.md`,
   `README.md` index, `project-kit/`, layer folders with their own kits).
   Existing files are never overwritten; no workflow files, manifests, or
   dependencies are injected.
   The linkage is remembered in `~/Projects/Workflows/.registry/<slug>.json`.
2. Inspect the target as-is: its entrypoints, configs, tests, docs. Adopt its
   coding standards; ask the user for stack/lint/test commands if unclear.
3. Generate only missing planning (brief deltas, specs) inside the target's own
   `project-kit/` and layer kits — do not import the workflow tree into the target.
4. Verify with the target's own commands from its specs/tracker. The workflow's
   `check.py` gates apply to this workflow repo, not to generated projects.

## Daily prompt, skills, MCPs, Context7

Daily loop (one spec per fresh session): paste `templates/daily-implementation-prompt.md` after each merge, clear the session, repeat. How-to: the prompt file's header + `docs/planning/BRANCH-POLICY.md` + `docs/tooling/GATES.md`.

Skills: check `.agents/skills/` first every session (`plan-project`, `contract-sync`, `git-branch-flow`, `current-docs`, etc.). Missing skill? Create it from `templates/skill.md` and re-run the gate.

MCPs/Context7: MCP servers (Context7 for current docs, filesystem, GitHub, etc.) are per-machine config, never committed keys — setup per editor in `docs/tooling/SKILLS-MCP-CONTEXT7.md`. Force-use directive every session: "Always use repo skills first; always use Context7/MCP to fetch current docs for every tool, framework, package, and MCP service — never answer versioned APIs from memory; record library, version, source, date. If unreachable, say so and mark unverified." Save it in your editor memory too.

## Hard rules

1. **User structure wins.** Ask what they are creating; no fixed area list.
2. **Plan before production code.** Reviewable specs + acceptance criteria first.
3. **One fact, one owner.** Status in trackers; order in roadmap; decisions in ADRs.
4. **Contract sync in same change.** Owner + consumer docs together.
5. **Physical ownership.** Target code stays in the target. Template stays clean.
6. **One spec, one branch, one PR.** See `docs/planning/BRANCH-POLICY.md`.
7. **Evidence before completion.** Real command output, revision, env, limits.
8. **Tracker before push.** Update owning tracker in the same branch.
9. **Fix and explain.** Reproduce, scope fix, verify, keep regression evidence.
10. **Research current interfaces.** Version-specific official docs first.
11. **Security explicit.** No committed credentials/dumps. Least privilege.
12. **Tools respect permissions.** No publishing/migrations/deploy outside scope.
13. **Readable workflow.** Route, don't narrate, in agent files.

## Verification

Read `docs/tooling/GATES.md`. `python3 scripts/check.py --mode template` checks
this layout; `--mode staged/branch` checks target branches with `.baseline/`.
Husky runs staged checks; CI repeats them. Register real lint/test/security
commands per target area before implementation.

## Communication and handoff

State what changed, why, what was verified, what remains open. Use
`templates/handoff.md`. For the daily loop (one spec per fresh session), use
`templates/daily-implementation-prompt.md`. Never present scaffolds as shipped features.
