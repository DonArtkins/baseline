# Bug workflow

Use [the bug template](../templates/bug.md) for a reproducible problem. Keep status, owning spec, environment/revision, expected versus observed behavior, sanitized evidence, root cause, fix and regression result together. Summarize open bugs in [INDEX](INDEX.md).

Store screenshots and short sanitized logs under `evidence/`. Raw exports, session cookies, customer records and large binaries remain outside version control. A bug is closed only when the regression is verified. UI issues need viewport/theme/state information; concurrency issues need reproducible timing or an integration test.
