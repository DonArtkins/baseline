# Template validation

Validated locally on 2026-09-27 in `/home/artkins/Programming/baseline`. This report concerns the reusable workflow, not a future application's acceptance or security.

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
- The master template remains without Git history and without `.baseline/` (per-target state). Run `git init -b main` and `npm install` in a new project copy to activate hooks there.

## Not activated or not verified

- GitHub-hosted CI, repository protection and CodeRabbit account integration: no repository/account changes were made.
- Product lint/build/security/integration commands: intentionally unconfigured until a real project selects its stack. Implementation phase rejects empty command lists.
- Video/reel transcripts and X post contents: unavailable; the source register retains their access status.
- Full Markdown style lint, external-link checks and anchor validation: not part of the included checker.

## Maintenance

Rerun the documented checks when the workflow changes. Extend regression tests for a new owner/system or gate rule. Keep unknowns and skipped checks visible. An approval link proves a record exists; a human must verify its authenticity and scope.
