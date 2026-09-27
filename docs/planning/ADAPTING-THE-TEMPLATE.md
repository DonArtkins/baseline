# Adapt the template to the project

Baseline imposes no fixed structure. Keep the target's folders, language, and
standards as-is. There is no fixed `--systems` list — `scripts/configure.py`
takes free-form `--areas` / `--stack` (e.g. `--areas "mobile app"`,
`"web + python api"`, `"legacy cleanup"`).

## Small projects

Use only what the target needs. Do not invent an API, database, AI agent, or
mobile app just because a reference kit exists. Fill one root kit plus enough
local context to decide clearly.

## Large projects

Split by real ownership and deployment boundaries. The root kit coordinates;
each area owns its context, specs, verification, and tracker. More files are
justified by distinct topics and readers, not a fixed count. Monorepos and
separate service repos are both supported — never restructure just to match the
template.

## Rename or add an area

Name it in the target's own words in `.baseline/project.json` (`areas` list,
created per target by `configure.py`). Update the system map, AGENTS routing,
and affected links. No checker registry change is needed — `scripts/check.py`
discovers `*/AGENTS.md` kits dynamically and accepts free-form areas.

## Default branch

Set `default_branch`/`remote` in the target's `.baseline/project.json`, update
the CI push trigger and examples, and fetch the actual remote ref before branch
checks.

## Decide what to retain

Keep planning, contract, and evidence rules that protect real boundaries. Mark
inapplicable schema, UI, container, or release sections with a reason. Do not
manufacture migrations or deployables to fill templates.
