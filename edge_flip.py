import collections
import itertools
import math
from typing import Generator
from utils import edges_cross

type Point = tuple[float, float]
type Vertex = Point
type Edge = tuple[Vertex, Vertex]
type Triangulation = set[Edge]
type Face = tuple[Vertex, Vertex, Vertex]


def dist_sq(a: Point, b: Point) -> float:
    (ax, ay), (bx, by) = a, b
    return (ax - bx) ** 2 + (ay - by) ** 2


def dist(a: Point, b: Point) -> float:
    return math.sqrt(dist_sq(a, b))


def start(e: Edge) -> Vertex:
    return e[0]


def end(e: Edge) -> Vertex:
    return e[1]


def edge_length(e: Edge) -> float:
    return dist(*e)


def vertex_neighbours(t: Triangulation, v: Vertex) -> Generator[Vertex]:
    for e in t:
        a, b = e

        if a == v:
            yield b

        if b == v:
            yield a


def vertices_opposite(t: Triangulation, e: Edge) -> list[Vertex]:
    start_neighbours: set[Vertex] = set(vertex_neighbours(t, start(e)))
    end_neighbours: set[Vertex] = set(vertex_neighbours(t, end(e)))

    candidates = list(start_neighbours.intersection(end_neighbours))

    if len(candidates) == 1:
        return candidates

    def det(p: Vertex) -> float:
        (ax, ay), (bx, by) = e
        cx, cy = p
        return (ax - bx) * (ay - cy) - (ay - by) * (ax - cx)

    candidates_left = [cx for cx in candidates if det(cx) < 0]
    candidates_right = [cx for cx in candidates if det(cx) > 0]

    (ax, ay), (bx, by) = e
    midpoint = ((ax + bx) / 2, (ay + by) / 2)

    if len(candidates_left) != 0:
        candidates_left = [min(candidates_left, key=lambda p: dist_sq(p, midpoint))]

    if len(candidates_right) != 0:
        candidates_right = [min(candidates_right, key=lambda p: dist_sq(p, midpoint))]

    return candidates_left + candidates_right


def faces_with(t: Triangulation, e: Edge) -> Generator[Face]:
    opposite = vertices_opposite(t, e)

    for opp in opposite:
        yield (start(e), end(e), opp)


def face_edges(f: Face) -> tuple[Edge, Edge, Edge]:
    return (
        (f[0], f[1]),
        (f[0], f[2]),
        (f[1], f[2]),
    )


def circumcentre(f: Face) -> Point:
    (x1, y1), (x2, y2), (x3, y3) = f

    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

    cx = (
        (x1 * x1 + y1 * y1) * (y2 - y3)
        + (x2 * x2 + y2 * y2) * (y3 - y1)
        + (x3 * x3 + y3 * y3) * (y1 - y2)
    ) / d

    cy = (
        (x1 * x1 + y1 * y1) * (x3 - x2)
        + (x2 * x2 + y2 * y2) * (x1 - x3)
        + (x3 * x3 + y3 * y3) * (x2 - x1)
    ) / d

    return (cx, cy)


def normalised_edge(e: Edge) -> Edge:
    return tuple(sorted(e))  # type: ignore


def local_triangulation(t: Triangulation, e: Edge) -> Triangulation:
    faces = faces_with(t, e)

    local_t = set()

    for face in faces:
        for edge in face_edges(face):
            # Normalise the edge before adding it to the set so that we don't get duplicates.
            local_t.add(normalised_edge(edge))

    return local_t


def is_face_delaunay(t: Triangulation, f: Face) -> bool:
    cc = circumcentre(f)

    # Now we need the circumradius, so we can check for vertices in the circumcircle.
    [a, b, c] = [edge_length(e) for e in face_edges(f)]

    # https://en.wikipedia.org/wiki/Heron%27s_formula
    s = (a + b + c) / 2
    area_sq = s * (s - a) * (s - b) * (s - c)

    # Circumradius (squared)
    radius_sq = (a * a * b * b * c * c) / (16 * area_sq)

    # We need to check all the vertices except those those of the face.
    to_check = set((v for e in t for v in e if v not in f))

    return not any((dist_sq(cc, v) < radius_sq for v in to_check))


def is_edge_locally_delaunay(t: Triangulation, e: Edge) -> bool:
    if len(vertices_opposite(t, e)) == 1:
        return True

    local_t = local_triangulation(t, e)

    return all(is_face_delaunay(local_t, f) for f in faces_with(local_t, e))


def flipped_edge(t: Triangulation, e: Edge) -> Edge:
    opp = tuple(vertices_opposite(t, e))
    assert len(opp) == 2, f"found {len(opp)} opposite"

    opp = normalised_edge(opp)

    return opp


def flip_edge(t: Triangulation, e: Edge) -> Edge:
    opp = flipped_edge(t, e)

    t.remove(e)
    t.add(opp)

    return opp


def flip_all(t: Triangulation):
    while True:
        for e in t:
            if not is_edge_locally_delaunay(t, e):
                flip_edge(t, e)
                break
        else:
            # No flips made
            break


def normalised_triangulation(t: Triangulation) -> Triangulation:
    return set((normalised_edge(e) for e in t))


def in_quad(a: Point, b: Point, c: Point, d: Point, p: Point):
    vertx = [a[0], b[0], c[0], d[0]]
    verty = [a[1], b[1], c[1], d[1]]

    testx, testy = p

    m = False
    j = len(vertx) - 1

    for i in range(len(vertx)):
        if ((verty[i] > testy) != (verty[j] > testy)) and (
            testx
            < (vertx[j] - vertx[i]) * (testy - verty[i]) / (verty[j] - verty[i])
            + vertx[i]
        ):
            m = not m

        j = i

    return m


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception("lines do not intersect")

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def is_edge_flippable(t: Triangulation, ab: Edge) -> bool:
    if len(vertices_opposite(t, ab)) == 1:
        return False

    print(f"check {ab}")

    a, b = ab
    cd = flipped_edge(t, ab)
    c, d = cd

    intersection = line_intersection(ab, cd)

    iq = in_quad(a, c, b, d, intersection)

    # assert iq

    return iq


def constrained_triangulation(
    t_: Triangulation, constrained_edges_: list[Edge]
) -> Triangulation:
    t: Triangulation = normalised_triangulation(t_)
    constrained_edges: list[Edge] = [normalised_edge(e) for e in constrained_edges_]

    for s in constrained_edges:
        if s in t:
            continue

        q = collections.deque((e for e in t if edges_cross(e, s)))

        while len(q) != 0:
            ab: Edge = q.popleft()

            if is_edge_flippable(t, ab):
                cd = flip_edge(t, ab)

                if edges_cross(cd, s):
                    q.append(cd)
            else:
                q.append(ab)

        while True:
            for e in t:
                if e not in constrained_edges and not is_edge_locally_delaunay(t, e):
                    flip_edge(t, e)
                    break
            else:
                # No flips made
                break

    return t
