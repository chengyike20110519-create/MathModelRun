# Independent evaluation rubric

Use this rubric in `REVIEW`, `RECOVER`, and final `DELIVER` mode. The evaluator
is not the same context that generated the artifact. Re-run the important
commands and inspect the files; do not accept a summary as evidence.

## Scoring

Score each dimension from 0 to 5.

| Score | Meaning |
|---:|---|
| 0 | Missing, fabricated, or contradicted by evidence |
| 1 | Mentioned but not executable or not traceable |
| 2 | Partially implemented; important gaps block confidence |
| 3 | Meets the minimum standard and can be defended |
| 4 | Strong, consistent, and independently reproducible |
| 5 | Exceptional, robust across plausible changes, and clearly explained |

Use a weighted score:

| Dimension | Weight | Hard floor |
|---|---:|---:|
| Problem fidelity | 0.12 | 3 |
| Model reasoning | 0.15 | 3 |
| Method validity | 0.15 | 3 |
| Data provenance and leakage control | 0.12 | 3 |
| Reproducibility | 0.12 | 3 |
| Result strength and comparison | 0.12 | 3 |
| Sensitivity and robustness | 0.08 | 2 |
| Paper clarity and argument | 0.06 | 2 |
| Figure, table, and submission quality | 0.04 | 2 |
| Reproducibility of final package | 0.04 | 3 |

Weights sum to 1.00. A project cannot pass if any hard floor is missed, even
when the weighted average is high.

## Dimension questions

### 1. Problem fidelity

- Does each answer directly address the asked question?
- Are the output type, units, time range, and population correct?
- Are problem facts separated from modeling assumptions?
- Did any fallback quietly change the question?

### 2. Model reasoning

- Is there a transparent baseline?
- Is the primary model justified rather than merely sophisticated?
- Are symbols, variables, parameters, objectives, and constraints consistent?
- Are rejected routes documented with concrete reasons?
- Is every assumption tied to a boundary or failure consequence?

### 3. Method validity

- Was a small proof of concept run before the full experiment?
- Do the mathematical formulation and implementation agree?
- For optimization, are solver status, objective, bounds, feasibility, and
  constraint violation checked?
- For prediction, are split, leakage, metric, and baseline appropriate?
- For simulation, are seed, repetitions, convergence, and uncertainty handled?

### 4. Data provenance and leakage control

- Does every data field have a source, unit, range, and missing-value rule?
- Are cleaning operations logged before execution?
- Is future or target information excluded from predictive features?
- Are public data, estimated values, simulated values, and user assumptions
  visibly distinguished?
- Is external data recorded with access date and citation?

### 5. Reproducibility

- Can a fresh agent run the key path from saved files?
- Are commands, environment, seeds, parameters, inputs, and hashes recorded?
- Do figures and tables have generating scripts?
- Does the frozen number match the named run and source file?
- Are manual edits to outputs detectable and prohibited?

### 6. Result strength and comparison

- Is the primary model compared with the baseline using the same metric and
  data split?
- Are uncertainty, confidence, or error bars reported where appropriate?
- Are improvements quantified rather than described vaguely?
- Are negative or mixed results explained honestly?
- Do conclusions stop where the evidence stops?

### 7. Sensitivity and robustness

- Are important parameters varied across plausible ranges?
- Are structural assumptions tested, not only numerical parameters?
- Is the conclusion stable under reasonable perturbations?
- Are unstable regions reported as limitations?
- Is a fallback plan documented for the failure boundary?

### 8. Paper clarity and argument

- Does every question receive a clear answer?
- Does the writing move from assumptions to model to evidence to conclusion?
- Are equations readable and connected to implementation?
- Are claims tied to evidence rather than rhetoric?
- Are limitations specific and credible?

### 9. Figure, table, and submission quality

- Are figure purpose and source clear?
- Are axes, units, legends, captions, and references correct?
- Are tables readable and numbered?
- Is the PDF free of overflow, missing figures, and blank pages?
- Does the package follow the contest template and anonymity rules?

### 10. Reproducibility of final package

- Does the submitted bundle include the necessary code, data references,
  environment notes, and build instructions?
- Are secrets, absolute personal paths, caches, and unrelated files excluded?
- Can the main result be rebuilt after the contest without reconstructing
  missing steps?
- Is the final PDF the one generated from the submitted source?

## Verdict rules

`PASS` requires all of the following:

1. Every acceptance criterion has reproduced evidence.
2. No hard floor is missed.
3. Weighted score is at least 4.00.
4. There are no hard errors.
5. No paper number or core claim is unverified.
6. The final package reproduces the reported PDF and frozen numbers.

Otherwise return `FAIL` with:

- the failed dimensions and criteria;
- the earliest invalid stage;
- the exact evidence that failed;
- one minimal corrective action per failure;
- whether the next strategy is `refine`, `fallback`, `replan`, or `stop`.

## Evaluation output

Write `audit/acceptance.json`:

```json
{
  "schema_version": "2.0",
  "generated_at": null,
  "verdict": "fail",
  "weighted_score": 0.0,
  "dimensions": [
    {
      "id": "method_validity",
      "score": 0,
      "weight": 0.15,
      "floor": 3,
      "passed": false,
      "reason": "",
      "evidence": []
    }
  ],
  "failed_criteria": [],
  "return_stage": "S4",
  "strategy": "refine",
  "unverified_claims": []
}
```

Use `strategy` as follows:

- `refine`: concept is sound; fix evidence or implementation;
- `fallback`: primary route failed; switch to the recorded fallback;
- `replan`: the contract or question no longer matches the work;
- `stop`: no defensible continuation remains within constraints.

## Reviewer guardrails

- Do not edit the artifact you are reviewing to make it pass.
- Do not trust the generator's summary, screenshot, or chat statement.
- Do not lower a hard floor because the result is elegant or expensive.
- Do not treat a compiled PDF as evidence that its numbers are valid.
- Do not treat unit tests as sufficient when the contest claim is user- or
  solver-visible.
- If a check cannot be reproduced, mark it unverified rather than failed or
  passed.
