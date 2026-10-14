---
name: mathmodel-data-figure
description: "Design and revise evidence-based Python result charts for modeling papers; choose encodings from the argument, verify data meaning, render at manuscript size, and prepare files for independent scientific and visual review. Not for AI workflow images or changing the model."
---

# MathModel Data Figure

Read `my-mathmodel-agent/references/data-figure-agent.md` from the repository
root and only the reference designs applicable to the task. Treat it as the
operating contract. Work on the delegated subproblem, verified inputs, active
figure paths and actual manuscript dimensions. Do not alter raw data, frozen
results, the model or unrelated paper sections to improve the appearance.

Compare two suitable encodings, preserve the estimator and uncertainty
meaning, save the figure specification and numerical checks, then generate
native Python data figures and captions. Inspect actual final-size and grayscale
previews. Address specific defects; colors and complexity must express evidence.

Seal the exact artifacts using `figure_gate.py`, leaving scientific and visual
reviews pending for an independent reviewer. Return preview/vector files,
definitions, check evidence, any blocking missing data, and the review entry
point. AI conceptual workflows are routed through `ai-workflow-gate.md` instead.
