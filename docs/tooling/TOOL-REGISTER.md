# Tool register

| Tool | Role | Selected version/status | Source | Validation |
|---|---|---|---|---|
| Python | Portable local gates | 3.10+ standard library | Python installation in the environment | Gate and regression checks |
| Git | Candidate snapshots and branch checks | Installed version | Git CLI | Isolated repository tests |
| Husky | Hook installation | 9.1.7, pinned | [Official setup](https://typicode.github.io/husky/get-started.html) | Installed; lockfile generated; actual hooks passed isolated Git verification |
| actions/checkout | CI checkout | Fixed v4 commit in workflow | [Official repository](https://github.com/actions/checkout) | YAML supplied; live CI needs your repository |
| CodeRabbit | Optional review assistant | Disabled by default | [Configuration](https://docs.coderabbit.ai/reference/configuration) | No account/app connected |
| Context7 | Current-doc retrieval via MCP | Per-machine config, key in env (never committed) | [Official repository](https://github.com/upstash/context7) | Ask agent to fetch a versioned package doc and cite version/date; fallback to official docs recorded as unverified |
| Agent skills | File-based procedures | 10 root skills + infra/qa kits, `name:`/`description:` frontmatter | [Skills/MCP/Context7 setup](SKILLS-MCP-CONTEXT7.md) | `check.py --mode template` validates frontmatter + links |
| MCP servers | Editor/CLI tool backends (filesystem, GitHub, DB, …) | Per-machine `mcp.json`/TOML, no secrets in repo | [Skills/MCP/Context7 setup](SKILLS-MCP-CONTEXT7.md) | Agent lists servers; version/source/date recorded in specs |

These choices support the workflow only; they do not choose the product stack. Recheck supported versions and compatibility when adopting the template. Pin reviewed tool versions/actions; run `npm install` to generate the lockfile and use `npm ci` after. Record provider/API/tool changes here and in affected setup documentation.
