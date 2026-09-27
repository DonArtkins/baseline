# baseline

A reusable, planning-first workflow for building software with AI agents. Adapts to
new, existing, legacy, single-app, web, mobile, python, monorepo, or microservice
projects. It does not impose a fixed app scaffold or fixed `--systems` list.

Start with [START-HERE.md](START-HERE.md), follow root [AGENTS.md](AGENTS.md).

## Repository map (permanent template layout)

```text
baseline/
├── AGENTS.md                  Root agent rules + reading order (new vs existing)
├── START-HERE.md              Human onboarding (no fixed list, existing plug-in primary)
├── package.json               Husky hook install (npm install)
├── project-kit/               Cross-area context, specs (reference, fill per target)
├── infra/ qa/                 Optional delivery/test reference kits
├── docs/                      Decisions, contracts, design, operations, planning, tooling
├── research/                  Brief, sources, findings, knowledge-base starter
├── templates/                 Copyable spec, decision, contract, research forms
├── scripts/                   configure.py (free-form) + check.py + tests
├── bugs/                      Reproductions, sanitized evidence
├── inspo/                     Attributed visual references and analysis
├── .agents/skills/            Reusable workflow skills
├── .github/                   CI checks, PR and issue templates
├── .husky/                    Local commit/push entrypoints
└── .coderabbit/               Review intake records
```

No `.baseline/` in the master (workflow-repo-internal gated-branch state only; never generated into projects).
No `backend/ web/ mobile/ ai/ mcp/`, no `prompts/ diagrams/ examples/`.

## Use

- New: `python3 scripts/configure.py --name my-project` (asks what you are building). The new project gets project-owned files only (`AGENTS.md` about that project, `README.md`, `planning/` starter) — no workflow files, no manifests, no dependencies.
- Existing (primary): `python3 scripts/configure.py --existing /path/to/app --name my-app --areas "app, api, db"` — creates only missing project-owned starters, never overwrites, injects nothing.
- Runtime files (`package.json`, lockfiles, containers, migrations) belong to the project's feature specs; the AI creates them when a spec orders it.
- Shared KB (outside every target, created once, never inside projects): `<parent-of-this-repo>/my-knowledge-base/` (e.g. `/home/artkins/Programming/my-knowledge-base/`) — export as its own repo, keep updating. See [START-HERE](START-HERE.md) + [knowledge-base](research/knowledge-base/README.md).

## Check the template

```sh
python3 scripts/check.py --mode template
python3 -m unittest discover -s scripts/tests -v
```

Validates workflow structure only, not a future product.
