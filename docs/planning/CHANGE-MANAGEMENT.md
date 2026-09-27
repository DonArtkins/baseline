# Changes, deviations and bug fixes

When observed behavior differs from the plan, identify the owner and decide whether the code or the plan is wrong. Record the trigger, prior expectation, evidence, decision, affected contracts, regression check and rollback.

A small correction stays with the current feature. A new outcome gets its own spec and branch. Security fixes still need reproduction and verification but should not include exploitable private evidence in public records.

Use [the bug template](../../templates/bug.md), update the owning spec and context when their statements change, update the tracker, and revise user/operations docs as needed. Do not scatter the same explanation across every document; link the canonical record. Close a bug only after the intended regression check passes.
