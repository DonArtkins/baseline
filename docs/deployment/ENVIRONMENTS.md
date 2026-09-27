# Environments and configuration

| Environment | Owner | Services | Data classification | Config names/source | Approval boundary |
|---|---|---|---|---|---|
| Local | To assign | To design | Synthetic | Names only | Local setup |
| CI/test | To assign | To design | Synthetic | Secret store references | Isolated tests |
| Production | To assign | To design | Determine | Secret manager references | Explicit release authorization |

Record ports, hostnames, service IDs and env names as contracts. Commit only empty placeholders in `.env.example`; never copy live values into planning documents. Define credential rotation and who may access each environment.
