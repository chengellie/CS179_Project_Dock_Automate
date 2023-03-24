import csv
import copy
from typing import Optional, Set
from time import time  # https://docs.python.org/3/library/time.html

from ship import Ship
from search import *
from util import *
from log import Log


def balance(ship: Ship):
    ship.print_weights()

    # Test balance search
    start_time = time()
    sol = uniform_cost_balance(ship, "cntr-cross")
    print(f"Timer: {round(time() - start_time, 5)} seconds")

    if sol != None:
        print(sol.moves)
        print(sol.time_cost, sol.cntr_cross_bal_heuristic)


def load_unload_ship(ship: Ship):
    # Test loads unloads search
    # print(ship.loads)
    # print(ship.ship_state[7][1].selected)
    start_time = time()
    sol = uniform_cost_lu(ship)
    print(f"Timer: {round(time() - start_time, 5)} seconds")

    if sol != None:
        print(sol.moves)
        print(sol.time_cost, sol.cntr_cross_bal_heuristic)


if __name__ == "__main__":
    ship = create_ship(
        "ShipCase/ShipCase4.txt"
    )
    print(ship)

    print(ship.goal_state)
    # print(ship.time_between_col(0, 1))
    # print(ship.time_between_col(8, 3))
    # print(ship.get_moves([7, 8], [6, 3]))
    balance(ship)
    # load_unload_ship(ship)

    # Keep these commented unless testing logs
    # log = Log("testlog")
    # log.writelog("Testing Log")
    # log.writecomment("Good Day Sir")
    # log.readlog(printlog=True)
