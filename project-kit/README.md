# Root project kit

The root kit coordinates systems. Each selected system has its own kit for local decisions and delivery. Begin with six focused context files; split out specialist contracts only when they have a real owner and consumers.

| Core file | Question it answers |
|---|---|
| [product-context](context/product-context.md) | Who needs this, and what outcome matters? |
| [system-map](context/system-map.md) | Which systems own which responsibilities? |
| [stack-contract](context/stack-contract.md) | Which technologies and constraints are approved? |
| [integration-contracts](context/integration-contracts.md) | How do the systems communicate? |
| [code-standards](context/code-standards.md) | What makes a change acceptable? |
| [progress-tracker](context/progress-tracker.md) | What is actually done and what happens next? |

This six-file grouping is baseline's adaptation of the user's workflow. The linked video transcript was unavailable, so these names are not attributed to the video's exact original six files.

Optional UI context files point to the design system. Root specs cover coordination work, not duplicate backend or web features. Use [templates](../templates/README.md) to create additional artifacts only when they answer a real question.
