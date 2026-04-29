import matplotlib
import matplotlib.pyplot as plt
import itertools
import random
import edge_flip
from fractions import Fraction
import tikzplotlib

# matplotlib.use("pgf")
matplotlib.rcParams.update(
    {
        "pgf.texsystem": "pdflatex",
        "font.family": "serif",
        "text.usetex": True,
        "pgf.rcfonts": False,
    }
)


def edges_cross(ea, eb):
    aa, ab = ea
    ba, bb = eb

    # If the edges share vertices, they are adjacent, but not "crossing".
    if aa == ba or aa == bb or ab == ba or ab == bb:
        return False

    def ccw(p, q, r):
        return (r[1] - p[1]) * (q[0] - p[0]) > (q[1] - p[1]) * (r[0] - p[0])

    return ccw(aa, ba, bb) != ccw(ab, ba, bb) and ccw(aa, ab, ba) != ccw(aa, ab, bb)


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

n_vertices = 22

random.seed(987)

x = [random.uniform(-3.0, 3.0) for _ in range(n_vertices)]
y = [random.uniform(-3.0, 3.0) for _ in range(n_vertices)]

# x = [float(m) for m in random.choices(range(0, 101), k=n_vertices)]
# y = [float(m) for m in random.choices(range(0, 101), k=n_vertices)]

raw_vertices = itertools.zip_longest(x, y)


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


# fig = plt.gcf()
# plt.show()
# fig.savefig("/tmp/greedy_unflipped.pgf", backend="pgf")
tikzplotlib.save("/tmp/greedy_flipped.tex")
