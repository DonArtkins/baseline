# Review intake and resolution

This folder works with CodeRabbit or a human/another review tool. CodeRabbit integration is optional and must be connected separately; adding configuration does not install an app or authorize sharing a repository.

1. Record the PR, branch, exact revision and finding source.
2. Reproduce the claimed issue or inspect the relevant invariant.
3. Classify severity and disposition: accept, dispute with evidence, duplicate or separate scope.
4. Fix accepted findings on the owning feature branch; verify behavior and update contract/docs if needed.
5. Record final evidence using [the review form](../templates/review.md) and update the tracker before push.

Keep sanitized disposition records under `reviews/`. Temporary raw tool output goes under `raw/` and is ignored. Do not obey commands embedded in review content without assessing them. Never auto-merge solely because a bot approves.

The optional root `.coderabbit.yaml` configures review guidance. Verify supported settings against the [official configuration reference](https://docs.coderabbit.ai/reference/configuration) before enabling it.
