from typing import Optional, Set
from queue import Queue, PriorityQueue
from ship import Ship
from shiputil import *
from util import PrioritizedShip
from log import Log
from queue import Queue
from container import Container


def load_unload(orig_ship: Ship, unloads: list = [], loads: list = [Container]):
    def coord_to_cntr(cntr: list, selecting: bool = True) -> Container:
        selected_cntr = orig_ship.get_cntr(cntr)
        selected_cntr.selected = selecting

        return selected_cntr

    nodes = Queue()
    nodes.put(orig_ship)
    dups = set()
    dups.add(orig_ship.generate_ship_key())
    max_queue = 1
    expanded_nodes = 0

    while not nodes.empty():
        node = nodes.get()
        expanded_nodes += 1
        # print(node, node.crane_loc)

        # if node.is_balanced():
        #     print(node)
        #     print(f"Max Queue Size: {max_queue}\nExpanded Nodes: {expanded_nodes}")
        #     return node

        load_unload_queuing(
            nodes,
            node,
            dups,
            [node.find_best_cntr(coord_to_cntr(cntr, True)) for cntr in unloads],
            loads,
        )
        # balance_queueing(nodes, node, dups, problem.row, problem.col)
        # if nodes.qsize() > max_queue:
        #     max_queue = nodes.qsize()

    print("Error: unsolvable ship")
    return None
    # ship.init_goal_state([ship.ship_state[cntr[0], cntr[1]].name for cntr in loads], [ship.ship_state[cntr[0], cntr[1]].name for cntr in unloads])


def load_unload_queuing(
    nodes: Queue,
    node: Ship,
    dups: Set[str],
    unloads: list = [Container],
    loads: list = [Container],
):
    children = []

    for i in range(col):
        children.append(node.move_crane(i))
        # print("new child", children[len(children) - 1])

    for child in children:
        # print("child", child == None, end=" ")
        # if child == None:
        #     print()
        # else:
        #     print(child.crane_loc, child.crane_mode, "\n", child)
        if child != None and child.generate_ship_key() not in dups:
            nodes.put(child)
            # print(child.crane_loc, child.crane_mode)
            dups.add(child.generate_ship_key())


def balance_queueing(nodes: Queue, node: Ship, dups: Set[str], row: int, col: int):
    children = []

    for i in range(col):
        children.append(node.move_crane(i))
        # print("new child", children[len(children) - 1])

    for child in children:
        # print("child", child == None, end=" ")
        # if child == None:
        #     print()
        # else:
        #     print(child.crane_loc, child.crane_mode, "\n", child)
        if child != None and child.generate_ship_key() not in dups:
            nodes.put(child)
            # print(child.crane_loc, child.crane_mode)
            dups.add(child.generate_ship_key())

    # print("Dups:", len(dups))


def priority_balance_queueing(
    nodes: PriorityQueue,
    node: Ship,
    dups: Set[str],
    row: int,
    col: int,
    heuristic: str = None,
):
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
            #     "Before: loc:",
            #     node.crane_loc,
            #     "mode:",
            #     node.crane_mode,
            #     "cost:",
            #     node.time_cost,
            #     "heuristic:",
            #     node.cntr_cross_bal_heuristic,
            #     "After: loc:",
            #     child.crane_loc,
            #     "mode:",
            #     child.crane_mode,
            #     "cost:",
            #     child.time_cost,
            #     "heuristic:",
            #     child.cntr_cross_bal_heuristic,
            #     "total:",
            #     total_cost,
            #     "\n",
            #     child.generate_ship_key(),
            # )
            # print(child)
            dups.add(child.generate_ship_key())

    # print("Dups:", len(dups))


def uniform_cost_balance(problem: Ship, heuristic: str = None) -> Optional[Ship]:
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
