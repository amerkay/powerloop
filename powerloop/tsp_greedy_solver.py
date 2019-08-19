"""
Greedy algorithm for TSP adapted from Josh Kelle's work at:
https://github.com/rellermeyer/99tsp/blob/master/python/greedy/greedy.py
"""

from math import sqrt


def dist2(x1, y1, x2, y2):
    """
    Computes Euclidean distance squared
    """
    return (x2 - x1)**2 + (y2 - y1)**2


def getNearestNode(remaining_nodes, current_node):
    """
    Args:
        remaining_nodes: list of (nodeid, x, y) triples
        current_node: the "current" node; (nodeid, x, y)

    Returns:
        1. nearest node: the (nodeid, x, y) triple closest to the current node
        2. the distance between this nearest node and the current node
    """
    _, cur_x, cur_y = current_node
    # dict that maps {dist2(a, b) -> b} where a is the "current" node.
    dist_to_node = {dist2(cur_x, cur_y, x, y): (nodeid, x, y) for nodeid, x, y in remaining_nodes}
    return dist_to_node[min(dist_to_node)], sqrt(min(dist_to_node))


def solveGreedyTSP(data):
    """
    Args:
        data: a list of triples of ints.
                [
                    (nodeid, x, y), # node [0] is the starting point used
                    (nodeid, x, y),
                    ...
                    (nodeid, x, y)
                ]

    Returns:
        best_path: list of (nodeid, x, y) triples in the order in which nodes
            should be visited.
        min_dist: The total distance of best_path
    """

    best_path = None
    min_dist = None

    # removed for-loop, as we have one starting point
    # for start_node in data:
    total_distance = 0
    start_node = data[0]
    visited_nodes = [start_node]
    remaining_nodes = [node for node in data if node is not start_node]

    while len(remaining_nodes) > 0:
        nearest_node, distance = getNearestNode(remaining_nodes, visited_nodes[-1])
        visited_nodes.append(nearest_node)
        remaining_nodes.remove(nearest_node)
        total_distance += distance

    # account for distance from last node to first node
    _, firstx, firsty = visited_nodes[0]
    _, lastx, lasty = visited_nodes[-1]
    total_distance += sqrt(dist2(firstx, firsty, lastx, lasty))

    # removed if statement with for-loop
    # if min_dist is None or total_distance < min_dist:
    best_path = visited_nodes
    min_dist = total_distance
    # print("starting at node {i} gives a distance of {d}".format(i=start_node[0], d=total_distance))

    return best_path, min_dist
