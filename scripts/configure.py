#!/usr/bin/env python3
"""Start a new project or plug into an existing one.

Everything this script writes into a target project is project-owned:
a project-specific AGENTS.md, README.md, and planning/ starter files.
Nothing references this workflow, no START-HERE, no .baseline/ directory,
no package.json / package-lock / node_modules — runtime files are decided
by the project's own feature specs and executed by the AI agent.

New project:
  python3 scripts/configure.py --name my-project

New project with free-form description:
  python3 scripts/configure.py --name my-project --areas "web app, python api" --stack "python, sqlite" --target ~/Projects/Workflows/my-project

Plug into an existing codebase (never overwrites):
  python3 scripts/configure.py --existing /path/to/existing-app --name existing-app --areas "app, api, db"

A shared knowledge base lives OUTSIDE every target at
<home>/Projects/Workflows/knowledge-base. A small registry entry under
<home>/Projects/Workflows/.registry/ remembers the linkage; the target
itself stays 100 percent project-owned.
"""
import argparse
import json
from datetime import date
from pathlib import Path
import re
import sys

TEMPLATE_ROOT = Path(__file__).resolve().parents[1]


def workflows_home() -> Path:
    return Path.home() / "Projects" / "Workflows"


def shared_kb_home() -> Path:
    return workflows_home() / "knowledge-base"


def registry_home() -> Path:
    return workflows_home() / ".registry"


def slug_ok(s: str) -> bool:
    return bool(re.fullmatch(r'[a-z0-9][a-z0-9-]*', s or ''))


def parse_areas(areas: str) -> list:
    return [a.strip() for a in (areas or "").split(",") if a.strip()]


def ask(prompt: str, default: str = "") -> str:
    suffix = " [" + default + "]" if default else ""
    try:
        v = input(prompt + suffix + ": ").strip()
    except EOFError:
        v = ""
    return v or default


def ensure_shared_kb() -> Path:
    kb = shared_kb_home()
    kb.mkdir(parents=True, exist_ok=True)
    for sub in ("sources", "inbox", "core", "engineering", "decisions", "meta"):
        (kb / sub).mkdir(exist_ok=True)
    readme = kb / "README.md"
    if not readme.exists():
        starter = TEMPLATE_ROOT / "research" / "knowledge-base" / "README.md"
        intro = starter.read_text(encoding="utf-8") if starter.exists() else "# Knowledge base\n"
        readme.write_text(
            intro
            + "\n\n---\n\n## This shared copy\n\n"
            + "This directory is the reusable master knowledge base for ALL projects.\n"
            + "It lives OUTSIDE any single target project so new, existing, legacy,\n"
            + "monorepo, and microservice projects can all read from it.\n\n"
            + "- Keep project secrets/customer data OUT of here; distill reusable lessons only.\n"
            + "- Push this folder as its own GitHub repo and pull/update it from each project.\n"
            + "- Suggested remote name: knowledge-base (private repo if notes contain internal judgment).\n",
            encoding="utf-8",
        )
        src_dir = TEMPLATE_ROOT / "research" / "knowledge-base"
        if src_dir.exists():
            for f in src_dir.glob("*.md"):
                dest = kb / f.name
                if not dest.exists():
                    import shutil
                    shutil.copy(f, dest)
    return kb


def project_agents_md(name: str, areas: list, stack: str) -> str:
    areas_line = ", ".join(areas) if areas else "to be defined during planning"
    stack_line = stack or "to be decided during planning; the project's feature specs own this choice"
    return (
        "# Agent instructions — " + name + "\n"
        + "\n"
        + "## What this project is\n"
        + "\n"
        + "Areas: " + areas_line + ".\n"
        + "Stack / conventions: " + stack_line + ".\n"
        + "Adopt this project's existing folders, language, and standards as-is.\n"
        + "Never restructure source to match an outside scaffold.\n"
        + "\n"
        + "## Reading order\n"
        + "\n"
        + "1. The user's current request.\n"
        + "2. `planning/project-brief.md` — problem, users, scope, constraints.\n"
        + "3. `planning/progress-tracker.md` — section 0 execution chain gives the next spec.\n"
        + "4. The owning spec under `planning/specs/` plus every file it names.\n"
        + "5. This project's own source, configs, and tests as-is.\n"
        + "\n"
        + "## Working rules\n"
        + "\n"
        + "1. Plan before code: reviewable spec plus binary acceptance criteria first.\n"
        + "2. One spec, one branch, one review: `feature/<area>/<NN>-<slug>` from the\n"
        + "   fetched default branch tip (`fix/` for bugs, `docs/` for planning-only).\n"
        + "3. Implement exactly what the spec says. Runtime files (manifests,\n"
        + "   dependencies, migrations, containers) are created only when a feature\n"
        + "   spec orders them, using that spec's commands — never speculatively.\n"
        + "4. Verify with this project's own commands (recorded in the spec/tracker),\n"
        + "   and report exact output: pass/fail/skip counts, revision, limits.\n"
        + "5. Update `planning/progress-tracker.md` in the same branch before review.\n"
        + "6. No destructive commands without explicit approval. Commands needing\n"
        + "   elevated rights: print them, ask, and wait.\n"
        + "7. Report when done: what changed, verification evidence, open items,\n"
        + "   and anything needed from the user as numbered copy-run steps. Then wait\n"
        + "   for explicit approval before the next spec.\n"
    )


def project_readme_md(name: str, areas: list, stack: str) -> str:
    areas_line = ", ".join(areas) if areas else "to be defined"
    stack_line = stack or "to be decided in planning"
    return (
        "# " + name + "\n"
        + "\n"
        + "Areas: " + areas_line + ".\n"
        + "Stack: " + stack_line + ".\n"
        + "\n"
        + "## Work here\n"
        + "\n"
        + "1. Read `AGENTS.md`, then `planning/project-brief.md`.\n"
        + "2. Check `planning/progress-tracker.md` for the next spec.\n"
        + "3. Implement one spec per branch; verify with this project's own commands.\n"
    )


def project_brief_md(name: str, areas: list, stack: str) -> str:
    areas_line = ", ".join(areas) if areas else "FILL IN"
    stack_line = stack or "FILL IN"
    return (
        "# Project brief — " + name + "\n"
        + "\n"
        + "Status: DRAFT. Fill this in; unknowns stay open questions, not inventions.\n"
        + "\n"
        + "## Problem\n"
        + "\n"
        + "What happens today, who is affected, and what evidence shows it matters.\n"
        + "\n"
        + "## Areas\n"
        + "\n"
        + areas_line + "\n"
        + "\n"
        + "## Stack / conventions\n"
        + "\n"
        + stack_line + "\n"
        + "\n"
        + "## Users and journeys\n"
        + "\n"
        + "Three concrete journeys: actor, start state, action, success, failure, permissions.\n"
        + "\n"
        + "## Scope\n"
        + "\n"
        + "First-release outcomes, explicit exclusions, later possibilities.\n"
        + "\n"
        + "## Success\n"
        + "\n"
        + "Observable outcomes and how they will be measured.\n"
    )


def project_tracker_md() -> str:
    return (
        "# Progress tracker\n"
        + "\n"
        + "## 0. Execution chain\n"
        + "\n"
        + "Full chain:\n"
        + "\n"
        + "```text\n"
        + "01\n"
        + "```\n"
        + "\n"
        + "Next:\n"
        + "\n"
        + "```text\n"
        + "01\n"
        + "```\n"
        + "\n"
        + "## 1. Status board\n"
        + "\n"
        + "| ID | Feature | State | Evidence | Operator gates |\n"
        + "|---|---|---|---|---|\n"
        + "| 01 | Foundation | PLANNED | Not run | OPEN |\n"
        + "\n"
        + "## 2. In flight\n"
        + "\n"
        + "None yet.\n"
        + "\n"
        + "## 3. Verification and deviations\n"
        + "\n"
        + "Not run. Record exact commands, revision, pass/fail/skip, and limits here.\n"
        + "\n"
        + "## 4. Next action and history\n"
        + "\n"
        + "Fill the brief, then spec 01.\n"
    )


def write_new_project(dest: Path, name: str, areas: list, stack: str) -> list:
    if dest.exists() and any(dest.iterdir()):
        raise SystemExit("Refusing to write into non-empty directory: " + str(dest))
    dest.mkdir(parents=True, exist_ok=True)
    planning = dest / "planning" / "specs"
    planning.mkdir(parents=True, exist_ok=True)
    written = []
    for rel, content in (
        ("AGENTS.md", project_agents_md(name, areas, stack)),
        ("README.md", project_readme_md(name, areas, stack)),
        ("planning/project-brief.md", project_brief_md(name, areas, stack)),
        ("planning/progress-tracker.md", project_tracker_md()),
    ):
        p = dest / rel
        p.write_text(content, encoding="utf-8")
        written.append(rel)
    return written


def plug_existing(target: Path, name: str, areas: list, stack: str) -> list:
    written = []
    candidates = (
        ("AGENTS.md", project_agents_md(name, areas, stack)),
        ("README.md", project_readme_md(name, areas, stack)),
        ("planning/project-brief.md", project_brief_md(name, areas, stack)),
        ("planning/progress-tracker.md", project_tracker_md()),
    )
    for rel, content in candidates:
        # Never overwrite project files. READMEs almost always exist; the rest
        # are created only when the project does not have them yet.
        if rel == "README.md" and (target / rel).exists():
            continue
        p = target / rel
        if p.exists():
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        written.append(rel)
    return written


def record_registry(name: str, mode: str, target: Path, areas: list, stack: str, kb: Path) -> Path:
    registry_home().mkdir(parents=True, exist_ok=True)
    entry = {
        "name": name,
        "mode": mode,
        "target": str(target),
        "areas": areas,
        "stack": stack,
        "knowledge_base": str(kb),
        "date": date.today().isoformat(),
    }
    dest = registry_home() / (name + ".json")
    dest.write_text(json.dumps(entry, indent=2) + "\n", encoding="utf-8")
    return dest


def main() -> int:
    p = argparse.ArgumentParser(description="Start projects with project-owned files only.")
    p.add_argument("--name", default="")
    p.add_argument("--target", default="")
    p.add_argument("--existing", default="")
    p.add_argument("--areas", default="")
    p.add_argument("--stack", default="")
    args = p.parse_args()

    kb = ensure_shared_kb()

    if not args.existing and not args.name:
        print("What are you creating? (no fixed list — describe it in your own words)")
        mode = ask("New project or plug into existing? [new/existing]", "new").lower()
        if mode.startswith("exist"):
            args.existing = ask("Path to the existing project folder")
            default_slug = Path(args.existing).name.lower().replace("_", "-") if args.existing else ""
            args.name = ask("Project slug for config", default_slug)
            args.areas = ask('Areas/folders you care about (free text, e.g. "app, api, db")')
            args.stack = ask("Stack / coding standards (free text, blank = keep project as-is)")
        else:
            args.name = ask("New project slug (lowercase, dashes)")
            args.areas = ask('What are you building? (free text, e.g. "single mobile app", "web + python api")')
            args.stack = ask("Stack / conventions (free text, blank = decide during planning)")
            args.target = ask("Target folder (blank = ~/Projects/Workflows/<name>)")

    if args.existing:
        target = Path(args.existing).expanduser().resolve()
        if not target.is_dir():
            p.error("existing path is not a directory: " + str(target))
        name = args.name or target.name.lower().replace("_", "-")
        if not slug_ok(name):
            p.error("name must be a lowercase slug")
        areas = parse_areas(args.areas)
        written = plug_existing(target, name, areas, args.stack or "")
        reg = record_registry(name, "existing", target, areas, args.stack or "", kb)
        print("Plugged into existing project: " + str(target))
        if written:
            print("Created project-owned files: " + ", ".join(written))
        else:
            print("Project already had its own files; nothing overwritten.")
        print("Registry entry: " + str(reg))
        return 0

    name = args.name
    if not name or not slug_ok(name):
        p.error("provide --name as a lowercase slug, e.g. my-project")
    dest = Path(args.target).expanduser() if args.target else (workflows_home() / name)
    areas = parse_areas(args.areas)
    written = write_new_project(dest.resolve(), name, areas, args.stack or "")
    reg = record_registry(name, "new", dest.resolve(), areas, args.stack or "", kb)
    print("Created project-owned files in " + str(dest) + ": " + ", ".join(written))
    print("No workflow files, manifests, or dependencies were added; feature specs own those.")
    print("Registry entry: " + str(reg))
    return 0


if __name__ == "__main__":
    sys.exit(main())
