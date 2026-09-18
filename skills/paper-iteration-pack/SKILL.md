---
name: paper-iteration-pack
description: "Iterate an existing paper or report from concrete review feedback: audit claims and source data, redesign figures, tighten layout, synchronize numbers, render, and verify the final document in place. Use for paper/figure revision packages, chart upgrades, and submission polish. Do not use for drafting a paper from scratch or for a one-line wording change with no evidence or layout impact."
metadata:
  short-description: "Turn paper review feedback into verified visual and textual revisions"
---

# Paper Iteration Pack

Use this skill when a paper, report, thesis section, competition paper, or
slide-like document already exists and the user provides review suggestions,
figure feedback, or a request to make the delivery clearer, tighter, brighter,
or more submission-ready.

The unit of work is an **iteration package**, not a collection of isolated
edits. One package normally contains:

1. a source-of-truth ledger;
2. the revised figure or layout source;
3. synchronized text, captions, tables, and references;
4. a rebuilt output artifact;
5. visual and numeric verification;
6. a short change and evidence report.

## Non-negotiable rules

- Read the existing document, current figure, generator, caption, and nearby
  claim before changing anything. Do not redesign from a screenshot alone.
- Trace every changed number to a frozen result, run output, raw data, or an
  explicitly labeled user-provided value. Never silently reconcile a conflict
  by copying a number from the old figure.
- Keep a stable rounding policy. A displayed percentage must agree with the
  same source value used in the abstract, body, table, figure, and conclusion.
- Rebuild figures from their existing source when possible. Replace the target
  file in place; do not create `v2`, `final-final`, or parallel old versions.
- Treat rendering as separate from generation. A saved PNG is not proof that
  the paper page is correct. Compile or export the document and inspect the
  actual page containing the revised material.
- Record structural, runtime, and visual evidence separately. A file-existence
  check does not prove that a chart is readable or that a PDF page fits.
- Preserve the author's language, terminology, citation style, and document
  class unless the review request explicitly asks for a change.
- Stop and report a blocker when source data, generator code, or required
  rendering tools are missing. Do not invent data to make the visual look
  complete.

## Iteration workflow

1. **Frame the requested change.** Extract the review suggestions and turn
   them into observable acceptance criteria: what must change, where it must
   appear, and how it will be checked.
2. **Audit the current state.** Locate the document source, target page or
   section, figure file, figure generator, source data, caption, and every
   repeated number or claim.
3. **Choose the revision scope.** Decide whether this is a figure-only change,
   figure plus text, layout-only change, evidence/provenance repair, or a
   source-data problem that requires upstream regeneration.
4. **Choose the visual encoding.** Match the chart to the comparison. Read
   [references/visual-selection.md](references/visual-selection.md) when the
   request mentions advanced charts, bar-chart upgrades, density, color, or 3D.
5. **Implement in the canonical source.** Patch the existing plotting or
   layout code, regenerate the target artifact in place, and keep any style
   preset configurable rather than hard-coding one paper's content.
6. **Synchronize the document.** Update the caption, body, table, abstract,
   labels, and evidence mapping whenever the visual or source value changed.
7. **Render and inspect.** Rebuild the paper or report and inspect the actual
   revised page at normal reading size. Check clipping, overlap, font size,
   contrast, aspect ratio, aspect-ratio distortion, and print legibility.
8. **Report the package.** State changed files, source values, visual changes,
   commands or tools used, verification level, and any unresolved limitation.

For a fuller stage-by-stage procedure, read
[references/iteration-workflow.md](references/iteration-workflow.md).

## Figure decisions that are easy to get wrong

- Use a grouped bar or dot plot when a small number of exact category values
  must be compared. Label values directly and start the scale at zero for
  bars.
- Add a second panel only when it answers a distinct question. A useful pair is
  absolute values plus relative change, a slope chart, or a small-multiple
  breakdown.
- Prefer dumbbell or slope charts for before/after comparisons. Prefer a
  lollipop or ordered dot plot when many categories make solid bars noisy.
- Use a heatmap for a matrix, a response surface for two continuous inputs and
  one continuous response, and a spatial plot when the data have real geometry.
- Do not use 3D merely to make a chart look advanced. A 3D bar chart normally
  hides exact values and adds occlusion. Use 3D only when the third dimension
  is a genuine ordered or continuous variable and rotation reveals structure
  that a 2D projection cannot communicate reliably.

## MCM/MCM-style visual preset

Treat this as a preset, not a universal rule:

- compact canvas with controlled margins;
- bright but distinguishable colors with sufficient contrast;
- light neutral panel background, subtle grid, no heavy border;
- direct labels or direct annotations instead of a distant legend when space
  permits;
- one result-oriented title per panel or figure;
- full-width placement only when the extra detail is readable at paper scale.

Do not describe a figure as submission-ready until the rendered page has been
inspected. If the renderer or page inspection is unavailable, say exactly
which part remains unverified.

## Completion report

Keep the final report short and evidence-oriented. Include:

- **Changed:** document, figure, caption, data, and generator paths;
- **Data:** source files or frozen values used, including units and rounding;
- **Visual decision:** what was changed and why that encoding fits the claim;
- **Verification:** generation command/result, render command/result, and what
  was visually inspected;
- **Remaining risk:** any missing source, tool limitation, or unchecked claim.

Use the user's language for the report. In Chinese requests, use
`中文为主、英文术语保留原文` unless told otherwise.
