# Data model and lifecycle

Status: UNFILLED; no schema or database choice is approved.

Document entities, relationships, keys, constraints, indexes, deletion/retention and access boundaries. Include estimated growth and sensitive fields. Link the approved ERD/version (stored in the target's own docs or `docs/` location) before schema code.

For every migration, identify compatibility, backfill, verification and recovery. Separate generating migration files from applying them to an environment. A fresh-database test does not prove upgrade safety; test representative existing data where relevant.
