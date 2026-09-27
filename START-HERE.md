# Start here — new or existing projects (no fixed list)

This template adapts to what YOU are creating. There is no required
`--systems backend,web,infra,qa` list. Describe your project in your own words;
the agent adopts your folders, language, and coding standards.

Default locations (any OS — Windows, macOS, Linux):

- Workflow home: `~/Projects/Workflows/` (`Path.home() / "Projects" / "Workflows"`)
- This template master: stays clean, e.g. `~/Projects/Workflows/baseline`
- New projects: `~/Projects/Workflows/<your-slug>/`
- Shared knowledge base (OUTSIDE every target, created ONCE): `<parent-of-this-repo>/my-knowledge-base/` (e.g. `/home/artkins/Programming/my-knowledge-base/`)

## Path A — new project

```sh
python3 scripts/configure.py --name my-project
```

Without flags it asks: what are you building (`--areas` free text, e.g.
`"single mobile app"`, `"web + python api"`, `"monorepo"`), stack/conventions
(`--stack` free text, blank = decide during planning), and target folder
(blank = `~/Projects/Workflows/my-project`). With flags:

```sh
python3 scripts/configure.py --name my-project --areas "web app, python api" --stack "fastapi, sqlite, pytest" --target ~/Projects/Workflows/my-project
```

Then in the NEW project: fill `planning/project-brief.md`, let the AI plan and spec using that project's own `AGENTS.md`, then:

```sh
git init -b main
```

Runtime files (`package.json`, lockfiles, containers, migrations) are created only when a feature spec orders them — never by the generator. The `npm install` / Husky / `check.py` tooling belongs to this workflow repo, not to generated projects.

## Path B — existing / legacy project plug-in (most important)

Do not copy the template over your code. From the template folder:

```sh
python3 scripts/configure.py --existing /path/to/existing-app --name existing-app --areas "app, api, db"
```

This writes ONLY missing project-owned starter files into the target (its own `AGENTS.md` when it has none, `planning/` starter when absent).
No source, config, or tooling is overwritten; no workflow files, manifests, or dependencies are injected. The linkage is remembered in `~/Projects/Workflows/.registry/<slug>.json`. Then open the TARGET project and
tell your agent: "Follow that project's `AGENTS.md`. Inspect this repo as-is,
adopt its coding standards, and generate only missing planning artefacts."

Ask the user for real lint/test/security commands and record them in the target's specs/tracker before implementation — never in workflow files.

## Knowledge base — why it matters and how to keep it

`research/knowledge-base/` is the starter; the MASTER lives at
`<parent-of-this-repo>/my-knowledge-base/` (e.g. `/home/artkins/Programming/my-knowledge-base/`), outside every target and never inside a generated project,
so all projects (new, legacy, monorepo, microservices) read from one place.
It is created ONCE for a first-time user; later runs find it and skip recreating it.

Why: projects end, judgment compounds. Distilled notes (problem, options,
trade-offs, verification, when it fails) save re-research and stop repeating
failures. A project kit holds one project's decisions; the KB holds reusable
reasoning across projects.

Export it as its own repo so it has independent history:

```sh
cd <parent-of-this-repo>/my-knowledge-base  # e.g. /home/artkins/Programming/my-knowledge-base
git init -b main
git add . && git commit -m "knowledge base seed"
gh repo create knowledge-base --private --source=. --push
```

Keep updating it after each project (what worked, counterexamples, version
changes) and push. `configure.py` creates/links it automatically; agents consult
it by topic, never bulk-import it. Keep secrets and customer data OUT — distill
lessons only. See `research/knowledge-base/README.md`.

## Resume

Read root `AGENTS.md`, the target handoff/brief, owning tracker/spec, and open
bug/review evidence. Use `templates/handoff.md`. For the repeat loop (merge,
clear session, next spec), paste [the master daily implementation prompt](templates/daily-implementation-prompt.md) — it forces skills-first + Context7/MCP current docs (step 0). Full wiring: [skills/MCP/Context7](docs/tooling/SKILLS-MCP-CONTEXT7.md). Consult the shared KB by topic.
