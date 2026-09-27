#!/usr/bin/env python3
"""Flexible baseline setup with no fixed systems list.

The template itself stays clean. This script writes per-project state into
the target project and ensures a shared knowledge base lives OUTSIDE any
single target, by default at <home>/Projects/Workflows/knowledge-base
(works on Windows, macOS, Linux via Path.home()).

New project:
  python3 scripts/configure.py --name my-project

New project with free-form description:
  python3 scripts/configure.py --name my-project --areas "web app, python api" --stack "python, sqlite" --target ~/Projects/Workflows/my-project

Plug into existing / legacy codebase (primary use-case, never overwrites source):
  python3 scripts/configure.py --existing /path/to/existing-app --name existing-app --areas "app, api, db"

Only .baseline/ plus a handoff note are written into the target.
"""
import argparse
import json
import shutil
from pathlib import Path
import re
import sys

TEMPLATE_ROOT = Path(__file__).resolve().parents[1]


def workflows_home() -> Path:
    return Path.home() / "Projects" / "Workflows"


def shared_kb_home() -> Path:
    return workflows_home() / "knowledge-base"


def slug_ok(s: str) -> bool:
    return bool(re.fullmatch(r'[a-z0-9][a-z0-9-]*', s or ''))


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
                    shutil.copy(f, dest)
    return kb


def write_target_baseline(target: Path, name: str, mode: str, areas: str, stack: str, kb_path: Path):
    bdir = target / ".baseline"
    bdir.mkdir(parents=True, exist_ok=True)
    (bdir / "local").mkdir(exist_ok=True)
    proj = {
        "name": name,
        "mode": mode,
        "areas": [a.strip() for a in areas.split(",") if a.strip()] if areas else [],
        "stack": stack or "",
        "phase": "planning",
        "knowledge_base": str(kb_path),
        "default_branch": "main",
        "remote": "origin",
        "notes": "Free-form areas/stack in the target project's own words. No fixed system list is enforced.",
    }
    (bdir / "project.json").write_text(json.dumps(proj, indent=2) + "\n", encoding="utf-8")
    change = {
        "system": "root",
        "spec": "00",
        "summary": "Baseline plug-in initialised",
        "contract_changed": False,
        "schema_changed": False,
        "ui_changed": False,
        "required_docs": [],
        "contract_docs": [],
        "consumer_docs": [],
        "approval_refs": [],
    }
    (bdir / "change.json").write_text(json.dumps(change, indent=2) + "\n", encoding="utf-8")
    handoff = target / "BASELINE-HANDOFF.md"
    if not handoff.exists():
        handoff.write_text(
            "# Baseline handoff — " + name + "\n\n"
            + "Mode: " + mode + "\n\n"
            + "Areas (your words, not a fixed list): " + (areas or "—") + "\n\n"
            + "Stack / conventions: " + (stack or "—") + "\n\n"
            + "Shared knowledge base (outside this project): `" + str(kb_path) + "`\n\n"
            + "Next: open this project with your AI agent. Tell it to read the baseline\n"
            + "AGENTS.md reading order, inspect THIS project's existing folders as-is,\n"
            + "and generate only missing planning artefacts inside this project.\n"
            + "Do not restructure source folders to match the template.\n",
            encoding="utf-8",
        )


def copy_template_to(dest: Path):
    ignore = shutil.ignore_patterns(".git", "node_modules", "__pycache__", ".venv", "dist", "build", ".baseline")
    if dest.exists() and any(dest.iterdir()):
        raise SystemExit("Refusing to copy into non-empty directory: " + str(dest))
    dest.mkdir(parents=True, exist_ok=True)
    for item in TEMPLATE_ROOT.iterdir():
        if item.name in (".git", "node_modules", "__pycache__", ".venv", ".baseline"):
            continue
        d = dest / item.name
        if item.is_dir():
            shutil.copytree(item, d, ignore=ignore, dirs_exist_ok=True)
        else:
            shutil.copy2(item, d)


def main() -> int:
    p = argparse.ArgumentParser(description="Flexible baseline setup (no fixed systems list).")
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
        areas = args.areas or ""
        stack = args.stack or ""
        write_target_baseline(target, name, "existing", areas, stack, kb)
        print("Plugged into existing project: " + str(target))
        print("Shared knowledge base: " + str(kb))
        print("Wrote .baseline/project.json + BASELINE-HANDOFF.md only. No source files touched.")
        return 0

    name = args.name
    if not name or not slug_ok(name):
        p.error("provide --name as a lowercase slug, e.g. my-project")
    dest = Path(args.target).expanduser() if args.target else (workflows_home() / name)
    write_target_baseline_copy = False
    copy_template_to(dest)
    write_target_baseline(dest, name, "new", args.areas or "", args.stack or "", kb)
    print("Created " + str(dest))
    print("Shared knowledge base: " + str(kb))
    print("Fill the brief in the new copy and let the agent plan. Template master is untouched.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
