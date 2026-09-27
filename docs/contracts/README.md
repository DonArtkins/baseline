# Canonical contracts

Copy [the contract template](../../templates/contract.md) for each meaningful shared boundary. Group related endpoints under one domain contract rather than creating a file for every field.

A contract states its owner, version, consumers, request/response or event schema, auth, errors, limits, retries, idempotency, compatibility and test examples. Include an environment matrix separately when deployment configuration is shared. No secret values belong here.

The root integration context is the registry. A consumer context links its accepted contract version and records known gaps. Contract code or OpenAPI schemas can become the machine-readable authority once the stack is chosen; document how generated copies stay synchronized.
