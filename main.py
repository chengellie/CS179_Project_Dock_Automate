import csv
import copy
from typing import Optional, Set
from ship import Ship
from search import *
from shiputil import *
from log import Log


if __name__ == "__main__":
    ship = create_ship(
        "ShipCase/ShipCase2.txt",
        "load_unload.txt",
        "OUTBOUNDShipCase/OUTBOUNDshipcasetest.txt",
    )
    print(ship)

    # sol = breadth_first_balance(ship)
    # print(sol.moves)
    # sol.print_weights()

    sol = uniform_cost_balance(ship)
    if sol != None:
        print(sol.moves)

    # Keep these commented unless testing logs
    # log = Log("testlog")
    # log.writelog("Testing Log")
    # log.writecomment("Good Day Sir")
    # log.readlog(printlog=True)
