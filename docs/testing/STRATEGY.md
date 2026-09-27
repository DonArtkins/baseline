# Verification strategy

Map each acceptance criterion to the cheapest credible evidence: unit behavior, integration boundary, contract parity, end-to-end journey, visual/accessibility check or operational drill. Include authorization denials and recovery paths, not only successful requests.

Keep local tests with their system and cross-system suites under QA when that system is selected. Define fixture ownership, isolated environments, cleanup, nondeterminism control and what external services are mocked. Record pass/fail/skip counts and explain skipped required checks.

AI workflows also need representative evaluation cases, tool authorization tests, prompt-injection cases, cost/latency measurements and failure handling. Evaluation success is not permission for autonomous writes.
