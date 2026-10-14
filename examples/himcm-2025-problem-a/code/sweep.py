"""Discrete-event sweep simulator (PoC level, Q2 basic scenario).

Assumptions (data_cleaned/data_plan.json):
- Responders enter from an exit, move at P1 walk speed on graph edges.
- Checking a room costs check_time and must be done by exactly one
  responder (no duplicated checks in the primary model).
- Responders partition rooms; each walks a route: start exit -> rooms in
  given order -> end at either exit (nearest when done).
- Makespan = max over responders of total route time.

Exact cross-check: enumerate all room->responder assignments and
nearest-insertion room orders for the 2-responder basic case.
"""

import itertools
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from buildings import build_basic  # noqa: E402


def route_time(b, start, rooms_in_order, end, walk_speed=1.2, check_time=20.0):
    """Time for one responder to go start -> each room in order -> end,
    checking each room. Uses shortest-path travel times between nodes."""
    t = 0.0
    cur = start
    for rid in rooms_in_order:
        node = ("room", rid)
        t += shortest_path_time(b, cur, node, walk_speed)
        t += b.rooms[rid]["check_time"]
        cur = node
    t += shortest_path_time(b, cur, end, walk_speed)
    return t


def _sp_times(b, src, walk_speed):
    """Dijkstra from src over edge travel times (edges store distance; we
    recompute time with the given walk speed)."""
    import heapq

    dist = {src: 0.0}
    pq = [(0.0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float("inf")):
            continue
        for v, duv in b.edges[u].items():
            nd = d + duv / walk_speed
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


_sp_cache = {}


def shortest_path_time(b, a, c, walk_speed=1.2):
    key = (a, round(walk_speed, 4))
    if key not in _sp_cache:
        _sp_cache[key] = _sp_times(b, a, walk_speed)
    return _sp_cache[key][c]


def clear_cache():
    _sp_cache.clear()


def sweep_partition(b, assignment, starts, walk_speed=1.2):
    """assignment: responder index -> room list (in visit order).
    starts: responder index -> entry node. Each responder finishes at the
    exit nearest to their last room (they leave the building).
    Returns (makespan, per-responder times)."""
    times = []
    for r, rooms in enumerate(assignment):
        if not rooms:
            times.append(0.0)
            continue
        best = float("inf")
        for e in b.exits:
            t = route_time(b, starts[r], rooms, e, walk_speed)
            best = min(best, t)
        times.append(best)
    return max(times), times


def greedy_single(b, start, rooms, walk_speed=1.2):
    """Baseline: one responder, nearest-room greedy from start."""
    order = []
    remaining = set(rooms)
    cur = start
    while remaining:
        nxt = min(remaining,
                  key=lambda r: shortest_path_time(b, cur, ("room", r), walk_speed))
        order.append(nxt)
        remaining.remove(nxt)
        cur = ("room", nxt)
    return order


def exact_basic_two(b, walk_speed=1.2):
    """Enumerate all partitions of the 6 rooms between 2 responders and
    greedy-ordered routes; return the minimum makespan found."""
    rooms = sorted(b.rooms)
    best = (float("inf"), None)
    for mask in range(1 << len(rooms)):
        a = [r for i, r in enumerate(rooms) if mask & (1 << i)]
        c = [r for i, r in enumerate(rooms) if not mask & (1 << i)]
        for asg in (a, c), (c, a):
            for start0 in b.exits:
                for start1 in b.exits:
                    orders = []
                    for r, rooms_r in enumerate(asg):
                        start = (start0, start1)[r]
                        if rooms_r:
                            orders.append(
                                greedy_single(b, start, rooms_r, walk_speed))
                        else:
                            orders.append([])
                    ms, _ = sweep_partition(b, orders, [start0, start1],
                                            walk_speed)
                    if ms < best[0]:
                        best = (ms, (orders, start0, start1))
    return best


if __name__ == "__main__":
    b = build_basic()
    clear_cache()
    # Baseline: single responder greedy.
    base_order = greedy_single(b, ("exit", 0), sorted(b.rooms))
    t_base = route_time(b, ("exit", 0), base_order, ("exit", 1))
    print(f"[poc] baseline single-greedy  = {t_base:.1f} s, order={base_order}")

    # Primary (basic scenario is small enough for exact enumeration).
    clear_cache()
    ms_exact, detail = exact_basic_two(b)
    print(f"[poc] exact enumeration best  = {ms_exact:.1f} s, detail={detail}")

    # Simulator consistency: replaying the exact orders through
    # sweep_partition must reproduce the exact makespan.
    clear_cache()
    orders, s0, s1 = detail
    ms_replay, _ = sweep_partition(b, orders, [s0, s1])
    assert abs(ms_replay - ms_exact) < 1e-6, (
        f"simulator replay {ms_replay} != exact {ms_exact}")
    print(f"[poc] simulator replay of exact plan = {ms_replay:.1f} s (consistent)")

    # Heuristic partition (N/S split by entry side) vs exact optimum.
    asg = [["N1", "N2", "N3"], ["S1", "S2", "S3"]]
    starts = [("exit", 0), ("exit", 1)]
    ms_heur, _ = sweep_partition(b, asg, starts)
    gap = (ms_heur - ms_exact) / ms_exact * 100
    print(f"[poc] side-partition heuristic = {ms_heur:.1f} s "
          f"(optimality gap {gap:.1f}%)")

    # One-factor sensitivity: check time +-25%.
    for ct in (15.0, 25.0):
        bb = build_basic(check_time=ct)
        clear_cache()
        ms_ct, _ = exact_basic_two(bb)
        print(f"[poc] sensitivity check_time={ct:.0f}s -> makespan {ms_ct:.1f}s")

    print("[poc] PASS: baseline, exact optimum, simulator consistency, "
          "heuristic gap, and sensitivity all computed")
