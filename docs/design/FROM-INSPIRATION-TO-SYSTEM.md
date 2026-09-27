# Turn UI references into a complete design system

## 1. Start with the product's jobs

List the people, journeys, screen types, devices and information density. A landing page, a daily work dashboard and a mobile checkout need different structures. Select references that solve comparable interaction problems.

## 2. Search deliberately

On Dribbble, search by surface and behavior: dashboard filters, empty search results, mobile settings, table detail drawers. On X, inspect the original posts of creators you value, including the user-suggested `@marcelkargul`; follow links to actual demos where available. Do not treat popularity as evidence of usability.

Capture a small coherent set with source/creator links. Include full screens and closeups of relevant controls. Prefer references with more than one state or viewport. Add observations to the inspiration catalog; a saved screenshot without provenance is unfinished intake.

## 3. Decompose the references

Ask the AI to inspect supplied images and separate observation from inference:

```text
For each reference, describe layout, spacing rhythm, type hierarchy, color roles,
control anatomy, information density and visible states. Mark inferred measurements.
Identify missing responsive, focus, loading, error and empty states. Do not assume
behavior that a screenshot cannot show. Propose what fits our product and why.
```

Look for relationships: text hierarchy, alignment, repeated gaps and action prominence. An AI-estimated 24px gap is a hypothesis until measured or deliberately chosen.

## 4. Choose a visual direction

Select one canonical layout for a surface and name supporting sources by component. Explain rejected traits: low contrast, excessive decoration, tiny targets, unusable data density or motion that obscures work. Resolve conflicting references in a design decision rather than allowing each screen to choose differently.

## 5. Define tokens

Build primitive values, semantic roles and component mappings. Color roles include canvas, surface, text, border, action, focus and status. Define typography, spacing, radius, elevation, density, layering and motion. Use semantic names such as `color.text.secondary`; avoid product code depending directly on a sampled screenshot color.

Define both themes if the product requires them. Verify actual foreground/background combinations, including charts and disabled/selected states. Keep canonical values in [ui-tokens](../../project-kit/context/ui-tokens.md), with implementation mappings in each consumer. This document owns methodology, not duplicate token values.

## 6. Specify components and behavior

Register buttons, fields, validation messages, menus, dialogs, tables, navigation and domain components in [ui-registry](../../project-kit/context/ui-registry.md). Specify anatomy, variants, sizing, keyboard behavior, focus, labels, content limits and state transitions. A disabled button should explain how the user can proceed where that is unclear.

Cover default, hover where applicable, focus-visible, pressed, selected, disabled, loading, empty, error, success and permission-denied states as relevant. State what happens to entered data after a failure or navigation.

## 7. Design screens and flows

Create wireframes for real journeys using the component system. Include representative long text, large counts, missing data, slow network and narrow viewports. Define navigation and information priority rather than merely arranging cards. Record accessible names, focus order and responsive transformations.

## 8. Approve a concrete version

Keep editable design files and exported evidence in the target's own design location (or `docs/design/`), with source URL/node, version and approver. Figma is optional; any reviewable format can work. An exported image is not automatically approved. Record sign-off in the approval register before UI implementation.

## 9. Implement and verify

Map tokens to the chosen framework's theme, build reusable components and implement one representative screen before expanding. Compare at named viewports and states. Test keyboard interaction, zoom/reflow, screen-reader semantics, reduced motion and contrast as relevant to the product's accessibility target. Log visual discrepancies as bugs with evidence.

## 10. Evolve the system

A new screen should reuse existing tokens/components first. When a new pattern is necessary, update the registry and design contract with rationale, source and consumer impact. Avoid one-off overrides that quietly fork the design system.
