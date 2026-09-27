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
`.baseline/project.json` + `change.json` are generated per target project by
`scripts/configure.py`. If they are absent, you are in the template master.

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
7. `research/knowledge-base/README.md` by topic (shared KB lives outside the
   target at `~/Projects/Workflows/knowledge-base`). Relevant `.agents/skills/`.
   For UI, `inspo/` + `docs/design/`.

Build a short reading map first. Read bodies, not just filenames. Report what was
inaccessible. Do not claim a full codebase review from an index.

## How to use baseline

### A. New project

1. Run `python3 scripts/configure.py --name <slug>` (asks what you are building
   in your own words; `--areas` / `--stack` are free text, e.g. `--areas "mobile app"`).
   This creates `~/Projects/Workflows/<slug>/` + shared `~/Projects/Workflows/knowledge-base/`
   (Windows/macOS/Linux via `Path.home()`).
2. Fill `research/project-brief.md` in the new copy. Keep unknowns open.
3. Plan with `.agents/skills/plan-project/SKILL.md` + `templates/` forms.
   Generate planning artefacts in the target's natural locations; record approvals
   in `docs/planning/APPROVALS.md`.
4. `git init -b main`, `npm install` (restores Husky from `package.json`),
   `python3 scripts/check.py --mode template`.

### B. Existing / legacy project plug-in (primary use-case)

1. Run `python3 scripts/configure.py --existing /path/to/app --name <slug> --areas "<folders you care about>"`.
   Only `.baseline/` + `BASELINE-HANDOFF.md` are written. Source, configs, and
   tooling are never overwritten.
2. Inspect the target as-is: its entrypoints, configs, tests, docs. Adopt its
   coding standards; ask the user for stack/lint/test commands if unclear.
3. Generate only missing planning (brief deltas, ADRs, specs in `templates/`
   forms) inside the target or alongside it — do not import the whole template
   tree into the target.
4. Record per-area verification commands in the target `.baseline/project.json`
   before implementation. Run `python3 scripts/check.py --mode template` from the
   template; run target tests from the target.

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
