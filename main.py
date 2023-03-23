import csv
import copy
from typing import Optional, Set
from time import time  # https://docs.python.org/3/library/time.html

from ship import Ship
from search import *
from util import *
from log import Log


if __name__ == "__main__":
    ship = create_ship(
        "ShipCase/ShipCase3.txt",
        "load_unload.txt",
        "OUTBOUNDShipCase/OUTBOUNDshipcasetest.txt",
    )
    print(ship)
    ship.print_weights()

    # Test balance search
    start_time = time()
    sol = uniform_cost_balance(ship, "cntr-cross")
    print(f"Timer: {round(time() - start_time, 5)} seconds")

    if sol != None:
        print(sol.moves)
        print(sol.time_cost, sol.cntr_cross_bal_heuristic)

    # Test loads unloads search
    # cntr1 = Container([0, 0], 5, "Cat", [ship.row, ship.col])
    # cntr2 = Container([0, 0], 10, "Cat", [ship.row, ship.col])
    # ship.loads = [cntr1, cntr2]
    # ship.ship_state[7][1].selected = True

    # start_time = time()
    # sol = uniform_cost_lu(ship)
    # print(f"Timer: {round(time() - start_time, 5)} seconds")

    # if sol != None:
    #     print(sol.moves)
    #     print(sol.time_cost, sol.cntr_cross_bal_heuristic)

    # Keep these commented unless testing logs
    # log = Log("testlog")
    # log.writelog("Testing Log")
    # log.writecomment("Good Day Sir")
    # log.readlog(printlog=True)
