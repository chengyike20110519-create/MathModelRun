"""Publication-oriented figures for the frozen HiMCM experiment."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


INK = "#17212b"
MUTED = "#5f6b76"
GRID = "#dbe2e8"
TEAL = "#087f8c"
CORAL = "#d86651"
GOLD = "#c88a22"
BLUE = "#2d5f8b"
GREEN = "#3a8066"
PALETTE = ["#087f8c", "#2d5f8b", "#c88a22", "#d86651"]


def style() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9.2,
        "axes.titlesize": 12.2,
        "axes.titleweight": "bold",
        "axes.labelsize": 9.5,
        "axes.labelcolor": INK,
        "axes.edgecolor": "#93a1ac",
        "axes.linewidth": 0.75,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelsize": 8.2,
        "ytick.labelsize": 8.2,
        "legend.fontsize": 8.0,
        "figure.facecolor": "white",
        "axes.facecolor": "#fbfcfd",
        "savefig.dpi": 220,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.12,
    })


def finish(fig: plt.Figure, path: Path) -> None:
    fig.savefig(path, facecolor="white")
    fig.savefig(path.with_suffix(".svg"), facecolor="white")
    plt.close(fig)


def draw_figures(
    figure_dir: Path,
    years: np.ndarray,
    values: np.ndarray,
    train_years: np.ndarray,
    test_years: np.ndarray,
    all_years: np.ndarray,
    forecast_years: np.ndarray,
    linear_all: np.ndarray,
    exponential_all: np.ndarray,
    logistic_all: np.ndarray,
    linear_forecast: np.ndarray,
    exponential_forecast: np.ndarray,
    logistic_forecast: np.ndarray,
    target: float,
    rolling_years: np.ndarray,
    rolling_values: np.ndarray,
    maximum: dict[str, float | int],
    temp_years: np.ndarray,
    temp_values: np.ndarray,
    temp_fit: np.ndarray,
    temp_forecast: np.ndarray,
    thresholds: dict[str, dict[str, float | list[float]]],
    shared_co2: np.ndarray,
    shared_temp: np.ndarray,
    correlation: float,
    sensitivity: dict[str, dict[str, float]],
) -> None:
    style()
    figure_dir.mkdir(parents=True, exist_ok=True)

    # Figure 1: model comparison with an explicit train/test hand-off.
    fig, ax = plt.subplots(figsize=(8.55, 4.55))
    ax.axvspan(years[0], test_years[0], color="#eef4f5", zorder=0)
    ax.axvspan(test_years[0], years[-1], color="#fff1ed", zorder=0)
    ax.axvline(test_years[0], color=CORAL, lw=1.1, ls=(0, (4, 3)), zorder=2)
    ax.plot(years, values, color=INK, lw=1.35, marker="o", ms=2.6, label="Observed", zorder=5)
    ax.plot(years, linear_all, color=TEAL, lw=1.5, label="Linear")
    ax.plot(years, exponential_all, color=BLUE, lw=1.5, label="Exponential")
    ax.plot(years, logistic_all, color=GOLD, lw=1.5, label="Logistic")
    ax.plot(forecast_years, linear_forecast, color=TEAL, lw=1.5, ls="--")
    ax.plot(forecast_years, exponential_forecast, color=BLUE, lw=1.5, ls="--")
    ax.plot(forecast_years, logistic_forecast, color=GOLD, lw=1.5, ls="--")
    ax.axhline(target, color="#8b5960", lw=0.9, ls=(0, (2, 2)))
    ax.text(2099, target + 5, "685 ppm target", ha="right", color="#8b5960", fontsize=8)
    ax.text(1981, 595, "TRAIN", color=TEAL, weight="bold", fontsize=8)
    ax.text(2014, 595, "HOLDOUT", color=CORAL, weight="bold", fontsize=8)
    ax.set(xlim=(1957, 2102), ylim=(295, 720), xlabel="Year", ylabel="CO2 concentration (ppm)",
           title="Model comparison and long-horizon extrapolation")
    ax.grid(axis="y", color=GRID, lw=0.65)
    ax.spines[["top", "right"]].set_visible(False)
    handles = [Line2D([0], [0], color=INK, marker="o", ms=3, lw=1.4, label="Observed"),
               Line2D([0], [0], color=TEAL, lw=1.5, label="Linear"),
               Line2D([0], [0], color=BLUE, lw=1.5, label="Exponential"),
               Line2D([0], [0], color=GOLD, lw=1.5, label="Logistic"),
               Line2D([0], [0], color=INK, lw=1.5, ls="--", label="Forecast")]
    ax.legend(handles=handles, ncol=5, loc="upper left", frameon=False, bbox_to_anchor=(0, 1.02))
    finish(fig, figure_dir / "fig1_co2_fits.png")

    # Figure 2: a compact temporal heat strip plus ranked window evidence.
    fig = plt.figure(figsize=(8.55, 3.85), constrained_layout=True)
    gs = fig.add_gridspec(2, 1, height_ratios=(1.0, 3.1), hspace=0.12)
    ax0 = fig.add_subplot(gs[0])
    heat = rolling_values[np.newaxis, :]
    cmap = LinearSegmentedColormap.from_list("window", ["#e8f1f2", "#78b7b1", "#d86651"])
    ax0.imshow(heat, aspect="auto", cmap=cmap, extent=(rolling_years[0] - .5, rolling_years[-1] + .5, 0, 1))
    ax0.set(yticks=[], xlim=(rolling_years[0] - .5, rolling_years[-1] + .5), title="Ten-year change intensity")
    ax0.set_xticks([1969, 1979, 1989, 1999, 2009, 2019])
    ax0.tick_params(axis="x", labelbottom=False, length=0)
    for spine in ax0.spines.values(): spine.set_visible(False)
    ax = fig.add_subplot(gs[1])
    colors = np.where(rolling_values >= np.percentile(rolling_values, 75), CORAL, TEAL)
    ax.fill_between(rolling_years, rolling_values, color="#dcecef", alpha=.8, step="mid")
    ax.plot(rolling_years, rolling_values, color=TEAL, lw=1.2, marker="o", ms=2.6)
    peak = int(np.argmax(rolling_values))
    ax.scatter(rolling_years[peak], rolling_values[peak], s=42, color=CORAL, zorder=4)
    ax.annotate(f"Maximum: {int(maximum['start_year'])}-{int(maximum['end_year'])}\n{maximum['increase']:.2f} ppm",
                xy=(rolling_years[peak], rolling_values[peak]), xytext=(2010, rolling_values[peak] + 4.0),
                arrowprops=dict(arrowstyle="-", color=CORAL, lw=.9), color=CORAL, fontsize=8.2, ha="left")
    ref = np.where(rolling_years == 2004)[0][0]
    ax.scatter(rolling_years[ref], rolling_values[ref], s=30, color=GOLD, zorder=4)
    ax.annotate("1994-2004 reference", xy=(2004, rolling_values[ref]), xytext=(1991, rolling_values[ref] - 4.2),
                arrowprops=dict(arrowstyle="-", color=GOLD, lw=.8), color="#916719", fontsize=8)
    ax.set(xlabel="Window end year", ylabel="Change over 10 years (ppm)", title="Acceleration is concentrated in the latest window")
    ax.grid(axis="y", color=GRID, lw=.65); ax.spines[["top", "right"]].set_visible(False)
    finish(fig, figure_dir / "fig2_tenyear.png")

    # Figure 3: chronology is encoded in point color and shown directly.
    fig, ax = plt.subplots(figsize=(7.25, 4.65))
    points = ax.scatter(shared_co2, shared_temp, c=np.linspace(1959, 2021, len(shared_co2)), cmap="viridis",
                        s=30, alpha=.9, edgecolors="white", linewidth=.35, zorder=3)
    slope, intercept = np.polyfit(shared_co2, shared_temp, 1)
    xx = np.linspace(shared_co2.min() - 4, shared_co2.max() + 7, 80)
    ax.plot(xx, intercept + slope * xx, color=CORAL, lw=1.8, zorder=2)
    for yr in (1959, 1980, 2000, 2021):
        idx = int(np.argmin(np.abs((1959 + np.arange(len(shared_co2))) - yr)))
        ax.annotate(str(yr), (shared_co2[idx], shared_temp[idx]), xytext=(5, 5), textcoords="offset points", fontsize=7.7, color=INK)
    ax.text(.04, .94, f"Pearson r = {correlation:.3f}", transform=ax.transAxes, color=CORAL, weight="bold", fontsize=9)
    cbar = fig.colorbar(points, ax=ax, pad=.02); cbar.set_label("Observation year", rotation=270, labelpad=15)
    ax.set(xlabel="CO2 concentration (ppm)", ylabel="Temperature anomaly (deg C)", title="A strong association with a visible time trajectory")
    ax.grid(color=GRID, lw=.65); ax.spines[["top", "right"]].set_visible(False)
    finish(fig, figure_dir / "fig3_scatter.png")

    # Figure 4: uncertainty is represented as horizontal year intervals.
    fig, ax = plt.subplots(figsize=(8.55, 4.25))
    ax.plot(temp_years, temp_values, color=INK, lw=1.15, marker="o", ms=2.2, label="Observed")
    ax.plot(temp_years, temp_fit, color=CORAL, lw=1.5, label="Linear trend")
    ax.plot(forecast_years, temp_forecast, color=CORAL, lw=1.5, ls="--")
    threshold_colors = {"1.25": TEAL, "1.5": GOLD, "2.0": CORAL}
    for key, item in thresholds.items():
        y = float(key); color = threshold_colors[key]
        ci = item["ci95_years"]
        ax.axhline(y, color=color, lw=.8, alpha=.55)
        ax.fill_between([float(ci[0]), float(ci[1])], y - .035, y + .035, color=color, alpha=.28)
        ax.axvline(float(item["year"]), color=color, lw=.8, ls=(0, (2, 3)), alpha=.8)
        ax.text(float(item["year"]) + 1.1, y + .035, f"{y:.2f} deg C  |  {float(item['year']):.1f}", color=color, fontsize=7.9, va="bottom")
    ax.set(xlim=(1957, 2102), ylim=(.25, 2.28), xlabel="Year", ylabel="Temperature anomaly (deg C)", title="Threshold timing under the fitted temperature trend")
    ax.grid(axis="y", color=GRID, lw=.65); ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, ncol=3, loc="upper left", bbox_to_anchor=(0, 1.02))
    finish(fig, figure_dir / "fig4_temp_threshold.png")

    # Figure 5: two forecast horizons make the rate sensitivity legible.
    fig, axes = plt.subplots(1, 2, figsize=(8.55, 3.8), sharey=True)
    labels = ["-10% rate", "Baseline", "+10% rate"]
    keys = ["minus_10_percent_rate", "baseline_rate", "plus_10_percent_rate"]
    colors = [TEAL, BLUE, CORAL]
    for ax, horizon in zip(axes, ("forecast_2050", "forecast_2100")):
        vals = [sensitivity[key][horizon] for key in keys]
        bars = ax.bar(labels, vals, color=colors, width=.62, edgecolor="white", linewidth=.8)
        for bar, value in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, value + 3, f"{value:.1f}", ha="center", va="bottom", fontsize=8.4, color=INK)
        ax.set_title(horizon.replace("forecast_", "").upper())
        ax.grid(axis="y", color=GRID, lw=.65); ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(axis="x", rotation=18)
    axes[0].set_ylabel("CO2 forecast (ppm)")
    fig.suptitle("Small rate changes compound over the forecast horizon", x=.08, ha="left", y=1.03, fontsize=12.2, fontweight="bold", color=INK)
    finish(fig, figure_dir / "fig5_sensitivity.png")
