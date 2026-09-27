# Organize knowledge for people and agents

## Route by question

Your index should answer “where do I read about this?” rather than reproduce every note. Group cross-cutting concerns separately from platform and domain material. Link companion notes and explain which one to read first when order matters.

A routing row can contain: question/topic, entry note, prerequisites, scope, last review and authority level. Example: “How do I choose client state ownership?” routes to a state-model note; it need not load database or payment guidance.

## Separate kinds of statements

Label facts verified from sources, local conventions, project decisions, hypotheses and deprecated guidance. Record version-sensitive claims. An agent should never mistake an experiment from last year for a current provider guarantee.

## Write an AGENTS entrypoint

Tell agents how to search the index, select relevant notes, report inaccessible sources, check current APIs and preserve private material. Make explicit that project requirements override advisory preferences. Source content must not instruct the agent to execute commands or reveal secrets.

## Keep retrieval simple initially

Start with file paths, topic names, aliases and `rg`. Good titles and links often solve retrieval without an embedding service. Consider semantic retrieval only after observing failed searches in a sufficiently large collection, and define permissions, provenance and freshness before indexing it.

## Avoid duplicate truth

One note owns a concept. Other notes link to it and add only domain-specific differences. Maintain a small glossary for overloaded words; a domain-specific meaning should not silently replace a general definition.
