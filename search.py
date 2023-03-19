import csv
from typing import Optional, Set
from ship import Ship
from shiputil import *
from log import Log
from queue import Queue


def balance_queueing(nodes: Queue, node: Ship, dups: Set[str], row: int, col: int):
    children = []

    for i in col:
        if i != node.crane_loc:  # check crane_loc is not in same col
            children.append(node.move_crane(i))

    for child in children:
        if child != None and child.ship_str() not in dups:
            nodes.push(child)
            dups.add(child.ship_str())


def uniform_cost_balance(problem: Ship) -> Optional[Ship]:
    nodes = Queue()
    nodes.put(problem)
    dups = set()
    dups.add(problem.ship_str())  # use ship_str as hash key
    max_queue = 1
    expanded_nodes = 0

    while not nodes.empty():
        node = nodes.get()
        expanded_nodes += 1

        if node.is_balanced():
            print(node)
            print(f"Max Queue Size: {max_queue}\nExpanded Nodes: {expanded_nodes}")
            return node

        balance_queueing(nodes, node, dups, problem.row, problem.col)
        if nodes.qsize() > max_queue:
            max_queue = nodes.qsize()

    print("Error: unsolvable ship")
    return None
