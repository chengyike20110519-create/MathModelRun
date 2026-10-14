"""Building graph definitions for 2025 HiMCM Problem A.

Geometry assumptions are declared in data_cleaned/data_plan.json.
All coordinates in meters. Nodes: ('hall', seg_index) for hallway
segments, ('room', id) for rooms, ('exit', i) for exits, ('stair', i)
for stairwells. Edges carry travel time in seconds derived from
geometry and P1 walk speed.
"""

WALK_SPEED = 1.2          # P1 m/s
DOOR_TIME = 2.0           # P5 s


class Building:
    def __init__(self):
        self.nodes = {}      # id -> (x, y, floor)
        self.edges = {}      # id -> {neighbor_id: time_s}
        self.rooms = {}      # room_id -> dict(check_time, priority, occupied, floor)
        self.exits = []
        self.hall_segments = []  # ordered segment ids per floor

    def add_node(self, nid, x, y, floor=0):
        self.nodes[nid] = (x, y, floor)
        self.edges.setdefault(nid, {})

    def link(self, a, b, time_s):
        self.edges[a][b] = time_s
        self.edges[b][a] = time_s

    def dist(self, a, b):
        ax, ay, _ = self.nodes[a]
        bx, by, _ = self.nodes[b]
        return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5

    def link_dist(self, a, b, speed=WALK_SPEED):
        self.link(a, b, self.dist(a, b) / speed + DOOR_TIME * 0)


def build_basic(check_time=20.0, walk_speed=WALK_SPEED):
    """Figure 1: one-story office, central hallway, 3 rooms per side,
    2 exits at opposite ends of the hallway."""
    b = Building()
    seg_len = 10.0  # 3 segments of 10 m = 30 m hallway
    # hallway segments
    for i in range(3):
        b.add_node(("hall", i), x=seg_len * i + seg_len / 2, y=0.0)
        if i > 0:
            b.link_dist(("hall", i - 1), ("hall", i), walk_speed)
    # exits at both ends
    b.add_node(("exit", 0), x=-1.0, y=0.0)
    b.add_node(("exit", 1), x=seg_len * 3 + 1.0, y=0.0)
    b.link_dist(("exit", 0), ("hall", 0), walk_speed)
    b.link_dist(("exit", 1), ("hall", 2), walk_speed)
    b.exits = [("exit", 0), ("exit", 1)]
    # rooms: 3 per side, door in middle of each hallway segment
    room_w = 5.0
    for side, y in (("N", 3.5), ("S", -3.5)):
        for i in range(3):
            rid = f"{side}{i+1}"
            b.add_node(("room", rid), x=seg_len * i + seg_len / 2, y=y)
            b.link_dist(("room", rid), ("hall", i), walk_speed)
            b.rooms[rid] = dict(check_time=check_time, priority=1,
                                occupied=False, floor=0)
    return b


STAIR_TIME = 25.0  # s to climb one floor (data_plan scenario_B/C)


def _floor_hallway(b, floor, n_seg, seg_len=10.0, y_base=0.0):
    """Create n_seg hallway segments on a floor, return segment ids."""
    ids = []
    for i in range(n_seg):
        nid = ("hall", floor, i)
        b.add_node(nid, x=seg_len * i + seg_len / 2, y=y_base + floor * 0.01,
                   floor=floor)
        if i > 0:
            b.link_dist(ids[-1], nid, WALK_SPEED)
        ids.append(nid)
    return ids


def _add_rooms(b, floor, hall_ids, rooms_per_seg, y, prefix, check_time,
               priority, occupied):
    """rooms_per_seg: dict seg_index -> count. Rooms spread evenly in seg."""
    rid_n = 0
    for seg_i, hall in enumerate(hall_ids):
        n = rooms_per_seg.get(seg_i, 0)
        for j in range(n):
            rid_n += 1
            rid = f"{prefix}{rid_n}"
            x = (hall[2] + 1) * 10.0 - 5.0 + (j - (n - 1) / 2) * 2.0
            b.add_node(("room", rid), x=x, y=y, floor=floor)
            b.link_dist(("room", rid), hall, WALK_SPEED)
            b.rooms[rid] = dict(check_time=check_time, priority=priority,
                                occupied=occupied, floor=floor)


def build_scenario_b():
    """2 floors: daycare (floor 0, 4 occupied high-priority rooms + lobby)
    + office (floor 1, 6 rooms like basic). 2 stairwells, 2 exits."""
    b = Building()
    # floor 0: daycare, 2 hallway segments, 2 rooms per segment
    h0 = _floor_hallway(b, 0, 2)
    _add_rooms(b, 0, h0, {0: 2, 1: 2}, y=3.5, prefix="D", check_time=25.0,
               priority=3, occupied=True)
    b.add_node(("room", "L1"), x=5.0, y=-3.5, floor=0)
    b.link_dist(("room", "L1"), h0[0], WALK_SPEED)
    b.rooms["L1"] = dict(check_time=30.0, priority=2, occupied=True, floor=0)
    # floor 1: office, 3 segments, 2 rooms per segment
    h1 = _floor_hallway(b, 1, 3)
    _add_rooms(b, 1, h1, {0: 2, 1: 2, 2: 2}, y=3.5, prefix="O", check_time=20.0,
               priority=1, occupied=False)
    # exits on floor 0
    b.add_node(("exit", 0), x=-1.0, y=0.0, floor=0)
    b.add_node(("exit", 1), x=21.0, y=0.0, floor=0)
    b.link_dist(("exit", 0), h0[0], WALK_SPEED)
    b.link_dist(("exit", 1), h0[1], WALK_SPEED)
    b.exits = [("exit", 0), ("exit", 1)]
    # stairwells: floor0 hall end <-> floor1 hall end
    for i, (a, c) in enumerate([(h0[0], h1[0]), (h0[1], h1[2])]):
        sn = ("stair", i)
        b.add_node(sn, x=b.nodes[a][0], y=-1.5, floor=None)
        b.link(a, sn, STAIR_TIME / 2)
        b.link(c, sn, STAIR_TIME / 2)
    return b


def build_scenario_c():
    """3 floors mixed-use: warehouse (2 large areas), labs (5, chemical
    hazard priority), L-shaped office (5 rooms + conference hall).
    2 stairwells, 3 exits."""
    b = Building()
    # floor 0: warehouse, 2 large areas, 2 segments
    h0 = _floor_hallway(b, 0, 2)
    for i, hall in enumerate(h0):
        rid = f"W{i+1}"
        b.add_node(("room", rid), x=hall[2] * 10.0 + 5.0, y=4.5, floor=0)
        b.link_dist(("room", rid), hall, WALK_SPEED)
        b.rooms[rid] = dict(check_time=45.0, priority=2, occupied=False, floor=0)
    b.add_node(("exit", 2), x=10.0, y=-4.5, floor=0)  # loading bay
    b.link_dist(("exit", 2), h0[0], WALK_SPEED)
    # floor 1: labs, 3 segments, 5 rooms (2+2+1)
    h1 = _floor_hallway(b, 1, 3)
    _add_rooms(b, 1, h1, {0: 2, 1: 2, 2: 1}, y=3.5, prefix="LB", check_time=35.0,
               priority=3, occupied=False)
    # floor 2: L-shaped office: straight part 3 segments 3 rooms, wing 2 rooms
    h2 = _floor_hallway(b, 2, 3)
    _add_rooms(b, 2, h2, {0: 1, 1: 1, 2: 1}, y=3.5, prefix="F", check_time=20.0,
               priority=1, occupied=False)
    wing = ("hall", 2, 3)
    b.add_node(wing, x=27.5, y=-6.0, floor=2)
    b.link_dist(h2[2], wing, WALK_SPEED)
    _add_rooms(b, 2, [wing], {0: 2}, y=-9.0, prefix="G", check_time=20.0,
               priority=1, occupied=False)
    b.add_node(("room", "CONF"), x=27.5, y=-3.0, floor=2)
    b.link_dist(("room", "CONF"), wing, WALK_SPEED)
    b.rooms["CONF"] = dict(check_time=30.0, priority=2, occupied=False, floor=2)
    # exits floor 0
    b.add_node(("exit", 0), x=-1.0, y=0.0, floor=0)
    b.add_node(("exit", 1), x=31.0, y=0.0, floor=0)
    b.link_dist(("exit", 0), h0[0], WALK_SPEED)
    b.link_dist(("exit", 1), h0[1], WALK_SPEED)
    b.exits = [("exit", 0), ("exit", 1), ("exit", 2)]
    # stairwells floor0<->1<->2 at both ends
    for i, xpos in enumerate((0.0, 20.0)):
        s01 = ("stair", i, 0)
        s12 = ("stair", i, 1)
        b.add_node(s01, x=xpos, y=-1.5, floor=None)
        b.add_node(s12, x=xpos, y=-1.5, floor=None)
        f0h = ("hall", 0, 0) if xpos == 0.0 else ("hall", 0, 1)
        f1h = ("hall", 1, 0) if xpos == 0.0 else ("hall", 1, 2)
        f2h = ("hall", 2, 0) if xpos == 0.0 else ("hall", 2, 2)
        b.link(f0h, s01, STAIR_TIME / 2)
        b.link(f1h, s01, STAIR_TIME / 2)
        b.link(f1h, s12, STAIR_TIME / 2)
        b.link(f2h, s12, STAIR_TIME / 2)
    return b
