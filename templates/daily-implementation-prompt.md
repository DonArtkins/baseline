# Master daily implementation prompt (copy-paste each session, one feature at a time)

Paste this at the start of a fresh agent session after you have merged the previous feature. It implements exactly ONE next spec, pushes it, reports, then waits. Clear the session after merge and repeat.

```text
Continue implementation for this project using baseline.

0. SKILLS + CURRENT DOCS (do this before anything else):
   - List .agents/skills/ and load the fitting skill(s) for this task
     (plan-project, contract-sync, git-branch-flow, current-docs, etc.).
     If none fits, create one from templates/skill.md first.
   - Always use Context7/MCP to get/install/create skills and to fetch
     current docs for every tool, framework, package, and MCP service we
     use — never answer versioned APIs from memory. Record library,
     version, source, and date in the spec. If Context7/MCP is unreachable,
     say so, fall back to official docs, and mark the claim unverified.
   - Full setup: docs/tooling/SKILLS-MCP-CONTEXT7.md.

1. READ FIRST (in this order, full bodies not filenames):
   - This project's BASELINE-HANDOFF.md (if present) and research/project-brief.md.
   - Root AGENTS.md, then the owning kit AGENTS.md (root, infra/, or qa/).
   - ALL progress trackers: project-kit/context/progress-tracker.md plus
     infra/project-kit/context/progress-tracker.md and
     qa/project-kit/context/progress-tracker.md where they exist.
     Use section 0 Execution chain "Next" to pick the ONE next spec.
     If trackers disagree, stop and ask before coding.
   - The owning feature spec plus every file it names (context, contracts,
     decisions, design refs). When you reach an agent file, read it plus
     every file it points to. Do not start until you have enough context.

2. BRANCH: fetch the remote default branch, then switch to a new branch for
   the new spec from its tip: feature/<area>/<NN>-<slug>
   (fix/<area>/<NN>-<slug> for a bug fix, docs/<area>/<NN>-<slug> for
   planning-only). Never branch from another feature branch. Never commit
   directly to main.

3. IMPLEMENT exactly what the spec and its named files say. Do not add
   scope, do not invent stack or structure, do not reformat unrelated files.
   Exception: a genuine fix may go in only via the contract-sync rule
   (docs/planning/CONTRACT-SYNC.md): update owner + consumer docs in the
   same branch, tell me, and document it in the spec/tracker.

4. RULES: enforce every rule in the AGENTS files after every run, and all
   sync rules (contracts, decisions, docs, tests together). No destructive
   commands (no rm -rf of source, no reset --hard, no drop/migrate-down
   without my explicit go-ahead). Any command needing sudo: print it,
   prompt me for the password, and wait for me to type it before using it.

5. TRACKERS: after the work, update the owning progress tracker AND every
   affected layer's tracker: Execution chain Full/Next fences, status-board
   row, verification section (exact commands, revision, pass/fail/skip,
   limits), and next action. Keep history concise and dated.

6. REVIEW INTAKE: check .coderabbit/reviews/ (and .coderabbit/review.txt
   if present). If there are unaddressed findings, reproduce each, fix
   accepted ones on this same branch, verify, and record disposition with
   templates/review.md. An empty folder/file means nothing to fix.

7. PUSH GATE (root only): from the project root run
   python3 scripts/check.py --mode template and the target's real
   lint/test/security commands, plus the Husky pre-push contract check.
   Tracker must be updated before push. Push only the current feature
   branch to its matching remote ref.

8. REPORT back: what you did, files changed and why, test/gate results
   with counts, open operator gates, deviations, review dispositions, and
   anything YOU need from ME (DB connect, docker, migrations, env keys,
   approvals) as numbered step-by-step commands I can copy-run. Then STOP
   and wait for my explicit approval before touching the next feature.
```

## Why one feature per paste

A cleared session plus this prompt guarantees the agent re-reads the trackers and spec chain instead of coasting on stale context. Merge, clear, paste, implement, push, report, approve — repeat. See [handoff](handoff.md), [branch policy](../docs/planning/BRANCH-POLICY.md), [gates](../docs/tooling/GATES.md), and [review intake](../.coderabbit/README.md).
