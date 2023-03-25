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
    sol = uniform_cost_lu(ship, "cntr-lu")
    print(f"Timer: {round(time() - start_time, 5)} seconds")

    if sol != None:
        print(sol.moves)
        print(sol.time_cost, sol.cntr_lu_heuristic)


if __name__ == "__main__":
    # with open("data/action_list.csv", mode="w", newline="") as csvfile:
    #     file_writer = csv.writer(
    #         csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
    #     )
    #     file_writer.writerow(["name", "qty", "type", "coords", "weight"])
    #     # file_writer.writerow(['Cat',1,'Unload','7_1',99])
    #     # file_writer.writerow(['Bat',1,'Load',"N/A",5432])
    #     file_writer.writerow(["Cow", 1, "Unload", "7_1", 500])
    #     file_writer.writerow(["Rat", 1, "Load", "N/A", 5397])

    ship = create_ship("ShipCase/ShipCase5.txt", "data/test_list.csv")
    # balance(ship)
    load_unload_ship(ship)

    # Keep these commented unless testing logs
    # log = Log("testlog")
    # log.writelog("Testing Log")
    # log.writecomment("Good Day Sir")
    # log.readlog(printlog=True)
