import csv
import copy
from typing import Optional, Set
from ship import Ship
from search import *
from shiputil import *
from log import Log


if __name__ == "__main__":
    ship = create_ship(
        "ShipCase/ShipCase4.txt",
        "load_unload.txt",
        "OUTBOUNDShipCase/OUTBOUNDshipcasetest.txt",
    )

    # print("search debug")
    # ship_copy = copy.deepcopy(ship)
    # print(ship.is_empty_col(0))
    # ship_copy.move_cntr(1, 11)
    # ship_copy.move_cntr(2, 11)
    # print(ship.is_full_col(1))
    sol = uniform_cost_balance(ship)
    print(sol.moves)
    sol.print_weights()
    # if sol != None:
    #     print(sol.moves)
    # Keep these commented unless testing logs
    # log = Log("testlog")
    # log.writelog("Testing Log")
    # log.writecomment("Good Day Sir")
    # log.readlog(printlog=True)
