#!/usr/bin/env python3
"""Start a new project or plug into an existing one.

Everything this script writes into a target project is project-owned:
a project-specific AGENTS.md, README.md with a file index, a project-kit
(context plus feature specs), and — when areas are given — one folder per
layer, each with its own AGENTS.md, README.md index, and planning kit.
Nothing references this workflow, no START-HERE, no .baseline/ directory,
no manifests or dependencies at the root — runtime files are decided
by the project's own feature specs and executed by the AI agent.

New project:
  python3 scripts/configure.py --name my-project

New project with free-form description:
  python3 scripts/configure.py --name my-project --areas "web app, python api" --stack "python, sqlite" --target ~/Projects/Workflows/my-project

Plug into an existing codebase (never overwrites):
  python3 scripts/configure.py --existing /path/to/existing-app --name existing-app --areas "app, api, db"

A shared knowledge base lives OUTSIDE every target at
<home>/Projects/Workflows/my-knowledge-base, next to the generated projects.
It is created ONCE for a first-time user; later runs reuse it untouched.
A small registry entry under
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
    # One permanent home, in the same folder as the generated projects:
    # <home>/Projects/Workflows/my-knowledge-base.
    # Neutral name — each user owns theirs; nothing private is ever read or copied.
    # Created ONCE for a first-time user; later runs reuse it untouched.
    # BASELINE_KB_HOME overrides for testing or custom placement.
    import os
    override = os.environ.get("BASELINE_KB_HOME")
    if override:
        return Path(override).expanduser()
    return workflows_home() / "my-knowledge-base"


def registry_home() -> Path:
    return workflows_home() / ".registry"


def slug_ok(s: str) -> bool:
    return bool(re.fullmatch(r'[a-z0-9][a-z0-9-]*', s or ''))


def slugify(s: str) -> str:
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', (s or '').lower())).strip('-')


def parse_areas(areas: str) -> list:
    return [a.strip() for a in (areas or "").split(",") if a.strip()]


def ask(prompt: str, default: str = "") -> str:
    suffix = " [" + default + "]" if default else ""
    try:
        v = input(prompt + suffix + ": ").strip()
    except EOFError:
        v = ""
    return v or default


def kb_agents_md() -> str:
    return (
        "# Agent instructions — shared knowledge base\n"
        + "\n"
        + "## What this is\n"
        + "\n"
        + "Reusable engineering judgment shared by ALL projects: how to choose, why an\n"
        + "approach works, when it fails, and how to verify it. Project decisions live\n"
        + "in their projects; only distilled, reusable lessons live here. Never store\n"
        + "project secrets, customer data, names, identifiers, or internal URLs here.\n"
        + "\n"
        + "## How to populate it (after every project or discovery)\n"
        + "\n"
        + "1. Pick one recurring question (start with `STARTER-TOPICS.md`, top-down).\n"
        + "2. Write one short note per question: precise question, short answer,\n"
        + "   situations where it applies, alternatives and counterexamples, current\n"
        + "   sources with version/date, a small verification exercise, open uncertainty,\n"
        + "   and a last-reviewed date.\n"
        + "3. File it by topic: `core/` (architecture, security, testing principles),\n"
        + "   `engineering/` (APIs, data, state, delivery), `decisions/` (adopted working\n"
        + "   preferences and exceptions). Raw captures go in `sources/`; unverified ideas\n"
        + "   wait in `inbox/` until reviewed.\n"
        + "4. Revisit a note when a dependency changes, an experiment fails, or a project\n"
        + "   exposes a counterexample. Update the recommendation in place, record what\n"
        + "   changed and why, and mark the old decision superseded — never leave two\n"
        + "   contradictory instructions active.\n"
        + "5. Push this folder as its own repository after every update so all projects\n"
        + "   share the improved base.\n"
        + "\n"
        + "## How projects use it\n"
        + "\n"
        + "Consult by topic; never bulk-import. Distill project specifics out before\n"
        + "bringing a lesson here.\n"
    )


def ensure_shared_kb() -> Path:
    # Create-once: a first-time user gets the seeded base (format, structure,
    # starter topics, and the populating guide above); every later run finds it
    # already there and leaves it untouched — never recreated, never reseeded,
    # never placed inside a generated project.
    kb = shared_kb_home()
    if (kb / "README.md").exists():
        return kb
    kb.mkdir(parents=True, exist_ok=True)
    for sub in ("sources", "inbox", "core", "engineering", "decisions", "meta"):
        (kb / sub).mkdir(exist_ok=True)
    (kb / "AGENTS.md").write_text(kb_agents_md(), encoding="utf-8")
    starter = TEMPLATE_ROOT / "research" / "knowledge-base" / "README.md"
    intro = starter.read_text(encoding="utf-8") if starter.exists() else "# Knowledge base\n"
    (kb / "README.md").write_text(
        intro
        + "\n\n---\n\n## This shared copy\n\n"
        + "This directory is the reusable master knowledge base for ALL projects.\n"
        + "It lives OUTSIDE any single target project, next to the generated projects,\n"
        + "so new, existing, legacy, monorepo, and multi-repo projects can all read it.\n\n"
        + "- Created once; later runs reuse it untouched. Push it as its own repo.\n"
        + "- How to populate it: read `AGENTS.md` in this folder.\n"
        + "- Keep project secrets/customer data OUT of here; distill reusable lessons only.\n",
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


def root_tracker_md() -> str:
    return (
        "# Progress tracker — root coordination\n"
        + "\n"
        + "The most important file after the brief. The execution chain picks the next\n"
        + "spec; the status board is the delivery truth. Update both in the same branch.\n"
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
        + "Fill the product context, then spec 01.\n"
    )


def layer_tracker_md(layer: str) -> str:
    return (
        "# Progress tracker — " + layer + " layer\n"
        + "\n"
        + "This layer's execution chain and delivery truth. The root tracker chains the\n"
        + "layers; this file chains this layer's specs. Update both in the same branch.\n"
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
        + "| 01 | Layer foundation | PLANNED | Not run | OPEN |\n"
        + "\n"
        + "## 2. In flight\n"
        + "\n"
        + "None yet.\n"
        + "\n"
        + "## 3. Verification and deviations\n"
        + "\n"
        + "Not run. This layer's own commands only — never another layer's gates.\n"
    )


def product_context_md(name: str, areas: list, stack: str) -> str:
    areas_line = ", ".join(areas) if areas else "FILL IN"
    stack_line = stack or "FILL IN"
    return (
        "# Product context — " + name + "\n"
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


def system_map_md(areas: list, layer_slugs: list, links: list) -> str:
    lines = (
        "# System map\n"
        + "\n"
        + "Status: DRAFT. Who owns what. Amend when responsibility moves.\n"
        + "\n"
        + "## Layers\n"
        + "\n"
    )
    if layer_slugs:
        for slug, area in zip(layer_slugs, areas):
            lines += "- `" + slug + "/` — " + area + " (own AGENTS.md, README.md index, project kit)\n"
    else:
        lines += "Single app: everything lives in this root — no layer subfolders. Split into\nlayer folders only for a real ownership or deployment reason; each new layer gets\nits own AGENTS.md, README.md index, and project kit, linked here.\n"
    if links:
        lines += "\n## Linked repositories\n\n"
        for link in links:
            lines += "- `" + link + "` — separate repo; communicate only through interface contracts.\n"
    lines += (
        "\n"
        + "## Data and trust flow\n"
        + "\n"
        + "Actors, entrypoints, trust boundaries, data stores, external providers.\n"
        + "Who authorizes each write. Link canonical contracts, don't repeat payloads.\n"
    )
    return lines


def stack_contract_md(stack: str) -> str:
    return (
        "# Stack contract\n"
        + "\n"
        + "Status: DRAFT. Approved technologies and constraints. Decided by feature\n"
        + "specs; this file records the decision, it doesn't invent it.\n"
        + "\n"
        + "Current: " + (stack or "FILL IN") + "\n"
        + "\n"
        + "## Rules\n"
        + "\n"
        + "- Runtime files (manifests, lockfiles, containers, migrations) are created\n"
        + "  only when a feature spec orders them, with that spec's commands.\n"
        + "- Verification commands per layer are recorded in specs and trackers.\n"
    )


def integration_contracts_md() -> str:
    return (
        "# Integration contracts\n"
        + "\n"
        + "Status: EMPTY. Canonical contract records live in `docs/contracts/`.\n"
        + "\n"
        + "## Registry\n"
        + "\n"
        + "| Contract ID | Owner | Canonical document | Consumers | Compatibility/version |\n"
        + "|---|---|---|---|---|\n"
        + "| None yet | To decide | Create after discovery | To identify | To decide |\n"
        + "\n"
        + "## Change procedure\n"
        + "\n"
        + "Owner plus consumer docs update in the same branch, with compatibility and\n"
        + "rollback tests. Keep retired values only in clearly historical records.\n"
    )


def code_standards_md(stack: str) -> str:
    return (
        "# Code standards\n"
        + "\n"
        + "Status: DRAFT. What makes a change acceptable in this project"
        + (" (" + stack + ")" if stack else "")
        + ": formatting, lint, tests, review bar.\n"
        + "Adopt the existing codebase's standards for plugged-in projects.\n"
    )


def spec_shell_md(kind: str) -> str:
    return (
        "# 01 — Foundation (" + kind + ")\n"
        + "\n"
        + "Status: DRAFT. First independently reviewable outcome. The AI executes this\n"
        + "spec; it owns every runtime file it needs.\n"
        + "\n"
        + "## Outcome\n"
        + "\n"
        + "FILL IN: concrete user-visible result.\n"
        + "\n"
        + "## Dependencies\n"
        + "\n"
        + "FILL IN: what must exist first (spec IDs, contracts, approvals).\n"
        + "\n"
        + "## Setup and initialization\n"
        + "\n"
        + "FILL IN: official scaffold commands if any (run into temp/fresh folders,\n"
        + "merge without overwriting project files). Runtime files this spec creates.\n"
        + "\n"
        + "## Files owned and separation of concerns\n"
        + "\n"
        + "FILL IN: paths this spec owns; what stays untouched.\n"
        + "\n"
        + "## Verification\n"
        + "\n"
        + "FILL IN: this layer's own commands and expected results. Never another\n"
        + "layer's gates.\n"
        + "\n"
        + "## Acceptance criteria\n"
        + "\n"
        + "- [ ] FILL IN binary pass/fail checks.\n"
    )


def project_agents_md(name: str, areas: list, stack: str, kb: str, layer_slugs: list, links: list) -> str:
    areas_line = ", ".join(areas) if areas else "to be defined during planning"
    stack_line = stack or "to be decided during planning; the project's feature specs own this choice"
    out = (
        "# Agent instructions — " + name + "\n"
        + "\n"
        + "## What this project is\n"
        + "\n"
        + "Areas: " + areas_line + ".\n"
        + "Stack / conventions: " + stack_line + ".\n"
        + "Adopt this project's existing folders, language, and standards as-is.\n"
        + "Never restructure source to match an outside scaffold.\n"
        + "Shared lessons live at `" + kb + "` — consult by topic, never commit secrets there.\n"
        + "\n"
        + "## Reading order\n"
        + "\n"
        + "1. The user's current request.\n"
        + "2. `project-kit/context/product-context.md` — problem, users, scope, constraints.\n"
        + "3. `project-kit/context/progress-tracker.md` — section 0 execution chain gives the next spec.\n"
        + "   In a layered project also read each layer's own tracker (see below).\n"
        + "4. The owning spec under `project-kit/feature-specs/` (or the layer's kit) plus every file it names.\n"
        + "5. This project's own source, configs, and tests as-is.\n"
        + "\n"
        + "## Architecture: single app, monorepo, or multi-repo\n"
        + "\n"
        + "Each project has its own architecture — single app, monorepo, or multi-repo.\n"
        + "Follow the brief and specs; never impose one shape on another.\n"
        + "\n"
        + "- Single app: everything lives in this root — no layer subfolders. Do NOT\n"
        + "  create one folder per area for a single app; the project IS this root.\n"
        + "  A second folder appears only for a real second deployable layer.\n"
        + "- Monorepo (several areas in this folder): organize each layer into its own\n"
        + "  folder. Every layer gets its own `AGENTS.md` (that layer's areas, stack,\n"
        + "  commands), its own `README.md` (what the layer is about, an index of every\n"
        + "  file with what each does and how to upgrade it), and its own project kit\n"
        + "  (brief slice, specs, progress tracker). This root file links every layer\n"
        + "  file; layers reference the root instead of duplicating its decisions.\n"
        + "- Multi-repo: the same pattern, except each layer lives in its own\n"
        + "  repository at its accurate location. Repos reference each other by location\n"
        + "  plus interface contracts, and communicate only through those contracts.\n"
        + "- Progress trackers are the most important thing: the root tracker chains\n"
        + "  the layers and their specs, each layer tracker chains its own specs.\n"
        + "  Update the owning tracker plus every affected tracker in the same branch.\n"
        + "- Hard gates run per layer only: a layer's checks, tests, and pre-push gates\n"
        + "  run for that layer's changes. Never run another layer's gates while working\n"
        + "  in this one.\n"
    )
    if len(layer_slugs) > 1:
        out += "\n## Layers in this project\n\n"
        for slug, area in zip(layer_slugs, areas):
            out += ("- `" + slug + "/` — " + area + ": [" + slug + "/AGENTS.md](" + slug + "/AGENTS.md), "
                    + "[" + slug + "/README.md](" + slug + "/README.md), "
                    + "[tracker](" + slug + "/project-kit/context/progress-tracker.md)\n")
    if links:
        out += "\n## Linked repositories\n\n"
        for link in links:
            out += "- `" + link + "` — separate repo, accurate location; talk only via contracts.\n"
    out += (
        "\n"
        + "## Official scaffolds sit WITH the structure, never over it\n"
        + "\n"
        + "When a project or layer starts from an official command (for example\n"
        + "a Next.js, Vue, React Native, or Python starter, or any official install\n"
        + "link), that command must NOT destroy or overwrite the folder structure\n"
        + "already here — not `AGENTS.md`, not the project kits, not any folder.\n"
        + "Scaffold into an empty temp dir or a fresh subfolder, then arrange everything\n"
        + "to fit: every existing file stays, and the official folder structure stays\n"
        + "valid. Lose no file, compromise neither structure.\n"
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
        + "5. Update the owning tracker plus every affected tracker in the same branch.\n"
        + "6. No destructive commands without explicit approval. Commands needing\n"
        + "   elevated rights: print them, ask, and wait.\n"
        + "7. Report when done: what changed, verification evidence, open items,\n"
        + "   and anything needed from the user as numbered copy-run steps. Then wait\n"
        + "   for explicit approval before the next spec.\n"
    )
    return out


def layer_agents_md(name: str, layer: str, slug: str, stack: str) -> str:
    return (
        "# Agent instructions — " + layer + " layer (" + name + ")\n"
        + "\n"
        + "## What this layer is\n"
        + "\n"
        + layer + ". Stack / conventions: " + (stack or "decided by this layer's specs") + ".\n"
        + "See the root `AGENTS.md` and `project-kit/` for project-wide decisions;\n"
        + "this file owns only this layer. `README.md` next to this file indexes every\n"
        + "file in this layer.\n"
        + "\n"
        + "## Read first\n"
        + "\n"
        + "1. Root `AGENTS.md`, `project-kit/context/product-context.md`, root tracker.\n"
        + "2. `" + slug + "/project-kit/context/progress-tracker.md` — this layer's chain.\n"
        + "3. The owning spec plus this layer's source, configs, and tests as-is.\n"
        + "\n"
        + "## Rules\n"
        + "\n"
        + "- One spec per branch; update this layer's tracker plus the root tracker.\n"
        + "- Verify with this layer's own commands only — never another layer's gates.\n"
        + "- Official scaffolds merge in without overwriting this kit or any file.\n"
        + "- Report with evidence; wait for approval before the next spec.\n"
    )


def index_table(rows: list) -> str:
    out = "| File | What it does | How to upgrade it |\n|---|---|---|\n"
    for path, what, upgrade in rows:
        out += "| `" + path + "` | " + what + " | " + upgrade + " |\n"
    return out


def project_readme_rows(name: str, layer_slugs: list, areas: list) -> list:
    rows = [
        ("AGENTS.md", "Agent rules for this project", "Edit in place when responsibilities move"),
        ("README.md", "This index", "Add a row per new top-level file or layer"),
        ("project-kit/context/product-context.md", "Problem, users, scope, success", "Fill during planning; ADRs promote findings"),
        ("project-kit/context/system-map.md", "Layer ownership and data flow", "Amend when responsibility moves"),
        ("project-kit/context/stack-contract.md", "Approved stack and constraints", "Updated only by approved specs"),
        ("project-kit/context/integration-contracts.md", "Contract registry", "Add a row per new contract"),
        ("project-kit/context/code-standards.md", "Acceptance bar for changes", "Tighten with reason, link the decision"),
        ("project-kit/context/progress-tracker.md", "Execution chain and delivery truth", "Update in the same branch, always"),
        ("project-kit/feature-specs/01-foundation.md", "First spec; owns its runtime files", "New specs take the next free ID"),
        ("docs/contracts/README.md", "Canonical interface records", "One record per contract, versioned"),
        ("docs/decisions/README.md", "Why consequential choices were made", "One record per decision, dated"),
        ("research/project-brief.md", "Raw intake before it becomes context", "Promote answers into product-context"),
        ("bugs/INDEX.md", "Defect log with regression proof", "One entry per bug, sanitized evidence"),
    ]
    for slug, area in zip(layer_slugs, areas):
        rows.append((slug + "/", area + " layer: own AGENTS.md, README.md index, project kit",
                     "See " + slug + "/README.md"))
    return rows


def layer_readme_rows(slug: str, layer: str) -> list:
    return [
        (slug + "/AGENTS.md", "Agent rules for the " + layer + " layer", "Edit when layer ownership moves"),
        (slug + "/README.md", "This layer index", "Add a row per new file; app files get rows too"),
        (slug + "/project-kit/context/progress-tracker.md", "This layer's chain and delivery truth",
         "Update with the root tracker in the same branch"),
        (slug + "/project-kit/feature-specs/01-foundation.md", "This layer's first spec",
         "New specs take the next free ID; record layer-only commands"),
    ]


def project_readme_md(name: str, areas: list, stack: str, layer_slugs: list) -> str:
    areas_line = ", ".join(areas) if areas else "to be defined"
    stack_line = stack or "to be decided in planning"
    return (
        "# " + name + "\n"
        + "\n"
        + "Areas: " + areas_line + ". Stack: " + stack_line + ".\n"
        + "\n"
        + "## Work here\n"
        + "\n"
        + "1. Read `AGENTS.md`, then `project-kit/context/product-context.md`.\n"
        + "2. Check `project-kit/context/progress-tracker.md` for the next spec.\n"
        + "3. Implement one spec per branch; verify with this project's own commands.\n"
        + "\n"
        + "## File index\n"
        + "\n"
        + index_table(project_readme_rows(name, layer_slugs, areas))
    )


def layer_readme_md(name: str, layer: str, slug: str, stack: str) -> str:
    return (
        "# " + layer + " layer (" + name + ")\n"
        + "\n"
        + "Stack: " + (stack or "decided by this layer's specs") + ".\n"
        + "Official scaffold output lives here once a spec orders it; this kit stays.\n"
        + "\n"
        + "## File index\n"
        + "\n"
        + index_table(layer_readme_rows(slug, layer))
        + "\n"
        + "App files added later (by spec or official scaffold) each get a row above:\n"
        + "what the file does, and how to upgrade it without breaking the layer.\n"
    )


def scaffold_files(name: str, areas: list, stack: str, kb: Path, layer_slugs: list, links: list) -> dict:
    multi = len(layer_slugs) > 1
    if not multi:
        layer_slugs = []
    files = {
        "AGENTS.md": project_agents_md(name, areas, stack, str(kb), layer_slugs, links),
        "project-kit/context/product-context.md": product_context_md(name, areas, stack),
        "project-kit/context/system-map.md": system_map_md(areas, layer_slugs, links),
        "project-kit/context/stack-contract.md": stack_contract_md(stack),
        "project-kit/context/integration-contracts.md": integration_contracts_md(),
        "project-kit/context/code-standards.md": code_standards_md(stack),
        "project-kit/context/progress-tracker.md": root_tracker_md(),
        "project-kit/feature-specs/01-foundation.md": spec_shell_md("root"),
        "docs/contracts/README.md": "# Contracts\n\nCanonical interface records. One dated record per contract.\n",
        "docs/decisions/README.md": "# Decisions\n\nWhy consequential choices were made. One dated record per decision.\n",
        "research/project-brief.md": "# Project brief — " + name + "\n\nRaw intake. Promote answers into `project-kit/context/product-context.md`.\n",
        "bugs/INDEX.md": "# Bug index\n\n| ID | Summary | State | Regression proof |\n|---|---|---|---|\n",
    }
    for slug, area in zip(layer_slugs, areas):
        files[slug + "/AGENTS.md"] = layer_agents_md(name, area, slug, stack)
        files[slug + "/README.md"] = layer_readme_md(name, area, slug, stack)
        files[slug + "/project-kit/context/progress-tracker.md"] = layer_tracker_md(area)
        files[slug + "/project-kit/feature-specs/01-foundation.md"] = spec_shell_md(area)
    files["README.md"] = project_readme_md(name, areas, stack, layer_slugs)
    return files


def write_new_project(dest: Path, name: str, areas: list, stack: str, kb: Path, links: list) -> list:
    if dest.exists() and any(dest.iterdir()):
        raise SystemExit("Refusing to write into non-empty directory: " + str(dest))
    dest.mkdir(parents=True, exist_ok=True)
    layer_slugs = [slugify(a) for a in areas]
    written = []
    for rel, content in scaffold_files(name, areas, stack, kb, layer_slugs, links).items():
        p = dest / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        written.append(rel)
    return written


def plug_existing(target: Path, name: str, areas: list, stack: str, kb: Path, links: list) -> list:
    # Never overwrite project files: only missing starters are created.
    layer_slugs = [slugify(a) for a in areas]
    written = []
    for rel, content in scaffold_files(name, areas, stack, kb, layer_slugs, links).items():
        if rel == "README.md" and (target / rel).exists():
            continue
        p = target / rel
        if p.exists():
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        written.append(rel)
    return written


def record_registry(name: str, mode: str, target: Path, areas: list, stack: str, kb: Path, links: list) -> Path:
    registry_home().mkdir(parents=True, exist_ok=True)
    entry = {
        "name": name,
        "mode": mode,
        "target": str(target),
        "areas": areas,
        "stack": stack,
        "knowledge_base": str(kb),
        "links": links,
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
    p.add_argument("--link", action="append", default=[], help="Linked sibling repo location (repeatable, for multi-repo)")
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
        written = plug_existing(target, name, areas, args.stack or "", kb, args.link or [])
        reg = record_registry(name, "existing", target, areas, args.stack or "", kb, args.link or [])
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
    written = write_new_project(dest.resolve(), name, areas, args.stack or "", kb, args.link or [])
    reg = record_registry(name, "new", dest.resolve(), areas, args.stack or "", kb, args.link or [])
    print("Created " + str(len(written)) + " project-owned files in " + str(dest))
    print("No workflow files, manifests, or dependencies were added; feature specs own those.")
    print("Registry entry: " + str(reg))
    return 0


if __name__ == "__main__":
    sys.exit(main())
