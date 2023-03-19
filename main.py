import csv
from typing import Optional, Set
from ship import Ship
from shiputil import *
from log import Log


if __name__ == "__main__":
    create_ship(
        "ShipCase/shipcasetest.txt",
        "load_unload.txt",
        "OUTBOUNDShipCase/OUTBOUNDshipcasetest.txt",
    )

    # Keep these commented unless testing logs
    # log = Log("testlog")
    # log.writelog("Testing Log")
    # log.writecomment("Good Day Sir")
    # log.readlog(printlog=True)
