import matplotlib
import matplotlib.pyplot as plt
import itertools
import random

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
    (aa, ab) = ea
    (ba, bb) = eb

    # If the edges share vertices, they are adjacent, but not "crossing".
    # (We ignore the case where the edges are the same, since it won't happen in this use case.)
    if aa == ba or aa == bb or ab == ba or ab == bb:
        return False

    def ccw(p, q, r):
        return (r[1] - p[1]) * (q[0] - p[0]) > (q[1] - p[1]) * (r[0] - p[0])

    return ccw(aa, ba, bb) != ccw(ab, ba, bb) and ccw(aa, ab, ba) != ccw(aa, ab, bb)


n_vertices = 60

random.seed(123456)

x = random.sample(range(0, 101), n_vertices)
y = random.sample(range(0, 101), n_vertices)

vertices = itertools.zip_longest(x, y)
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

plt.xticks([])
plt.yticks([])

# Plot with varying colours by length.
cmap = plt.get_cmap("PuRd")

for i, (a, b) in enumerate(actual_edges):
    edge_color = cmap(i / num_edges)
    plt.plot([a[0], b[0]], [a[1], b[1]], color=edge_color, marker="o")

fig = plt.gcf()
plt.show()
fig.savefig("/tmp/figure.pgf", backend="pgf")
