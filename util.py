from dataclasses import dataclass, field
from typing import Any
from container import Container
from ship import Ship
import pandas as pd

# https://stackoverflow.com/questions/66448588/is-there-a-way-to-make-a-priority-queue-sort-by-the-priority-value-in-a-tuple-on?noredirect=1&lq=1
@dataclass(order=True)
class PrioritizedShip:
    priority: int
    item: Any = field(compare=False)


def create_ship(
    manifest_filename: str, op_filename: str, outbound_filename: str
) -> Ship:
    """Input filename of manifest, parses file contents. Returns ship object."""
    # https://www.pythontutorial.net/python-basics/python-read-text-file/
    with open(manifest_filename) as f:
        manifest_cntnt = [line for line in f.readlines()]
    with open(op_filename) as f:
        loads = f.readline().strip().split(",")
        unloads = f.readline().strip().split(",")

    ship = Ship()
    ship.init_ship_state_manifest(manifest_cntnt)

    cntr1 = Container([0, 0], 5, "Cat", [ship.row, ship.col])
    cntr2 = Container([0, 0], 10, "Cat", [ship.row, ship.col])
    loads = []
    ship.ship_state[7][1].selected = True
    ship.init_goal_state(loads, {})

    return ship


def unpack_actions(op_filename: str, row: int, col: int):
    actions = pd.read_csv(op_filename)
    loads = []
    unloads = []
    for i in actions.index:
        if actions["type"][i] == "Unload":
            unloads.append([int(x) for x in actions["coords"][i].split("_")])
        else:
            for j in range(0, int(actions["qty"][i])):
                loads.append(
                    Container(
                        [-1, -1], actions["weight"][i], actions["name"][i], [row, col]
                    )
                )

            # loads.extend([actions['name'][i]]*int(actions['qty'][i]))

    return loads, unloads


def setup_cntr(ship: Ship, cntr: list, selecting: bool = True) -> Container:
    selected_cntr = ship.get_cntr(cntr)
    selected_cntr.selected = selecting

    return selected_cntr


# TODO: Make Unmark Container Function
