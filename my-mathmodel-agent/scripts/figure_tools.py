"""Original, reusable Matplotlib helpers for contest-paper figures.

Import this module before pyplot and call prepare_runtime(). These are layout
and export helpers, not statistical estimators or scientific validation.
"""
from contextlib import contextmanager
from pathlib import Path
import hashlib
import json
import os
import tempfile


COLORS = {
    "ink": "#243746", "muted": "#596b78", "grid": "#e4ebed",
    "primary": "#166b80", "alternative": "#ba612c", "range": "#728b98",
    "accent": "#85446c", "neutral": "#b4c3ca",
}


def prepare_runtime(cache_dir=None, bundled_fonts=False):
    """Use file rendering and a writable cache; bypass system-font scanning
    only when explicitly requested for Latin-only figures in restricted macOS.
    For Chinese text, register an actual CJK font with font_manager.addfont().
    """
    cache = Path(cache_dir or Path(tempfile.gettempdir()) / "himcm-plot-cache")
    cache.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(cache))
    os.environ.setdefault("MPLBACKEND", "Agg")
    if bundled_fonts:
        os.environ.setdefault("MPL_IGNORE_SYSTEM_FONTS", "1")


@contextmanager
def paper_style(font_size=9.5, font_family="DejaVu Sans"):
    """Scoped starting style; dimensions are chosen by the figure script."""
    import matplotlib as mpl
    with mpl.rc_context({
        "font.family": font_family, "font.size": font_size,
        "axes.labelsize": font_size, "axes.titlesize": font_size + 0.5,
        "axes.titleweight": "bold", "axes.titlelocation": "left",
        "axes.titlepad": 12, "axes.labelcolor": COLORS["ink"],
        "axes.edgecolor": COLORS["neutral"], "axes.linewidth": 0.65,
        "text.color": COLORS["ink"], "xtick.color": COLORS["muted"],
        "ytick.color": COLORS["muted"], "xtick.labelsize": font_size - 0.5,
        "ytick.labelsize": font_size - 0.5, "xtick.major.size": 3,
        "ytick.major.size": 3, "grid.color": COLORS["grid"],
        "grid.linewidth": 0.6, "axes.axisbelow": True,
        "lines.linewidth": 1.6, "lines.markersize": 5,
        "legend.fontsize": font_size - 0.5, "legend.frameon": False,
        "figure.facecolor": "white", "axes.facecolor": "white",
        "savefig.facecolor": "white", "savefig.transparent": False,
        "savefig.bbox": None, "pdf.fonttype": 42, "ps.fonttype": 42,
        "svg.fonttype": "none", "text.usetex": False,
    }):
        yield


def clean_axes(ax, grid=None):
    """Keep the axes needed to read quantitative position."""
    ax.spines[["top", "right"]].set_visible(False)
    if grid is not None:
        ax.grid(axis=grid)
    return ax


def panel_title(ax, letter, title):
    ax.set_title(f"{letter}  {title}", loc="left")


@contextmanager
def nature_style(font_size=9, font_family="DejaVu Sans"):
    """Nature-inspired hierarchy adapted to contest-paper readability.
    This is an aesthetic preset, not a journal submission certification.
    """
    import matplotlib as mpl
    with paper_style(font_size=font_size, font_family=font_family):
        with mpl.rc_context({"axes.titlesize": font_size,
                             "axes.titleweight": "normal", "axes.titlepad": 10,
                             "axes.linewidth": 0.6, "lines.linewidth": 1.5,
                             "xtick.major.width": 0.6, "ytick.major.width": 0.6}):
            yield


def nature_panel_title(ax, letter, title):
    """Small lowercase label and a subordinate, aligned title."""
    ax.set_title(title, loc="left", pad=10, x=0.08)
    ax.text(0, 1.035, letter.lower(), transform=ax.transAxes,
            fontweight="bold", va="bottom", ha="left")


def check_panel_alignment(fig, groups, *, tolerance_pt=1.5):
    """Measure final drawn plot areas, not GridSpec cell allocations.
    groups are dicts with name, axes, and properties such as left/right/top/
    bottom/width/height. Intentional hero-width differences are excluded from
    equal-width groups explicitly by the consuming figure script.
    """
    fig.canvas.draw()
    width_pt, height_pt = fig.get_size_inches() * 72
    rows, warnings = [], []
    for group in groups:
        values = []
        for ax in group["axes"]:
            bbox = ax.get_position()
            values.append({"left": bbox.x0 * width_pt, "right": bbox.x1 * width_pt,
                           "bottom": bbox.y0 * height_pt, "top": bbox.y1 * height_pt,
                           "width": bbox.width * width_pt,
                           "height": bbox.height * height_pt})
        spreads = {prop: max(v[prop] for v in values) - min(v[prop] for v in values)
                   for prop in group["properties"]}
        for prop, spread in spreads.items():
            if spread > tolerance_pt:
                warnings.append(f"{group['name']}: {prop} differs by {spread:.2f} pt")
        rows.append({"name": group["name"], "plot_area_pt": values,
                     "property_spread_pt": spreads})
    return {"tolerance_pt": tolerance_pt, "groups": rows, "warnings": warnings,
            "scope": "Explicit comparable plot areas; does not certify all figure geometry"}


def annotated_heatmap(ax, values, column_labels, row_labels, *,
                      annotations=None, cmap="cividis", vmin=None, vmax=None,
                      fontsize=None):
    """Require explicit shared limits for compared matrices; label actual
    values independently from the displayed color normalization."""
    import numpy as np
    from matplotlib.colors import to_rgb
    values = np.asarray(values, dtype=float)
    if values.shape != (len(row_labels), len(column_labels)):
        raise ValueError("Heatmap labels must match matrix dimensions")
    if annotations is None:
        annotations = [[f"{v:g}" for v in row] for row in values]
    if np.shape(annotations) != values.shape:
        raise ValueError("Annotations must match matrix dimensions")
    im = ax.imshow(np.ma.masked_invalid(values), cmap=cmap, vmin=vmin,
                   vmax=vmax, interpolation="nearest", aspect="auto")
    ax.set_xticks(range(len(column_labels)), column_labels)
    ax.set_yticks(range(len(row_labels)), row_labels)
    ax.tick_params(length=0, pad=7)
    ax.set_xticks(np.arange(-0.5, len(column_labels), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(row_labels), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=2.5)
    ax.tick_params(which="minor", length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    for (i, j), value in np.ndenumerate(values):
        if not np.isfinite(value):
            label, color = "NA", COLORS["ink"]
        else:
            rgb = np.array(to_rgb(im.cmap(im.norm(value))))
            rgb = np.where(rgb <= 0.04045, rgb / 12.92,
                           ((rgb + 0.055) / 1.055) ** 2.4)
            luminance = float(rgb @ [0.2126, 0.7152, 0.0722])
            # Choose the stronger white/ink contrast against each cell.
            color = "white" if luminance < 0.22 else COLORS["ink"]
            label = annotations[i][j]
        ax.text(j, i, label, ha="center", va="center", color=color,
                fontsize=fontsize, linespacing=1.5)
    return im


def dumbbell(ax, positions, first, second, *, labels=("Answered-max", "Full-max")):
    """Larger open squares + smaller filled circles remain visible when equal.
    first/second are score vectors, never indices hard-coded into axis positions.
    """
    import numpy as np
    first, second = np.asarray(first, float), np.asarray(second, float)
    positions = np.asarray(positions, float)
    if first.shape != second.shape or first.shape != positions.shape:
        raise ValueError("Dumbbell vectors must have equal shape")
    for y, a, b in zip(positions, first, second):
        ax.plot([a, b], [y, y], color=COLORS["neutral"], lw=1.8, zorder=2)
    ax.scatter(second, positions, s=68, marker="s", facecolors="white",
               edgecolors=COLORS["alternative"], linewidths=1.4,
               label=labels[1], zorder=3)
    ax.scatter(first, positions, s=23, marker="o", color=COLORS["primary"],
               label=labels[0], zorder=4)
    clean_axes(ax, "x")


def interval_plot(ax, positions, center, low, high, *, label="Equal weights"):
    """Draw supplied intervals; caller declares whether CI, percentiles,
    parameter sensitivity, or another measure. No automatic estimation.
    """
    import numpy as np
    positions, center, low, high = map(lambda v: np.asarray(v, float),
                                     (positions, center, low, high))
    if not (positions.shape == center.shape == low.shape == high.shape):
        raise ValueError("Interval vectors must have equal shape")
    if np.any(low > high):
        raise ValueError("Interval lower endpoint exceeds upper endpoint")
    ax.hlines(positions, low, high, color=COLORS["range"], linewidth=2.0, zorder=2)
    ax.vlines(low, positions - 0.055, positions + 0.055,
               color=COLORS["range"], linewidth=1.0)
    ax.vlines(high, positions - 0.055, positions + 0.055,
               color=COLORS["range"], linewidth=1.0)
    ax.scatter(center, positions, s=26, color=COLORS["primary"],
               label=label, zorder=3)
    clean_axes(ax, "x")


def time_band(ax, x, center, low, high, *, label, color=None):
    """Show supplied uncertainty with explicit gaps; smoothing is not applied.
    This helper does not infer a sampling unit, interval, or sample size.
    """
    import numpy as np
    x, center, low, high = map(lambda v: np.asarray(v, float), (x, center, low, high))
    if not (x.shape == center.shape == low.shape == high.shape):
        raise ValueError("Time-series vectors must have equal shape")
    if np.any(low > high):
        raise ValueError("Interval lower endpoint exceeds upper endpoint")
    color = color or COLORS["primary"]
    ax.fill_between(x, low, high, color=color, alpha=0.16, linewidth=0)
    ax.plot(x, center, color=color, label=label)
    clean_axes(ax, "y")


def export_figure(fig, stem, *, sources, description, transformations=(),
                  interval_definition="none", dpi=300):
    """Update the requested outputs in place; preserve exact canvas size.
    Writes source hashes and narrow mechanical checks, not an aesthetic pass.
    """
    import matplotlib
    from matplotlib.text import Text
    from PIL import Image
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    records = []
    for source in sources:
        path = Path(source).resolve()
        records.append({"path": str(path),
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    canvas = fig.bbox
    warnings, font_sizes, text_boxes = [], [], []
    undrawn_tick_labels = set()
    for ax in fig.axes:
        for axis, limits in ((ax.xaxis, ax.get_xlim()), (ax.yaxis, ax.get_ylim())):
            left, right = sorted(limits)
            for tick in axis.get_major_ticks() + axis.get_minor_ticks():
                # Locators may create tick artists beyond the viewport; those
                # are not drawn and must not generate false clipping warnings.
                if not axis.get_visible() or not left <= tick.get_loc() <= right:
                    undrawn_tick_labels.update((id(tick.label1), id(tick.label2)))
    for text in fig.findobj(Text):
        if (id(text) in undrawn_tick_labels or not text.get_visible()
                or not text.get_text().strip()):
            continue
        font_sizes.append(float(text.get_fontsize()))
        bounds = text.get_window_extent(renderer)
        if bounds.width > 0 and bounds.height > 0:
            text_boxes.append((text.get_text(), bounds))
        if (bounds.x0 < canvas.x0 - 1 or bounds.y0 < canvas.y0 - 1 or
                bounds.x1 > canvas.x1 + 1 or bounds.y1 > canvas.y1 + 1):
            warnings.append("Potential clipping: " + text.get_text())
    # This is a screen, not a complete layout verdict: renderer bounds can
    # overstate glyph intersections and cannot detect marks hiding each other.
    from matplotlib.transforms import Bbox
    for i, (label, box) in enumerate(text_boxes):
        for other_label, other_box in text_boxes[i + 1:]:
            intersection = Bbox.intersection(box, other_box)
            if intersection is not None and intersection.width > 1 and intersection.height > 1:
                warnings.append(f"Potential text overlap: {label!r} / {other_label!r}")
    for extension in ("png", "pdf", "svg"):
        fig.savefig(stem.with_suffix("." + extension), dpi=dpi, bbox_inches=None)
    output_hashes = {str(stem.with_suffix("." + ext).resolve()):
                     hashlib.sha256(stem.with_suffix("." + ext).read_bytes()).hexdigest()
                     for ext in ("png", "pdf", "svg")}
    width, height = map(float, fig.get_size_inches())
    with Image.open(stem.with_suffix(".png")) as raster:
        pixels = list(raster.size)
        stored_dpi = raster.info.get("dpi")
    expected = [round(width * dpi), round(height * dpi)]
    if any(abs(a - b) > 1 for a, b in zip(pixels, expected)):
        warnings.append("PNG dimensions differ from intended physical dimensions")
    manifest = {
        "description": description, "sources": records,
        "transformations": list(transformations),
        "interval_definition": interval_definition,
        "matplotlib_version": matplotlib.__version__,
        "size_inches": [width, height], "png_pixels": pixels,
        "png_dpi": stored_dpi, "minimum_visible_font_pt": min(font_sizes, default=None),
        "outputs": [str(stem.with_suffix("." + ext).resolve())
                    for ext in ("png", "pdf", "svg")],
        "output_sha256": output_hashes,
        "helper_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "mechanical_warnings": warnings,
        "visual_review": "pending; inspect actual PNG and intended manuscript size",
        "release_gate": "pending; seal the spec, inputs/code/helper, caption and outputs in a figure review record",
        "svg_note": "Text is editable; matching fonts are required to preserve appearance.",
    }
    stem.with_suffix(".audit.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest
