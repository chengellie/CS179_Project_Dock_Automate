from typing import Optional, Set
from queue import Queue, PriorityQueue
from ship import Ship
from util import *
from log import Log
from queue import Queue
from container import Container


# def load_unload(orig_ship: Ship, unloads: list[Container], loads: list[Container]):


#     return [orig_ship.find_best_cntr(coord_to_cntr(cntr, True)) for cntr in unloads]


def balance_queueing(nodes: Queue, node: Ship, dups: Set[str], row: int, col: int):
    children = []

    for i in range(col):
        children.append(node.move_crane(i))

    for child in children:
        if child != None and child.generate_ship_key() not in dups:
            nodes.put(child)
            dups.add(child.generate_ship_key())


def breadth_first_balance(problem: Ship) -> Optional[Ship]:
    nodes = Queue()
    nodes.put(problem)
    dups = set()
    dups.add(problem.generate_ship_key())
    max_queue = 1
    expanded_nodes = 0

    while not nodes.empty():
        node = nodes.get()
        expanded_nodes += 1
        # print(node, node.crane_loc)

        if node.is_balanced():
            print(node)
            print(f"Max Queue Size: {max_queue}\nExpanded Nodes: {expanded_nodes}")
            return node

        balance_queueing(nodes, node, dups, problem.row, problem.col)
        if nodes.qsize() > max_queue:
            max_queue = nodes.qsize()

    print("Error: unsolvable ship")
    return None


def priority_balance_queueing(
    nodes: PriorityQueue,
    node: Ship,
    dups: Set[str],
    row: int,
    col: int,
    heuristic: str = None,
) -> None:
    """Inputs priority queue, current ship, duplicates, ship size, heuristic type.
    Expand current node and add all valid children to priority queue. Returns None.
    """
    children = []

    for i in range(col):
        children.append(node.move_crane(i, heuristic))

    for child in children:
        if child != None and child.generate_ship_key() not in dups:
            total_cost = child.time_cost
            if heuristic == "cntr-cross":
                total_cost += child.cntr_cross_bal_heuristic
            nodes.put(PrioritizedShip(total_cost, child))
            # print(
            #     "Before: loc: ",
            #     node.crane_loc,
            #     ", mode: ",
            #     node.crane_mode,
            #     ", cost: ",
            #     node.time_cost,
            #     ", heuristic: ",
            #     node.cntr_cross_bal_heuristic,
            #     sep="",
            # )
            # print(
            #     "After: loc: ",
            #     child.crane_loc,
            #     ", mode: ",
            #     child.crane_mode,
            #     ", cost: ",
            #     child.time_cost,
            #     ", heuristic: ",
            #     child.cntr_cross_bal_heuristic,
            #     sep="",
            # )
            # print(
            #     "total:",
            #     total_cost,
            #     "\nkey:",
            #     child.generate_ship_key(),
            # )
            # print(child)
            dups.add(child.generate_ship_key())

    # print("Dups:", len(dups))


def uniform_cost_balance(problem: Ship, heuristic: str = None) -> Optional[Ship]:
    all_weights = []
    for i in range(0, problem.col):
        for j in range(problem.top_columns[i] + 1, problem.row):
            all_weights.append(problem.ship_state[j][i].weight)

    if len(all_weights) == 0:
        print("Already Balanced")
        return problem
    elif len(all_weights) == 1:  # TODO: SIFT, just move this single container
        print("Error: unsolvable ship")
        return None
    all_weights.sort(reverse=True)
    if all_weights[0] * 0.9 > sum(all_weights[1:]):  # TODO SIFT, find optimal moves
        print("Error: unsolvable ship")
        return None

    nodes = PriorityQueue()
    problem.set_cntr_cross_bal_heuristic()
    total_cost = problem.time_cost
    if heuristic == "cntr-cross":
        total_cost += problem.cntr_cross_bal_heuristic
    nodes.put(PrioritizedShip(total_cost, problem))
    dups = set()
    dups.add(problem.generate_ship_key())
    max_queue = 1
    expanded_nodes = 0

    while not nodes.empty():
        node = nodes.get().item
        expanded_nodes += 1
        # print(node, node.crane_loc)

        if node.is_balanced():
            print(node)
            print(f"Max Queue Size: {max_queue}\nExpanded Nodes: {expanded_nodes}")
            return node

        priority_balance_queueing(
            nodes, node, dups, problem.row, problem.col, heuristic
        )
        if nodes.qsize() > max_queue:
            max_queue = nodes.qsize()

    print("Error: unsolvable ship")
    return None


def priority_lu_queueing(
    nodes: PriorityQueue,
    node: Ship,
    dups: Set[str],
    row: int,
    col: int,
    heuristic: str = None,
):
    children = []

    # col 12 used for when crane is in loading area
    for i in range(col + 1):
        children.append(node.move_crane(i, heuristic))

    for child in children:
        if child != None and child.generate_ship_key() not in dups:
            total_cost = child.time_cost
            if heuristic == "cntr-lu":
                total_cost += child.cntr_lu_heuristic
            nodes.put(PrioritizedShip(total_cost, child))
            # print(
            #     "Before: loc: ",
            #     node.crane_loc,
            #     ", mode: ",
            #     node.crane_mode,
            #     ", cost: ",
            #     node.time_cost,
            #     ", heuristic: ",
            #     node.cntr_lu_heuristic,
            #     sep="",
            # )
            # print(
            #     "After: loc: ",
            #     child.crane_loc,
            #     ", mode: ",
            #     child.crane_mode,
            #     ", cost: ",
            #     child.time_cost,
            #     ", heuristic: ",
            #     child.cntr_lu_heuristic,
            #     sep="",
            # )
            # print(
            #     "total:",
            #     total_cost,
            #     "\nkey:",
            #     child.generate_ship_key(),
            # )
            # print(child)
            dups.add(child.generate_ship_key())


def uniform_cost_lu(problem: Ship, heuristic: str = None) -> Optional[Ship]:
    nodes = PriorityQueue()
    problem.set_cntr_lu_heuristic()
    total_cost = problem.time_cost
    if heuristic == "cntr-lu":
        total_cost += problem.cntr_lu_heuristic
    nodes.put(PrioritizedShip(total_cost, problem))
    dups = set()
    dups.add(problem.generate_ship_key())
    max_queue = 1
    expanded_nodes = 0

    while not nodes.empty():
        node = nodes.get().item
        expanded_nodes += 1

        if node.is_goal_state():
            print(node)
            print(f"Max Queue Size: {max_queue}\nExpanded Nodes: {expanded_nodes}")
            return node

        priority_lu_queueing(nodes, node, dups, problem.row, problem.col, heuristic)
        if nodes.qsize() > max_queue:
            max_queue = nodes.qsize()

    print("Error: unsolvable ship")
    return None
