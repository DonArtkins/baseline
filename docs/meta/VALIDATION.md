# Template validation

Validated in the checked-out copy of this repo (paths below are repo-relative or `~`-relative so they hold for any dev on any OS — never a hardcoded home directory). This report concerns the reusable workflow, not a future application's acceptance or security.

## Passed

- Structural checks: required documents, local inline Markdown links, spec/chain/status consistency and configuration.
- 28 behavioral tests, zero failures and zero skips, including isolated Git repositories.
- Staged secret detection even when the working copy has been cleaned.
- Missing tracker updates, invalid scope, undeclared consumer documents, unapproved production and schema changes are rejected.
- Runtime command failure blocks a branch check; a dirty tree cannot stand in for the committed snapshot.
- Initial planning bootstrap, feature branches and overlapping unmerged remote commits are handled explicitly.
- Pre-push ref checks reject a feature-to-main refspec, a different commit and deletion operations.
- All 17 SKILL.md files passed the available skill validator.
- CodeRabbit and GitHub workflow files parsed with a YAML parser. Parsing is not full service-schema validation.
- SHA-256 comparison found zero changes across 2,267 inventoried Griot files and 41 knowledge-base Markdown files; Griot's initial Git status was preserved.

- Husky 9.1.7 via `package.json`; run `npm install` to generate the lockfile. This dependency result is not a product security audit.
- Actual Husky pre-commit and pre-push hooks passed in a disposable repository/local bare remote; a subsequent staged synthetic secret-shaped fixture was rejected. No GitHub repository was created or changed.
- The master template carries no `.baseline/` (workflow-repo-internal gated-branch state only). This repo's own hooks activate with `npm install`; generated projects use their own toolchain from their specs.

## Not activated or not verified

- GitHub-hosted CI, repository protection and CodeRabbit account integration: no repository/account changes were made.
- Product lint/build/security/integration commands: intentionally unconfigured until a real project selects its stack. Implementation phase rejects empty command lists.
- Video/reel transcripts and X post contents: unavailable; the source register retains their access status.
- Full Markdown style lint, external-link checks and anchor validation: not part of the included checker.

## Maintenance

Rerun the documented checks when the workflow changes. Extend regression tests for a new owner/system or gate rule. Keep unknowns and skipped checks visible. An approval link proves a record exists; a human must verify its authenticity and scope.

## Owner review 2026-09-27

The repo owner inspected every generated test project and approved them as perfect. The single finding: knowledge-base and project locations must be dynamic per dev (not one machine's home, not one OS). Fixed — `scripts/configure.py` resolves everything from `Path.home()` with a `BASELINE_KB_HOME` override; docs use `~`-relative paths only.

## End-to-end proof 2026-09-27 (branch `feature/root/02-nextjs-landing-page-test`)

`configure.py` generated `~/Projects/Workflows/nextjs-landing-test/` (4 project-owned files, no residue by grep). Official `create-next-app@latest` (Next.js 16.3.6, TS, Tailwind, `--empty`) scaffolded to temp, merged under `web/` with all project files intact; `web/AGENTS.md` layer kit added per generated instructions. Landing hero written to `web/src/app/page.tsx`; `npm run build` passes (static `/`, TypeScript clean). Sandbox deviation only: `npm install` requires `--ignore-scripts` here. Test project retained for manual viewing.

## Shape matrix proof 2026-09-27 (same branch)

Single app stays flat at the root — no layer subfolders. Layer folders appear only with 2+ areas; `--link` cross-references multi-repo siblings.

- `vue-landing` (single, Vue+TS): official create-vue merged flat at root, zero losses; `npm run build` clean, `test:unit` 1 passed.
- `acme-monorepo` (web app + python api): `web-app/`, `python-api/` each with AGENTS.md, README.md index, project kit.
- `shop-web` ↔ `shop-api` (multi-repo): separate roots, linked both ways in AGENTS.md + system-map.
- `python-tool`, `ml-vision`, `py-backend` (singles): flat, 13 files each.
- `microservices` (gateway, orders, payments): three layer kits.
- No-overwrite: re-ran plug-in over hand-edited files — "nothing overwritten", edits intact.
- Residue greps across all generated trees: clean. `nextjs-landing-test` flattened to root (stray `landing-page/` removed, app rebuilt in place).
