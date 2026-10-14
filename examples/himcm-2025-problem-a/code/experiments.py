"""S5 experiment driver for 2025 HiMCM Problem A.

Runs:
  exp-001  Q2 basic scenario, responder scaling k=1..4 (exact k<=2)
  exp-002  Q3 scenarios B and C, responder scaling k=1..6 (heuristic)
  exp-003  Q4a Monte Carlo constraints on scenario B (200 samples)
  exp-004  Q4b technology levels on scenarios B and C

Every run writes results/runs/<id>/params.json + metrics.json.
"""

import itertools
import json
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from buildings import (STAIR_TIME, WALK_SPEED, build_basic, build_scenario_b,
                       build_scenario_c)
from sweep import (clear_cache, greedy_single, route_time, shortest_path_time,
                   sweep_partition)

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "results" / "runs"
SEED = 20251105


def save_run(run_id, params, metrics):
    d = RUNS / run_id
    d.mkdir(parents=True, exist_ok=True)
    (d / "params.json").write_text(json.dumps(params, indent=2))
    (d / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print(f"[{run_id}] saved: {d}")


# ---------------------------------------------------------------- optimize

def route_time_full(b, start, rooms_order, end, walk_speed):
    """Route time honoring per-room check_time and priority-3 rooms before
    others is handled by ordering input."""
    t = 0.0
    cur = start
    for rid in rooms_order:
        clear_cache()
        node = ("room", rid)
        t += shortest_path_time(b, cur, node, walk_speed)
        t += b.rooms[rid]["check_time"]
        cur = node
    clear_cache()
    t += shortest_path_time(b, cur, end, walk_speed)
    return t


def resp_time(b, start, rooms_order, walk_speed):
    """Responder finishes at the exit nearest to the last room."""
    return min(route_time_full(b, start, rooms_order, e, walk_speed)
               for e in b.exits)


def makespan(b, routes, starts, walk_speed):
    times = [resp_time(b, starts[r], routes[r], walk_speed)
             for r in range(len(routes))]
    return max(times) if times else 0.0, times


def initial_routes(b, k, rooms, walk_speed):
    """Priority-desc greedy insertion: sort rooms by priority desc, insert
    each into the responder+position with smallest makespan increase.
    Responders start at distinct exits when k <= len(exits)."""
    starts = [b.exits[i % len(b.exits)] for i in range(k)]
    routes = [[] for _ in range(k)]
    for rid in sorted(rooms, key=lambda r: -b.rooms[r]["priority"]):
        best = None
        for r in range(k):
            for pos in range(len(routes[r]) + 1):
                trial = [rt[:] for rt in routes]
                trial[r].insert(pos, rid)
                ms, _ = makespan(b, trial, starts, walk_speed)
                if best is None or ms < best[0]:
                    best = (ms, r, pos)
        _, r, pos = best
        routes[r].insert(pos, rid)
    return routes, starts


def local_search(b, routes, starts, walk_speed, max_passes=40):
    """Swap/move rooms between routes until no improvement."""
    best_ms, _ = makespan(b, routes, starts, walk_speed)
    for _ in range(max_passes):
        improved = False
        for r1 in range(len(routes)):
            for r2 in range(len(routes)):
                if r1 == r2:
                    continue
                for i, rid in enumerate(list(routes[r1])):
                    for pos in range(len(routes[r2]) + 1):
                        trial = [rt[:] for rt in routes]
                        trial[r1].remove(rid)
                        trial[r2].insert(pos, rid)
                        ms, _ = makespan(b, trial, starts, walk_speed)
                        if ms < best_ms - 1e-9:
                            routes = trial
                            best_ms = ms
                            improved = True
                            break
                    if improved:
                        break
                if improved:
                    break
            if improved:
                break
        if not improved:
            break
    return routes, best_ms


def optimize_k(b, k, rooms, walk_speed=WALK_SPEED):
    routes, starts = initial_routes(b, k, rooms, walk_speed)
    routes, ms = local_search(b, routes, starts, walk_speed)
    return ms, routes, starts


def exact_k1_k2_basic(b):
    rooms = sorted(b.rooms)
    out = {}
    # k=1: all orders 720 * 2 starts
    best = float("inf")
    for start in b.exits:
        for order in itertools.permutations(rooms):
            t = resp_time(b, start, list(order), WALK_SPEED)
            best = min(best, t)
    out[1] = best
    # k=2: partitions via greedy order within subset (validated in PoC)
    from sweep import exact_basic_two
    clear_cache()
    out[2], _ = exact_basic_two(b)
    return out


# ---------------------------------------------------------------- exp-001

def exp_001():
    b = build_basic()
    clear_cache()
    params = dict(scenario="basic (Figure 1)", walk_speed=WALK_SPEED,
                  check_time=20.0, seed=SEED, method="exact k<=2, heuristic k>=3")
    exact = exact_k1_k2_basic(b)
    scaling = {str(k): exact[k] for k in exact}
    detail = {}
    for k in (3, 4):
        clear_cache()
        ms, routes, starts = optimize_k(b, k, sorted(b.rooms))
        scaling[str(k)] = ms
        detail[str(k)] = dict(routes=routes, starts=[list(s) for s in starts])
    ms2, routes2, starts2 = optimize_k(b, 2, sorted(b.rooms))
    detail["2_heuristic_check"] = dict(routes=routes2, makespan=ms2)
    metrics = dict(responder_scaling_s=scaling, detail=detail,
                   optimum_k2_s=scaling["2"],
                   baseline_k1_s=scaling["1"],
                   speedup_k2_vs_k1=scaling["1"] / scaling["2"])
    save_run("exp-001", params, metrics)
    return scaling


# ---------------------------------------------------------------- exp-002

def exp_002():
    results = {}
    for name, fn in (("B", build_scenario_b), ("C", build_scenario_c)):
        b = fn()
        clear_cache()
        params = dict(scenario=name, walk_speed=WALK_SPEED, seed=SEED,
                      stair_time_s=STAIR_TIME, method="insertion + swap LS")
        scaling, detail = {}, {}
        for k in range(1, 7):
            clear_cache()
            ms, routes, starts = optimize_k(b, k, sorted(b.rooms))
            scaling[str(k)] = ms
            detail[str(k)] = dict(routes=routes, starts=[list(s) for s in starts])
        # optimal k: first k where marginal gain < 10%
        opt_k, prev = 1, None
        for k in sorted(scaling, key=int):
            if prev is not None and scaling[prev] / scaling[k] < 1.10:
                break
            opt_k, prev = int(k), k
        metrics = dict(responder_scaling_s=scaling, detail=detail,
                       optimal_k=opt_k,
                       optimal_makespan_s=scaling[str(opt_k)],
                       rooms=len(b.rooms), exits=len(b.exits))
        save_run(f"exp-002-{name}", params, metrics)
        results[name] = metrics
    return results


# ---------------------------------------------------------------- exp-003

def sample_scenario_b(rng, k, smoke=True, comm_p=0.2, occupancy=True):
    """One Monte Carlo sample of scenario B with realistic constraints.
    Returns (makespan, rooms_checked) for k=optimal from exp-002."""
    b = build_scenario_b()
    walk = WALK_SPEED
    if smoke:
        s = rng.uniform(0.0, 1.0)
        walk = WALK_SPEED * max(0.3, 1.0 - 0.7 * s)  # P6
    if occupancy:
        for rid, r in b.rooms.items():
            p = 0.8 if r["priority"] == 3 else 0.2
            if rng.random() < p:
                r["check_time"] = r["check_time"] * 1.5  # P8
    if comm_p > 0:
        for rid, r in b.rooms.items():
            if rng.random() < comm_p:
                r["check_time"] = r["check_time"] + rng.uniform(10, 30)  # P7
    clear_cache()
    ms, routes, starts = optimize_k(b, k, sorted(b.rooms), walk)
    return ms


def sample_scenario_b_fixed(rng, k, smoke_level=None, comm_p=0.0):
    """MC sample with a FIXED smoke level (isolate one factor)."""
    b = build_scenario_b()
    walk = WALK_SPEED
    if smoke_level is not None:
        walk = WALK_SPEED * max(0.3, 1.0 - 0.7 * smoke_level)
    if comm_p > 0:
        for r in b.rooms.values():
            if rng.random() < comm_p:
                r["check_time"] = r["check_time"] + rng.uniform(10, 30)
    clear_cache()
    ms, routes, starts = optimize_k(b, k, sorted(b.rooms), walk)
    return ms


def exp_005(n=100):
    """One-factor constraint curves on scenario B at optimal k:
    smoke level 0..1 (comm/occupancy off) and comm failure prob 0..0.4."""
    kopt = json.loads(
        (RUNS / "exp-002-B" / "metrics.json").read_text())["optimal_k"]
    smoke_curve, comm_curve = {}, {}
    for level in (0.0, 0.25, 0.5, 0.75, 1.0):
        rng = random.Random(SEED)
        s = [sample_scenario_b_fixed(rng, kopt, smoke_level=level)
             for _ in range(n)]
        smoke_curve[str(level)] = round(sum(s) / n, 1)
    for p in (0.0, 0.1, 0.2, 0.3, 0.4):
        rng = random.Random(SEED)
        s = [sample_scenario_b_fixed(rng, kopt, comm_p=p) for _ in range(n)]
        comm_curve[str(p)] = round(sum(s) / n, 1)
    params = dict(scenario="B", k=kopt, n=n, seed=SEED,
                  note="one-factor isolation; occupancy off")
    metrics = dict(smoke_level_curve_s=smoke_curve,
                   comm_fail_curve_s=comm_curve)
    save_run("exp-005", params, metrics)
    return metrics


def exp_003(n=200):
    kopt = json.loads(
        (RUNS / "exp-002-B" / "metrics.json").read_text())["optimal_k"]
    rng = random.Random(SEED)
    det = sample_scenario_b(random.Random(0), kopt, smoke=False, comm_p=0.0,
                            occupancy=False)
    samples = [sample_scenario_b(rng, kopt) for _ in range(n)]
    mean = sum(samples) / n
    sd = math.sqrt(sum((x - mean) ** 2 for x in samples) / (n - 1))
    ci = 1.96 * sd / math.sqrt(n)
    p95 = sorted(samples)[int(0.95 * n) - 1]
    params = dict(scenario="B", samples=n, seed=SEED,
                  smoke="P6 speed factor", comm_p=0.2, occupancy="P8 x1.5",
                  k=kopt)
    metrics = dict(deterministic_no_constraints_s=round(det, 1),
                   mc_mean_s=round(mean, 1), mc_sd_s=round(sd, 1),
                   mc_ci95_s=round(ci, 1), mc_p95_s=round(p95, 1),
                   degradation_pct=round((mean / det - 1) * 100, 1),
                   n=n, seed=SEED)
    save_run("exp-003", params, metrics)
    (RUNS / "exp-003" / "raw_samples.json").write_text(
        json.dumps(samples))
    return metrics


# ---------------------------------------------------------------- exp-004

def exp_004():
    """Technology: sensor coverage c in {0, 0.5, 1.0} multiplies room check
    time by (1 - 0.6c). Re-optimize each scenario at its optimal k."""
    out = {}
    for name, fn in (("B", build_scenario_b), ("C", build_scenario_c)):
        kopt = json.loads(
            (RUNS / f"exp-002-{name}" / "metrics.json").read_text())["optimal_k"]
        base_t, tech_t = {}, {}
        for c in (0.0, 0.5, 1.0):
            b = fn()
            clear_cache()
            for r in b.rooms.values():
                r["check_time"] = r["check_time"] * (1 - 0.6 * c)
            ms, routes, starts = optimize_k(b, kopt, sorted(b.rooms))
            (base_t if c == 0.0 else tech_t)[str(c)] = ms
        metrics = dict(k=kopt, no_tech_s=round(base_t["0.0"], 1),
                       sensor50_s=round(tech_t["0.5"], 1),
                       sensor100_s=round(tech_t["1.0"], 1),
                       reduction100_pct=round(
                           (1 - tech_t["1.0"] / base_t["0.0"]) * 100, 1))
        save_run(f"exp-004-{name}",
                 dict(scenario=name, tech="check_time*(1-0.6c)", k=kopt,
                      seed=SEED), metrics)
        out[name] = metrics
    return out


if __name__ == "__main__":
    exp_001()
    exp_002()
    exp_003()
    exp_004()
    exp_005()
    print("[experiments] all runs complete")
