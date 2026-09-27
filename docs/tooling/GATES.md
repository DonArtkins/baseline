# Configure and run the gates

## Modes

| Mode | Candidate checked | Intended use |
|---|---|---|
| `python3 scripts/check.py --mode template` | Current files, excluding generated/local folders | Validate the template or target docs structure |
| `python3 scripts/check.py --mode staged` | Git index, including partially staged content | Husky pre-commit |
| `python3 scripts/check.py --mode branch` | Committed HEAD against the remote default merge-base | Pre-push and PR CI |
| `python3 scripts/check.py --mode branch --base COMMIT` | Committed HEAD against an explicit base | Reproducible review or CI |

The template master has no `.baseline/` — that is expected. `.baseline/` is
workflow-repo-internal gated-branch state, never written into generated projects. Template
validation does not run product tests. Branch mode requires a clean tree.
Missing history fails explicitly; the checker never guesses an unrelated base.

## Included checks

- Required documents (`AGENTS.md`, `START-HERE.md`, `package.json`, brief, approvals, contract-sync) and local inline Markdown link targets.
- Feature IDs, required spec sections, Full/Next chain grammar and status-board coverage (for discovered `*/project-kit/` kits — root, `infra/`, `qa/`).
- Skill frontmatter with a name and description.
- Common credential shapes, private keys, environment files and oversized/runtime artifacts, including research notes.
- One branch/spec/area scope, tracker updates, owning spec updates for production changes.
- Declared contract documents and consumers updated in the candidate change.
- Existing approval references for implementation, schema and UI changes.
- Known overlapping unmerged commits in other remote branches.
- Registered verification/security commands for changed production areas in branch mode.

## Activate for a real project

Generated projects are 100 percent project-owned: their own `AGENTS.md`, `README.md`, `planning/` brief/tracker/specs, and verification commands from their own specs. The steps below apply to this workflow repo itself.

1. Ask what the user is creating (no fixed list): `python3 scripts/configure.py --name my-project` or `--existing /path/to/app`. `--areas` / `--stack` are free text.
2. Complete and approve planning; record its actual version in the approval register.
3. Fill `planning_approval` and real per-area commands in the repo's gated-branch config (`.baseline/project.json` where used).
4. Set phase to `implementation` only for approved product work.
5. Update the change manifest on each new feature branch: owning area/spec, summary, contract/schema/UI flags, approval references, required synchronized paths.
6. Initialize Git in your new project copy and run `npm install` from the root to install Husky (`husky` in `package.json`) and activate hooks. Commit the lockfile once generated.
7. Customize the CI workflow to provision your runtimes and isolated test services before registered commands run. Change its default-branch trigger if your default is not `main`.
8. Configure repository branch protection to require these checks and human review. These account settings are not activated by local files.

A command entry is an argument array executed without a shell:

```json
{
  "checks": [["npm", "run", "lint"], ["npm", "test"]],
  "security": [["npm", "audit", "--audit-level=high"]]
}
```

This is a syntax example, not a universal security policy. Use commands that apply to the target stack. A command that merely prints success is not evidence. CI must keep untrusted PR jobs isolated and without secrets.

## Bootstrap and partial staging

An unborn repository may commit the initial planning/template snapshot once. Production code is forbidden in that exception. After that, use a named branch matching the change manifest (`feature/<area>/<NN>-<slug>`, `fix/`, or `docs/`; root area is `root`).

The staged gate reads file contents from the index. Every changed candidate needs its owning tracker; a production change also needs its owning spec updated.

## Limits requiring human judgment

The gate does not prove every consumer is declared, a contract is semantically compatible, an approval is genuine, an API exists, a regex scanner finds every secret, or a branch with no shared remote refs was never stacked. It checks inline Markdown paths, not remote links, anchor validity, full Markdown lint or full YAML schema conformance. Add stack-specific tools when needed.

The optional CodeRabbit app, live GitHub CI, branch protection and production environments are not provisioned by this template. Do not report them as active until independently verified.

The first planning/template commit may also be pushed from the default branch when no remote default ref exists locally and HEAD has exactly one commit. This bootstrap exception never permits production source. Later pushes require normal feature scope and a fetched comparison ref.

The pre-push wrapper also validates Git's proposed ref updates: the current HEAD must target the matching branch name. It rejects feature-to-main refspecs, other commits, tags and deletion operations from this feature hook.
