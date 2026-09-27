# Security gates

## Included

The Python gate scans the candidate snapshot for common credential shapes, private key blocks and forbidden runtime artifacts. Findings show paths and line numbers, never matched secrets. Research and review evidence are included. This is a narrow hygiene check, not a complete secret scanner or security audit.

## Configure for your stack

Register actual dependency, secret-history and static-analysis commands in the selected systems' `security` command lists. Add authorization/injection/file-handling tests according to the threat model. Pin external tools and CI actions, review updates, and record limits and accepted findings with owners and expiry.

## CI and repository settings

Run checks on pull requests with read-only permissions and no deployment secrets. Require successful status checks and human review on the default branch. Protect gate/configuration changes with repository ownership rules. Do not use a privileged pull-request workflow to execute untrusted contributor code.

## Release evidence

Record dependency review, secret-history scan, auth boundary tests and recovery evidence relevant to the release. Mark missing commands NOT CONFIGURED; never print a green “secure” result because a tool was unavailable.
