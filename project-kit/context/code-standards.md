# Shared code and documentation standards

## Code

Choose language-specific formatting, typing, linting and test commands in each system kit. Keep domain decisions out of presentation adapters. Prefer the smallest component that solves the measured problem. Comments explain decisions and invariants rather than narrating syntax.

## Documentation

Write concrete inputs, outputs, ownership and acceptance criteria. Use relative links, named sources and dated evidence. Maintain one current statement per fact. Examples are labelled examples; unknowns are labelled unknowns. Update current sections in place and move historical details into linked evidence.

## Verification

Record exact commands, result counts, test environment and revision. Test observable behavior and important failure paths. Do not inflate coverage with tests that repeat implementation details. Docs-only edits need document checks, not an unrelated application build.

## Reviews

Check correctness, authorization, data consistency, usability, maintainability and operational recovery. The [review workflow](../../.coderabbit/README.md) applies with or without CodeRabbit.
