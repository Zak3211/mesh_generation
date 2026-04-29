import matplotlib
import matplotlib.pyplot as plt
import itertools
import random
import edge_flip
from fractions import Fraction
from utils import edges_cross

# import tikzplotlib

# matplotlib.use("pgf")
matplotlib.rcParams.update(
    {
        "pgf.texsystem": "pdflatex",
        "font.family": "serif",
        "text.usetex": True,
        "pgf.rcfonts": False,
    }
)


aerofoil = {
    "vertices": [
        (398, 237),
        (366, 236),
        (341, 222),
        (333, 198),
        (339, 176),
        (367, 153),
        (432, 127),
        (508, 116),
        (630, 125),
        (773, 164),
        (894, 210),
        (911, 220),
        (925, 226),
    ],
    "edges": [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 8),
        (8, 9),
        (9, 10),
        (10, 11),
        (11, 12),
        (12, 0),
    ],
}

surrounding = {
    "vertices": [
        (137, 199),
        (184, 120),
        (245, 76),
        (345, 41),
        (458, 31),
        (565, 27),
        (704, 38),
        (817, 52),
        (914, 83),
        (984, 124),
        (1007, 171),
        (952, 165),
        (870, 118),
        (789, 107),
        (721, 94),
        (639, 84),
        (554, 82),
        (478, 83),
        (429, 75),
        (361, 96),
        (295, 126),
        (252, 139),
        (208, 177),
        (187, 227),
        (182, 264),
        (212, 276),
        (276, 283),
        (342, 295),
        (405, 292),
        (477, 293),
        (547, 295),
        (628, 303),
        (704, 303),
        (793, 298),
        (880, 300),
        (965, 293),
        (1023, 281),
        (1052, 247),
        (1054, 237),
        (1042, 219),
        (1039, 202),
        (1053, 169),
        (1049, 135),
        (1024, 98),
        (992, 74),
        (949, 47),
        (891, 18),
        (796, 13),
        (688, -9),
        (447, -6),
        (343, 7),
        (265, 21),
        (196, 49),
        (124, 94),
        (74, 160),
        (67, 216),
        (101, 248),
        (130, 281),
        (153, 307),
        (346, 358),
        (446, 347),
        (612, 350),
        (924, 363),
        (1056, 336),
        (1109, 249),
        (1118, 155),
        (1100, 99),
        (1049, 44),
    ],
    "edges": [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 8),
        (8, 9),
        (9, 10),
        (10, 11),
        (11, 12),
        (12, 13),
        (13, 14),
        (14, 15),
        (15, 16),
        (16, 17),
        (17, 18),
        (18, 19),
        (19, 20),
        (20, 21),
        (21, 22),
        (22, 23),
        (23, 24),
        (24, 25),
        (25, 26),
        (26, 27),
        (27, 28),
        (28, 29),
        (29, 30),
        (30, 31),
        (31, 32),
        (32, 33),
        (33, 34),
        (34, 35),
        (35, 36),
        (36, 37),
        (37, 38),
        (38, 39),
        (39, 40),
        (40, 41),
        (41, 42),
        (42, 43),
        (43, 44),
        (44, 45),
        (45, 46),
        (46, 47),
        (47, 48),
        (48, 49),
        (49, 50),
        (50, 51),
        (51, 52),
        (52, 53),
        (53, 54),
        (54, 55),
        (55, 56),
        (56, 57),
        (57, 58),
        (58, 59),
        (59, 60),
        (60, 61),
        (61, 62),
        (62, 63),
        (63, 64),
        (64, 65),
        (65, 66),
        (66, 67),
    ],
}

# raw_vertices = [
#     (0.804, 0.473),
#     (0.624, 0.765),
#     (0.279, 0.784),
#     (0.117, 0.596),
#     (0.192, 0.242),
#     (0.447, 0.213),
#     (0.699, 0.229),
#     (0.374, 0.756),
#     (0.620, 0.555),
#     (0.224, 0.302),
#     (0.530, 0.617),
#     (0.689, 0.334),
#     # (0.242, 0.318),
#     # (0.326, 0.513),
#     # (0.414, 0.379),
#     # (0.537, 0.293),
#     # (0.318, 0.422),
#     # (0.430, 0.661),
#     # (0.254, 0.507),
#     # (0.524, 0.240),
#     # (0.534, 0.310),
#     # (0.326, 0.269),
#     # (0.587, 0.464),
#     # (0.201, 0.496),
#     # (0.295, 0.591),
#     # (0.331, 0.510),
#     # (0.493, 0.319),
#     # (0.528, 0.739),
#     # (0.178, 0.325),
#     # (0.384, 0.368),
#     # (0.686, 0.417),
#     # (0.310, 0.523),
#     # (0.214, 0.671),
#     # (0.648, 0.326),
#     # (0.603, 0.629),
#     # (0.647, 0.255),
#     # (0.363, 0.279),
#     # (0.710, 0.569),
#     # (0.344, 0.249),
#     # (0.331, 0.399),
#     # (0.618, 0.577),
#     # (0.727, 0.483),
#     # (0.199, 0.620),
#     # (0.640, 0.533),
#     # (0.647, 0.495),
#     # (0.476, 0.457),
#     # (0.139, 0.576),
#     # (0.333, 0.503),
#     # (0.740, 0.355),
#     # (0.399, 0.644),
#     (0.274, 0.257),
#     (0.316, 0.305),
#     (0.552, 0.711),
#     (0.669, 0.320),
#     (0.730, 0.521),
#     (0.335, 0.276),
#     (0.274, 0.457),
# ]

# n_vertices = 22

# random.seed(987)

# x = [random.uniform(-3.0, 3.0) for _ in range(n_vertices)]
# y = [random.uniform(-3.0, 3.0) for _ in range(n_vertices)]

# # x = [float(m) for m in random.choices(range(0, 101), k=n_vertices)]
# # y = [float(m) for m in random.choices(range(0, 101), k=n_vertices)]

# raw_vertices = itertools.zip_longest(x, y)

raw_vertices = aerofoil["vertices"] + surrounding["vertices"]

aerofoil_mid_x = sum((x for x, _ in aerofoil["vertices"])) / len(aerofoil["vertices"])
aerofoil_mid_y = sum((y for _, y in aerofoil["vertices"])) / len(aerofoil["vertices"])

# scale_factors = [0.05, 0.3, 0.1]

# for sf in scale_factors:
#     aerofoil_extra_x = [
#         int(x + sf * (aerofoil_mid_x - x)) for x, _ in aerofoil["vertices"]
#     ]

#     aerofoil_extra_y = [
#         int(y + sf * (aerofoil_mid_y - y)) for _, y in aerofoil["vertices"]
#     ]

#     raw_vertices += list(itertools.zip_longest(aerofoil_extra_x, aerofoil_extra_y))

raw_vertices = [(x, 400 - y) for x, y in raw_vertices]

constrained_edges = [(raw_vertices[i], raw_vertices[j]) for i, j in aerofoil["edges"]]

raw_vertices = list(set(raw_vertices))

n_raw = len(raw_vertices)


def are_collinear(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0]) == 0


vertices = []

for p in raw_vertices:
    is_collinear = False
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            if are_collinear(vertices[i], vertices[j], p):
                is_collinear = True
                break
        if is_collinear:
            break

    if not is_collinear:
        vertices.append(p)

x = [p[0] for p in vertices]
y = [p[1] for p in vertices]

n_after = len(vertices)

print(f"removed {n_raw - n_after} vertices")

possible_edges = itertools.combinations(vertices, 2)

edges_by_length = sorted(
    possible_edges,
    # Ascending order by squared length.
    key=lambda edge: (edge[0][0] - edge[1][0]) ** 2 + (edge[0][1] - edge[1][1]) ** 2,
)

actual_edges = []

for candidate in edges_by_length:
    if not any((edges_cross(existing, candidate) for existing in actual_edges)):
        actual_edges.append(candidate)

num_edges = len(actual_edges)

# plt.xticks([])
# plt.yticks([])

# # Plot with varying colours by length.
# cmap = plt.get_cmap("PuRd")

actual_edges: set = set(actual_edges)
edge_flip.flip_all(actual_edges)
actual_edges = edge_flip.constrained_triangulation(actual_edges, constrained_edges)

marked_edges = []

bad_vertices = set()

for i, (a, b) in enumerate(actual_edges):
    if edge_flip.is_edge_locally_delaunay(actual_edges, (a, b)):
        edge_color = "black"
    else:
        edge_color = "red"

        bad_vertices.add(a)
        bad_vertices.add(b)

    plt.plot([a[0], b[0]], [a[1], b[1]], color=edge_color)

bad_vertices = list(bad_vertices)
good_vertices = list(set((v for e in actual_edges for v in e if v not in bad_vertices)))

plt.scatter(
    [p[0] for p in bad_vertices], [p[1] for p in bad_vertices], c="red", zorder=10
)

plt.scatter(
    [p[0] for p in good_vertices], [p[1] for p in good_vertices], c="black", zorder=10
)

# # for i, _ in enumerate(actual_edges):
# k = 15
# e = actual_edges[k]

# opp = list(edge_flip.vertices_opposite(actual_edges, e))
# print(opp)
# plt.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], c="blue", zorder=10)

plt.axis("equal")
plt.tight_layout()
# fig = plt.gcf()
plt.show()
# fig.savefig("/tmp/greedy_unflipped.pgf", backend="pgf")
# tikzplotlib.save("/tmp/greedy_flipped.tex")
