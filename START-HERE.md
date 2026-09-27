# Start here — new or existing projects (no fixed list)

This template adapts to what YOU are creating. There is no required
`--systems backend,web,infra,qa` list. Describe your project in your own words;
the agent adopts your folders, language, and coding standards.

Default locations (any OS — Windows, macOS, Linux):

- Workflow home: `~/Projects/Workflows/` (`Path.home() / "Projects" / "Workflows"`)
- This template master: stays clean, e.g. `~/Projects/Workflows/baseline`
- New projects: `~/Projects/Workflows/<your-slug>/`
- Shared knowledge base (OUTSIDE every target): `~/Projects/Workflows/knowledge-base/`

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

Then in the NEW copy: fill `research/project-brief.md`, plan with
`.agents/skills/plan-project/SKILL.md` + `templates/`, record approvals in
`docs/planning/APPROVALS.md`, then:

```sh
git init -b main
npm install
python3 scripts/check.py --mode template
```

## Path B — existing / legacy project plug-in (most important)

Do not copy the template over your code. From the template folder:

```sh
python3 scripts/configure.py --existing /path/to/existing-app --name existing-app --areas "app, api, db"
```

This writes ONLY `.baseline/project.json` + `BASELINE-HANDOFF.md` into the target.
No source, config, or tooling is overwritten. Then open the TARGET project and
tell your agent: "Follow baseline `AGENTS.md` path B. Inspect this repo as-is,
adopt its coding standards, and generate only missing planning artefacts."

Ask the user for real lint/test/security commands and record them in the target
`.baseline/project.json` before implementation.

## Knowledge base — why it matters and how to keep it

`research/knowledge-base/` is the starter; the MASTER lives at
`~/Projects/Workflows/knowledge-base/`, outside every target, so all projects
(new, legacy, monorepo, microservices) read from one place.

Why: projects end, judgment compounds. Distilled notes (problem, options,
trade-offs, verification, when it fails) save re-research and stop repeating
failures. A project kit holds one project's decisions; the KB holds reusable
reasoning across projects.

Export it as its own repo so it has independent history:

```sh
cd ~/Projects/Workflows/knowledge-base
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
