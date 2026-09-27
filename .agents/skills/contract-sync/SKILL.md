---
name: contract-sync
description: Synchronize an interface change across its owner and consumers before commit or review.
---

# Contract Sync

Read docs/planning/CONTRACT-SYNC.md. Identify semantics as well as names. Update canonical contracts, owner/consumer specs and contexts in the same branch. Record affected paths and verification in the target's `.baseline/change.json` (generated per project). Mechanical path checks supplement semantic review; they do not replace it.

Paths in these instructions are relative to the project root. Apply only when relevant to the user's task; existing authorization and environment permissions still govern actions.
