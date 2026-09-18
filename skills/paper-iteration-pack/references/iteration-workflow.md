# Iteration Workflow

## 1. Build the request ledger

Before editing, write a compact ledger with one row per requested change:

| Field | Required content |
|---|---|
| Review item | The original suggestion or user request |
| Artifact | Page, section, figure, table, or source file |
| Current state | What the document currently says or shows |
| Source of truth | Frozen value, run output, raw data, or stated assumption |
| Acceptance test | Observable condition that proves the item is handled |
| Status | Open, changed, verified, or blocked |

If a suggestion is ambiguous, choose the least invasive interpretation that
still satisfies the stated review goal. Record the interpretation rather than
silently broadening the redesign.

## 2. Reconstruct the evidence chain

For every number or claim touched by the iteration, locate:

1. the document occurrence;
2. the figure, table, or generator that renders it;
3. the source result or data record;
4. the rounding and unit rule;
5. any downstream occurrence in abstract, conclusion, appendix, or evidence map.

Resolve conflicts in this order:

```text
frozen data / verified result > raw source data > explicit user-provided value
> old figure or screenshot
```

If the document and the source disagree, fix the document or the generator
after confirming the source. Do not "fix" the source to match stale prose.

## 3. Classify the revision

Choose the smallest category that reaches the requested outcome:

- **Copy only:** wording, terminology, or caption clarity.
- **Figure only:** encoding, labels, layout, palette, or dimensions.
- **Figure plus text:** the visual changes what a reader should notice.
- **Layout:** placement, width, page break, table density, or whitespace.
- **Evidence repair:** the claim lacks a traceable source or conflicts with it.
- **Upstream rebuild:** data, model output, or experiment parameters changed.

An upstream rebuild invalidates downstream visual and textual checks. Mark
them for fresh verification instead of carrying forward an old pass.

## 4. Edit the canonical source

- Patch the existing script or document source.
- Keep content and presentation separate: data, labels, and annotations should
  remain traceable to their records.
- Use a fixed seed or deterministic input when the figure depends on random
  simulation.
- Save over the requested output path. Remove obsolete generated copies when
  the user asked for an in-place replacement.
- Keep relevant source and output filenames stable so citations, LaTeX, or
  document links do not break.

## 5. Synchronize all surfaces

Update every affected surface in the same iteration:

- figure image or vector;
- figure caption;
- section body;
- table values and notes;
- abstract or executive summary;
- conclusion or recommendation;
- evidence map, manifest, or changelog where the project uses one.

Check repeated numbers explicitly. A figure can be numerically correct while
the prose still quotes an older percentage or a different rounding.

## 6. Verify in three layers

### Structural

- Expected source and output paths exist.
- File type, dimensions, and DPI or vector format are appropriate.
- The document references the intended filename.

### Runtime

- The figure or document can be regenerated from the canonical source.
- The generation command exits successfully from a clean working directory.
- Any data transformations used by the figure reproduce the same values.

### Visual

- Open the image itself at normal and zoomed-in reading size.
- Render or export the actual document and inspect the revised page.
- Confirm that labels, annotations, legends, captions, axes, and surrounding
  text do not overlap or clip.
- Confirm that the figure remains readable when printed or scaled to the final
  page width.

Record the strongest evidence obtained. Never upgrade a structural check to a
visual claim.

## 7. Close the iteration

The closeout should identify:

- the exact files replaced;
- the source values used;
- what the visual change improves;
- which checks were structural, runtime, and visual;
- what remains blocked or unverified.

For a multi-item review package, close with a checklist that maps each original
suggestion to its changed artifact and verification result.
