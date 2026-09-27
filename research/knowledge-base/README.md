# Build your own engineering knowledge base

A knowledge base stores reusable judgment: how to choose, why an approach works, when it fails, and how to verify it. A project kit stores the decisions for one project. Keep these jobs separate so a tutorial does not silently become a requirement for every application.

Borrowed format only: topic routing, cross-cutting guidance, focused engineering volumes, and documented updates. It contains original starter instructions and examples — no company standards, business content, or proprietary volumes of any kind.

## Start with a small collection

Pick three recurring questions from your own work, such as API error design, session handling or accessible forms. Write one short note per question with sources and verification. Add a master index that routes an agent to those notes. Expand only when a real question needs another topic.

Suggested structure for a separate personal knowledge repository:

```text
my-knowledge-base/
├── AGENTS.md           How agents locate and evaluate guidance
├── README.md           Topic map and reading routes
├── sources/            Attributed capture notes; private material segregated
├── inbox/              Unverified ideas awaiting review
├── core/               Architecture, security, testing principles
├── engineering/        APIs, data access, state, delivery
├── surfaces/           Web, mobile, desktop, CLI and design
├── domains/            Only domains you actually work in
├── decisions/          Your adopted working preferences and exceptions
└── meta/               Versions, corrections and maintenance schedule
```

You can begin under this template's `research/knowledge-base/` starter. The master copy lives next to the generated projects at `~/Projects/Workflows/my-knowledge-base/` — never inside one — created ONCE by `scripts/configure.py` for a first-time user (with its own `AGENTS.md` populating guide) and left untouched afterwards. Keep project-specific entity names, customer data and secrets out of the shared base.

## Export as its own repo (recommended)

The KB compounds across projects while projects come and go, so give it independent history:

```sh
cd ~/Projects/Workflows/my-knowledge-base
git init -b main
git add . && git commit -m "knowledge base seed"
gh repo create knowledge-base --private --source=. --push
```

Keep pushing updates after each project (what worked, counterexamples, version changes). Each project linkage is remembered in `~/Projects/Workflows/.registry/<slug>.json` with the KB path. Agents consult it by topic; never bulk-import it or commit target secrets to it.

## Use the guides in order

1. [Turn videos into verified notes](VIDEO-TO-KNOWLEDGE.md).
2. [Organize and retrieve knowledge](ORGANIZATION-AND-RETRIEVAL.md).
3. [Start with the starter topics](STARTER-TOPICS.md).
4. [Maintain it and apply it to projects](MAINTENANCE-AND-PROJECT-USE.md).
5. [Use the AI prompt recipes](AI-PROMPTS.md).
6. Read [the worked example](WORKED-EXAMPLE.md).

## What a useful note contains

A precise question, a short answer, situations where it applies, alternatives, counterexamples, current sources, a small verification exercise, open uncertainty and a last-reviewed date. Use [the knowledge-note template](../../templates/knowledge-note.md).

“Always use framework X” is usually a poor reusable note. “For these constraints, X reduces this cost; choose Y when these conditions change” preserves the reasoning an engineer needs.
