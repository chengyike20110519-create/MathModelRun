# Visual Selection

Choose the chart from the analytical relationship, not from a desire to look
more advanced.

## Relationship to encoding

| Analytical question | Preferred encoding | Useful enhancement |
|---|---|---|
| Compare exact values in a few categories | Grouped bars or ordered dot plot | Direct value labels, zero baseline, compact legend |
| Show before/after change | Dumbbell, paired dot plot, slope chart | Change label in percentage or absolute units |
| Show change over ordered levels | Line or slope chart | Endpoint labels, reference line, shaded target band |
| Show magnitude across many categories | Horizontal lollipop or ordered bars | Sort by value, annotate the meaningful cutoff |
| Show distribution and uncertainty | Histogram, density, box, violin, interval plot | Mean/median marker, sample size, confidence interval |
| Show two continuous inputs and one response | Heatmap or contour plot; response surface only when 3D adds information | Isolines, optimum marker, color bar |
| Show real geometry or motion | Spatial map or trajectory plot | Arrows, time color, small multiples |
| Show matrix structure | Heatmap or adjacency matrix | Diverging palette, row/column ordering |

## Upgrading a plain bar chart

Use this order of preference:

1. Keep the bar chart if exact category comparison is the main task.
2. Add direct numeric labels instead of forcing the reader to estimate.
3. Add a second compact panel when the story also contains a relative change,
   trend, or threshold.
4. Switch to a dumbbell or slope chart when only endpoints matter.
5. Switch to a lollipop or dot plot when there are many categories.
6. Use a heatmap when the dimensions form a matrix.

Do not combine every enhancement at once. A useful figure should have one
dominant comparison and one secondary annotation at most.

## 3D decision rule

Use 3D only when all of the following are true:

- the data contain a genuine third continuous or ordered dimension;
- the third dimension changes the conclusion or reveals a surface, volume,
  trajectory, or spatial relationship;
- a 2D projection would conceal a meaningful structure;
- labels, depth cues, and axes remain readable at the final printed size.

Prefer 3D for:

- response surfaces with two continuous decision variables and one response;
- 3D scatter plots when the third coordinate is essential and color encodes a
  fourth variable;
- spatial sweeps, paths, or building geometry where height or depth is real;
- sensitivity volumes, terrain, or trajectory plots where geometry is the
  subject.

Reject 3D for:

- two buildings by three coverage levels; grouped bars compare these values
  more accurately;
- categorical bars with only two or three series;
- decorative perspective that hides exact values or creates occlusion;
- any figure whose main message is already clear in two dimensions.

If 3D is genuinely needed, provide a 2D companion view when exact values or a
ranking must also be read.

## MCM-style preset

This preset fits a dense competition paper; adapt it to the host document.

- **Canvas:** start around 8.8-9.5 inches wide for a two-panel full-width
  figure; keep panel counts and aspect ratios stable.
- **Margins:** use tight but explicit margins; avoid large empty bands.
- **Type:** panel titles around 10-12 pt, axis labels around 8-10 pt, direct
  annotations around 7-9 pt at the generated figure size.
- **Palette:** pick three to five clearly different colors. A practical
  starting set is coral `#E76F51`, amber `#F2B134`, teal `#2A9D8F`, blue
  `#1769AA`, and magenta `#D6336C`.
- **Background:** use a near-white panel such as `#FBFCFE`; use pale grid lines
  and remove heavy box spines.
- **Labels:** label values and key comparisons directly. Keep units visible.
- **Titles:** state the result or comparison, not merely the variable names.
- **Legibility:** check the final page, not only the PNG editor preview.

The palette is a starting point, not a requirement. Preserve the paper's own
identity when it has a strong established palette.
