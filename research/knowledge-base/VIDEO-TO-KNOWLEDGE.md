# From Instagram or YouTube to usable engineering knowledge

## 1. Capture the source honestly

Start with any of the five reels in [the source register](../sources/REGISTER.md), or another creator you follow. Watch the source yourself when the agent cannot access it. Record URL, creator as shown, date, topic, timestamps and your own notes. Capture a transcript or screenshots only where you have permission to use them. Do not bypass access controls or claim unseen content was reviewed.

Separate the creator's claim, a demonstrated example and your interpretation. A short video may omit workload, versions, failure modes, costs or prerequisites. Those omissions become research questions.

## 2. Ask AI to extract claims, not manufacture authority

Supply the captured material and use this prompt:

```text
Work only from this supplied transcript/notes. Extract each technical claim with
its timestamp or note reference. Label missing details and ambiguity. Distinguish
what the creator said from your interpretation. Do not invent their stack,
benchmarks or examples. Return a verification checklist, not a project decision.
```

Ask for a table: claim, conditions, evidence shown, missing context, authoritative source to consult, safe experiment. Reject claims the model cannot map to the source.

## 3. Verify the mechanism

For each consequential claim, consult official documentation, original papers or a reproducible experiment appropriate to the subject. Check the relevant version and date. For a library API, use Context7 if available and follow its original documentation links; if unavailable, use the vendor documentation directly.

Ask: What workload was measured? What tradeoff changed? What happens on failure? What assumptions make this true? What counterexample would disprove a universal statement? Keep conflicting evidence rather than smoothing it away.

## 4. Run a small isolated exercise

Use synthetic data and a disposable environment. Predict the outcome before running. Save commands, versions, inputs and measured results. Avoid turning a learning exercise into production access or an unapproved external action. If no experiment was run, write NOT TESTED.

## 5. Write the reusable note

Summarize in your own words. Include applicability, limitations, alternatives and the evidence trail. Attribute a short quotation only when necessary. Do not republish whole transcripts, paid course materials or downloaded books as your own knowledge base.

## 6. Promote deliberately

Use states: CAPTURED → CHECKED → ADOPTED, or REJECTED/SUPERSEDED. CHECKED means the claim has evidence; ADOPTED means you have decided to use it within a named scope. A verified technique can still be wrong for your project's size, budget or team.

## 7. Transfer a project-specific decision

Link the note from a research finding. Compare options against the project brief. If adopted, write an ADR, update stack/contracts, and create an appropriately scoped feature spec. This path gives AI the context of your reasoning without turning social-media advice into mandatory architecture.
