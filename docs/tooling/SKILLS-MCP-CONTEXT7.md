# Skills, MCPs, and Context7 — install and force-use guide

This template ships with file-based agent skills. MCP servers (Context7, filesystem, GitHub, etc.) are configured per machine/editor, not committed with secrets. Wire once, reuse everywhere.

## 1. Agent skills (already in this repo)

Location: `.agents/skills/<name>/SKILL.md` (plus `infra/.agents/skills/`, `qa/.agents/skills/`). Each has `name:` + `description:` frontmatter — that is how agents discover them. `scripts/check.py` validates this.

| Skill | Use it when |
|---|---|
| `plan-project` | New/existing project planning pack |
| `contract-sync` | Any interface change (owner + consumers together) |
| `git-branch-flow` | One spec per branch, tracker before push |
| `bug-triage` | Reproduce, fix, regression evidence |
| `research-intake` | Turn sources/video notes into verified findings |
| `documentation-standards` | Keep docs owned and verifiable |
| `design-from-inspo` | References to design system + wireframes |
| `current-docs` | Verify any third-party API against current docs (use with Context7) |
| `review-resolution` | Resolve review findings with evidence |
| `rate-limit-recovery` | Resume throttled sessions without duplicate side effects |

Add a new skill: copy `templates/skill.md` to `.agents/skills/<slug>/SKILL.md`, fill name/description/procedure, run `python3 scripts/check.py --mode template`. Tell the AI: "Check `.agents/skills/` first; if no skill fits, create one from `templates/skill.md` and wire it in."

## 2. MCP servers (one-time per machine)

MCP = tools your agent can call (docs, files, GitHub, DB). Config lives OUTSIDE the repo (it holds paths/keys). Pick your editor:

**VS Code / Cursor** → `<home>/.vscode/mcp.json` or project `.vscode/mcp.json`:
```json
{
  "servers": {
    "context7": { "type": "stdio", "command": "npx", "args": ["-y", "@upstash/context7-mcp"], "env": { "CONTEXT7_API_KEY": "YOUR_KEY" } },
    "filesystem": { "type": "stdio", "command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/YOU/Projects"] }
  }
}
```

**Claude Code** → `claude mcp add context7 -- npx -y @upstash/context7-mcp` (then set `CONTEXT7_API_KEY` in env).
**Codex CLI** → `~/.codex/config.toml`:
```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
```
Never commit real keys. Keep a keyless example in the repo; real keys stay in env/dotfiles.

## 3. Context7 (current docs for your stack)

1. Get a key at the [Context7 repo](https://github.com/upstash/context7) / dashboard.
2. Add the `context7` server above for your editor; restart the agent/IDE.
3. Verify: ask the agent "Use Context7 to fetch the current docs for <package/framework> and cite the version/date." If it answers from memory without a lookup, stop it and repeat the directive below.
4. No key / offline? Fall back to official docs in browser + record the limitation and version/date in the spec (see `current-docs` skill).

## 4. Force the AI to always use them (paste this)

Add to every session along with the daily prompt (`templates/daily-implementation-prompt.md` step 0):

```text
Always use the repo's .agents/skills first (plan-project, contract-sync,
git-branch-flow, current-docs, etc.). If a needed skill is missing, create it
from templates/skill.md. Always use Context7/MCP to get/install/create skills
and to fetch current docs for every tool, framework, package, and MCP service
we use — never answer from memory for versioned APIs. Record library, version,
source, and date in the spec. If Context7/MCP is unreachable, say so, use
official docs, and mark the claim unverified.
```

For permanent memory (Codex `AGENTS.md`, Claude `CLAUDE.md`, Cursor rules), save that paragraph so it loads every session.

## 5. Wired-up checklist

- [ ] `python3 scripts/check.py --mode template` passes (skills + links valid).
- [ ] Agent lists `.agents/skills/` unprompted when you ask "what skills do we have?"
- [ ] Agent calls Context7/MCP for a versioned package and cites version + date.
- [ ] New skill created from `templates/skill.md` passes the gate.
- [ ] `docs/tooling/TOOL-REGISTER.md` records your stack's MCP/doc sources.
