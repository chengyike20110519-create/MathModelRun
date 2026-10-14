"""Generate all paper figures from run results (visualization_plan.json).

Usage: python3 code/make_figures.py            # all figures
"""

import json
import sys
import heapq
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).parent))
from buildings import build_basic, build_scenario_b, build_scenario_c  # noqa: E402
from sweep import clear_cache, exact_basic_two, route_time  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "results" / "runs"
FIGS = ROOT / "figures"
RUN_TAG = "run:exp-001..005"

C_PRIO = {1: "#9ecae1", 2: "#fdae6b", 3: "#f768a1"}


def sp_path(b, src, dst, walk_speed=1.2):
    """Shortest path node sequence from src to dst (Dijkstra)."""
    dist = {src: 0.0}
    prev = {src: None}
    pq = [(0.0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float("inf")):
            continue
        if u == dst:
            break
        for v, duv in b.edges[u].items():
            nd = d + duv / walk_speed
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    path = []
    cur = dst
    while cur is not None:
        path.append(cur)
        cur = prev.get(cur)
    return list(reversed(path))


def load(run, name="metrics.json"):
    return json.loads((RUNS / run / name).read_text())


def draw_building(ax, b, title):
    for nid, (x, y, fl) in b.nodes.items():
        if nid[0] == "room":
            rid = nid[1]
            r = b.rooms[rid]
            ax.add_patch(Rectangle((x - 2.4, y - 1.6), 4.8, 3.2,
                                   facecolor=C_PRIO[r["priority"]],
                                   edgecolor="k", lw=0.8))
            ax.text(x, y, f"{rid}\n{r['check_time']:.0f}s", ha="center",
                    va="center", fontsize=7)
        elif nid[0] == "exit":
            ax.plot(x, y, "g^", ms=10)
            ax.text(x, y - 0.9, "EXIT", ha="center", fontsize=7, color="g")
        elif nid[0] == "stair":
            ax.plot(x, y, "ks", ms=6)
            ax.text(x, y - 0.9, "STAIR", ha="center", fontsize=6)
    for a, nbrs in b.edges.items():
        ax.plot, None
        for c in nbrs:
            if a < c:
                x1, y1, _ = b.nodes[a]
                x2, y2, _ = b.nodes[c]
                ax.plot([x1, x2], [y1, y2], "k-", lw=0.6, alpha=0.5)
    ax.set_title(title, fontsize=10)
    ax.set_aspect("equal")
    ax.axis("off")


def fig1():
    b = build_basic()
    clear_cache()
    ms, (orders, s0, s1) = exact_basic_two(b)
    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    draw_building(ax, b, "")
    colors = ["#08519c", "#cb181d"]
    for i, (order, start) in enumerate([(orders[0], s0), (orders[1], s1)]):
        seq = [start]
        for rid in order:
            seq.append(("room", rid))
        end = min(b.exits,
                  key=lambda e: route_time(b, ("room", order[-1]), [], e))
        seq.append(end)
        xs, ys = [], []
        for a, c in zip(seq, seq[1:]):
            for node in sp_path(b, a, c):
                xs.append(b.nodes[node][0])
                ys.append(b.nodes[node][1])
        xs.insert(0, b.nodes[start][0])
        ys.insert(0, b.nodes[start][1])
        ax.plot(xs, ys, "-", color=colors[i], lw=2.2,
                label=f"R{i+1}: {'→'.join(order)} ({ms:.0f}s sweep)")
    ax.set_title(f"Basic scenario (Figure 1) — optimal 2-responder sweep, "
                 f"makespan = {ms:.1f} s", fontsize=11)
    ax.legend(fontsize=8, loc="upper center",
              bbox_to_anchor=(0.5, -0.02), ncol=2, frameon=False)
    fig.text(0.99, 0.01, RUN_TAG, fontsize=6, ha="right", color="gray")
    fig.savefig(FIGS / "fig1_basic_scenario.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig2():
    """Gantt timeline of the optimal 2-FF sweep."""
    b = build_basic()
    clear_cache()
    ms, (orders, s0, s1) = exact_basic_two(b)
    fig, ax = plt.subplots(figsize=(7, 2.8))
    for i, (order, start) in enumerate([(orders[0], s0), (orders[1], s1)]):
        t = 0.0
        cur = start
        for rid in order:
            node = ("room", rid)
            walk = route_time(b, cur, [], node)
            chk = b.rooms[rid]["check_time"]
            ax.barh(i, walk, left=t, color="#c6dbef", edgecolor="k", lw=0.4)
            ax.barh(i, chk, left=t + walk, color="#08519c", edgecolor="k",
                    lw=0.4)
            ax.text(t + walk + chk / 2, i, rid, ha="center", va="center",
                    fontsize=7, color="w")
            t += walk + chk
            cur = node
        fin = route_time(b, cur, [], min(
            b.exits, key=lambda e: route_time(b, cur, [], e)))
        ax.barh(i, fin, left=t, color="#c6dbef", edgecolor="k", lw=0.4)
        ax.text(t + fin + 2, i, f"exit {t + fin:.0f}s", va="center",
                fontsize=8)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Responder 1 (Exit W)", "Responder 2 (Exit E)"])
    ax.set_xlabel("time (s)")
    ax.set_title(f"Sweep timeline — makespan {ms:.1f} s")
    ax.axvline(ms, color="r", ls="--", lw=1)
    fig.text(0.99, 0.01, RUN_TAG, fontsize=6, ha="right", color="gray")
    fig.savefig(FIGS / "fig2_sweep_timeline.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig3():
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))
    for ax, (fn, title) in zip(axes, [
            (build_basic, "A: 1-floor office (6 rooms)"),
            (build_scenario_b, "B: 2-floor daycare + office (11 rooms)"),
            (build_scenario_c, "C: 3-floor mixed-use (13 rooms)")]):
        draw_building(ax, fn(), title)
    handles = [Rectangle((0, 0), 1, 1, facecolor=c, edgecolor="k")
               for c in [C_PRIO[1], C_PRIO[2], C_PRIO[3]]]
    fig.legend(handles, ["priority 1 (office)", "priority 2 (lobby/warehouse/"
                         "conference)", "priority 3 (daycare/labs)"],
               loc="lower center", ncol=3, fontsize=8)
    fig.suptitle("Building layouts (node color = occupant priority; label = "
                 "room id + check time)", fontsize=10)
    fig.text(0.99, 0.01, RUN_TAG, fontsize=6, ha="right", color="gray")
    fig.savefig(FIGS / "fig3_scenarios.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig4():
    sc_a = load("exp-001")["responder_scaling_s"]
    sc_b = load("exp-002-B")["responder_scaling_s"]
    sc_c = load("exp-002-C")["responder_scaling_s"]
    fig, ax = plt.subplots(figsize=(6, 4))
    for sc, label, mk in [(sc_a, "A: 1-floor office (6 rooms)", "o"),
                          (sc_b, "B: 2-floor daycare (11 rooms)", "s"),
                          (sc_c, "C: 3-floor mixed-use (13 rooms)", "^")]:
        ks = sorted(int(k) for k in sc)
        ax.plot(ks, [sc[str(k)] for k in ks], mk + "-", label=label, lw=1.5)
    ax.set_xlabel("number of responders")
    ax.set_ylabel("minimum sweep time (s)")
    ax.set_title("Responder scaling: diminishing returns mark the optimum")
    ax.legend(fontsize=8, loc="upper center",
              bbox_to_anchor=(0.5, -0.12), ncol=3, frameon=False)
    ax.grid(alpha=0.3)
    fig.text(0.99, 0.01, RUN_TAG, fontsize=6, ha="right", color="gray")
    fig.savefig(FIGS / "fig4_responder_scaling.png", dpi=300,
                bbox_inches="tight")
    plt.close(fig)


def fig5():
    m = load("exp-005")
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    sk = m["smoke_level_curve_s"]
    axes[0].plot([float(k) for k in sk], [sk[k] for k in sk], "o-", lw=1.5,
                 color="#7f2704")
    axes[0].set_xlabel("smoke level (0 = clear, 1 = dense)")
    axes[0].set_ylabel("mean sweep time (s)")
    axes[0].set_title("Smoke reduces walking speed (P6)")
    cm = m["comm_fail_curve_s"]
    axes[1].plot([float(k) for k in cm], [cm[k] for k in cm], "s-", lw=1.5,
                 color="#08306b")
    axes[1].set_xlabel("per-room communication failure probability")
    axes[1].set_ylabel("mean sweep time (s)")
    axes[1].set_title("Communication failure adds retry delay (P7)")
    for ax in axes:
        ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.text(0.99, 0.01, RUN_TAG, fontsize=6, ha="right", color="gray")
    fig.savefig(FIGS / "fig5_smoke_impact.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig6():
    samples = json.loads((RUNS / "exp-003" / "raw_samples.json").read_text())
    det = load("exp-003")["deterministic_no_constraints_s"]
    fig, ax = plt.subplots(figsize=(6, 3.4))
    ax.hist(samples, bins=25, color="#3182bd", edgecolor="k", lw=0.4)
    ax.axvline(det, color="g", ls="--", lw=1.5,
               label=f"unconstrained optimum ({det:.0f}s)")
    ax.set_xlabel("sweep time (s), 200 Monte Carlo samples")
    ax.set_ylabel("count")
    ax.set_title("Scenario B under combined constraints (smoke + comms + "
                 "occupancy)")
    ax.legend(fontsize=8)
    fig.text(0.99, 0.01, RUN_TAG, fontsize=6, ha="right", color="gray")
    fig.savefig(FIGS / "fig6_mc_distribution.png", dpi=300,
                bbox_inches="tight")
    plt.close(fig)


def fig7():
    b = load("exp-004-B")
    c = load("exp-004-C")
    fig, (ax, ax2) = plt.subplots(
        1, 2, figsize=(9.0, 3.65), gridspec_kw={"width_ratios": [2.05, 1.0]}
    )
    fig.subplots_adjust(left=0.07, right=0.98, bottom=0.15, top=0.84,
                        wspace=0.27)

    conditions = [
        ("no_tech_s", "0% sensors", "#E76F51"),
        ("sensor50_s", "50% sensors", "#F2B134"),
        ("sensor100_s", "100% sensors", "#2A9D8F"),
    ]
    x = np.arange(2)
    w = 0.23
    for i, (key, label, color) in enumerate(conditions):
        vals = [b[key], c[key]]
        bars = ax.bar(x + (i - 1) * w, vals, w, color=color, label=label,
                      edgecolor="white", linewidth=0.8, zorder=3)
        ax.bar_label(bars, labels=[f"{v:.1f}" for v in vals], padding=3,
                     fontsize=8, fontweight="bold", color="#24313A")

    ax.set_xticks(x)
    ax.set_xticklabels(["B  daycare\n(k = 5)", "C  mixed-use\n(k = 5)"],
                       fontsize=9, fontweight="bold", color="#24313A")
    ax.set_ylabel("minimum sweep time (s)", fontsize=9, color="#24313A")
    ax.set_ylim(0, 235)
    ax.set_yticks([0, 50, 100, 150, 200])
    ax.grid(axis="y", color="#DCE6F1", linewidth=0.8, zorder=0)
    ax.tick_params(axis="y", labelsize=8, colors="#52616B")
    ax.tick_params(axis="x", length=0)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.16), ncol=3,
              frameon=False, fontsize=8, handlelength=1.0, columnspacing=1.2)
    ax.set_title("Absolute sweep time", loc="left", fontsize=11,
                 fontweight="bold", color="#17324D", pad=24)

    for xi, scenario, color in zip(
            x, [b, c], ["#1769AA", "#D6336C"]):
        saving = scenario["no_tech_s"] - scenario["sensor100_s"]
        ax.annotate(
            f"-{scenario['reduction100_pct']:.1f}%  ({saving:.1f} s)",
            xy=(xi, scenario["no_tech_s"] + 8), ha="center", va="bottom",
            fontsize=8.5, fontweight="bold", color=color,
            bbox=dict(boxstyle="round,pad=0.22", fc="white", ec=color,
                      lw=0.8, alpha=0.95),
        )

    coverage_x = np.arange(3)
    b_vals = np.array([b[k] for k, _, _ in conditions])
    c_vals = np.array([c[k] for k, _, _ in conditions])
    b_pct = (b_vals / b_vals[0] - 1.0) * 100
    c_pct = (c_vals / c_vals[0] - 1.0) * 100
    b_pct[-1] = -b["reduction100_pct"]
    c_pct[-1] = -c["reduction100_pct"]

    ax2.axhline(0, color="#94A3B8", linewidth=0.9, linestyle="--", zorder=1)
    ax2.plot(coverage_x, b_pct, "-o", color="#1769AA", linewidth=2.2,
             markersize=6.5, markerfacecolor="white", markeredgewidth=2,
             label="B  daycare", zorder=3)
    ax2.plot(coverage_x, c_pct, "-s", color="#D6336C", linewidth=2.2,
             markersize=6.5, markerfacecolor="white", markeredgewidth=2,
             label="C  mixed-use", zorder=3)
    for xi, yb, yc in zip(coverage_x, b_pct, c_pct):
        ax2.text(xi, yb - 1.45, f"{yb:.1f}%", ha="center", va="top",
                 fontsize=7.5, color="#1769AA", fontweight="bold")
        ax2.text(xi, yc + 1.45, f"{yc:.1f}%", ha="center", va="bottom",
                 fontsize=7.5, color="#D6336C", fontweight="bold")

    ax2.set_xticks(coverage_x)
    ax2.set_xticklabels(["0%", "50%", "100%"], fontsize=8.5,
                        fontweight="bold", color="#24313A")
    ax2.set_xlabel("sensor coverage", fontsize=9, color="#24313A")
    ax2.set_ylabel("change vs. 0% sensors", fontsize=9, color="#24313A")
    ax2.set_xlim(-0.18, 2.18)
    ax2.set_ylim(-27, 5)
    ax2.set_yticks([-25, -20, -15, -10, -5, 0])
    ax2.set_yticklabels([f"{v}%" for v in [-25, -20, -15, -10, -5, 0]],
                        fontsize=8, color="#52616B")
    ax2.tick_params(length=0)
    ax2.grid(axis="y", color="#F0DCE7", linewidth=0.8, zorder=0)
    ax2.legend(loc="lower left", frameon=False, fontsize=8,
               handlelength=1.2, labelspacing=0.35)
    ax2.set_title("Relative reduction", loc="left", fontsize=11,
                  fontweight="bold", color="#17324D", pad=24)
    ax2.text(0.0, 1.14,
             "Stable benefit across very different buildings",
             transform=ax2.transAxes, ha="left", va="bottom", fontsize=8.2,
             color="#52616B")

    for panel in (ax, ax2):
        panel.set_facecolor("#FBFCFE")
        panel.spines[["top", "right", "left", "bottom"]].set_visible(False)

    fig.suptitle("Building automation compresses the sweep without changing "
                 "the staffing recommendation", x=0.07, y=0.97, ha="left",
                 fontsize=12, fontweight="bold", color="#17324D")
    fig.text(0.99, 0.015, RUN_TAG, fontsize=6, ha="right", color="gray")
    fig.savefig(FIGS / "fig7_technology.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    FIGS.mkdir(exist_ok=True)
    for fn in (fig1, fig2, fig3, fig4, fig5, fig6, fig7):
        fn()
        print(f"[figures] {fn.__name__} done")
