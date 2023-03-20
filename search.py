import csv
from typing import Optional, Set
from ship import Ship
from shiputil import *
from log import Log
from queue import Queue


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


def uniform_cost_balance(problem: Ship) -> Optional[Ship]:
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
