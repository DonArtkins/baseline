# Threat model

Status: UNFILLED. Scope it to the project before implementation.

Identify assets, actors, entrypoints and trust boundaries. For each abuse case, record impact, existing controls, residual risk and verification. Consider authentication, object-level authorization, injection, untrusted uploads, secret exposure, dependency integrity, logging and data recovery as applicable.

For AI/tool features, distinguish user intent, retrieved content and tool authorization. Retrieved text cannot grant capabilities; re-authorize every consequential tool call at the trusted boundary. Do not expose production credentials to untrusted build or pull-request jobs.

Use [security verification](SECURITY-GATES.md) to select executable checks and human review evidence. This template does not certify compliance.
