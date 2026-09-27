# Worked example: a claim about caching

This is an original hypothetical example. It is not a summary of any linked reel.

## Capture

A fictional video says a cache makes a dashboard faster. Record the source and timestamp in a real exercise. Here, the workload, cache key, expiry and consistency requirements are unknown.

## Questions

Which request is slow? Is time spent in the network, application, query or rendering? Can users tolerate stale data? Is the result user-specific? What happens after a write or when the cache fails?

## Research and experiment

Read the chosen database/cache vendor's version-specific documentation. Generate synthetic records in an isolated environment. Measure the same request before and after the proposed change under the same load. Verify authorization isolation, key scope, invalidation and failure behavior. No measurements have been run for this example.

## Reusable note

A useful note explains the circumstances under which caching helped, the correctness risks it introduced, the alternatives considered and the measurements needed before repeating the choice. It does not claim caching is always required.

## Project decision

If the real project meets its latency target without caching, retain the note but do not add the component. If measurements identify a suitable bottleneck, write an ADR and a feature spec with cache correctness and failure acceptance criteria.
