# Use AI to support engineering judgment

Before asking for code, make the decision concrete: who needs what, under which constraints, and what evidence would show success. Ask the agent to separate facts, assumptions and recommendations. A large answer is not necessarily a well-founded plan.

For each important choice, ask what simpler option was considered, what tradeoff the chosen option introduces, how it fails, who owns recovery and what evidence would cause you to revisit it. Apply this to data storage, caching, authentication, UI patterns and AI workflows alike.

Ask for a real failure example. If two users act at once, what preserves consistency? If a dependency times out, what does the user see? If an actor has the wrong permission, where is the request denied? If a deployment fails, how do you recover? Translate the answers into contracts and acceptance criteria.

Use the agent to research, compare, draft, implement and verify within a clear scope. Retain human ownership of product decisions and consequential approvals. Review concrete artifacts and test results rather than confidence in the agent's wording. Carry the decision into maintained context so the next session starts from evidence.
