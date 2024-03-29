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
    manifest_filename: str, op_filename: str=""
) -> Ship:
    """Input filename of manifest, parses file contents. Returns ship object."""
    # https://www.pythontutorial.net/python-basics/python-read-text-file/
    with open(manifest_filename) as f:
        manifest_cntnt = [line for line in f.readlines()]

    ship = Ship()
    ship.init_ship_state_manifest(manifest_cntnt)

    if op_filename != "":
        ship.loads, ship.unloads = unpack_actions(ship, op_filename, ship.row, ship.col)
        ship.unloads = [ship.find_best_cntr(cntr) for cntr in ship.unloads]

        ship.init_goal_state()

    return ship

# def create_ship_lu(
#     manifest_filename: str, op_filename: str, outbound_filename: str
# ) -> Ship:
#     """Input filename of manifest, parses file contents. Returns ship object."""
#     # https://www.pythontutorial.net/python-basics/python-read-text-file/
#     with open(manifest_filename) as f:
#         manifest_cntnt = [line for line in f.readlines()]
#     # with open(op_filename) as f:
#     #     loads = f.readline().strip().split(",")
#     #     unloads = f.readline().strip().split(",")

#     ship = Ship()
#     ship.init_ship_state_manifest(manifest_cntnt)


#     ship.init_goal_state()

#     return ship


def unpack_actions(ship: Ship, op_filename: str, row: int, col: int):
    actions = pd.read_csv(op_filename)
    loads = []
    unloads = []
    for i in actions.index:
        if actions["type"][i] == "Unload":
            unloads.append(
                setup_cntr(ship, [int(x) for x in actions["coords"][i].split("_")])
            )
        else:
            for j in range(0, int(actions["qty"][i])):
                new_cntr = Container([-1, -1], actions["weight"][i], actions["name"][i], [row, col])
                new_cntr.set_ship_coord([-1, -1])
                loads.append(new_cntr)

            # loads.extend([actions['name'][i]]*int(actions['qty'][i]))

    return loads, set(unloads)


def setup_cntr(ship: Ship, cntr: list, selecting: bool = True) -> Container:
    selected_cntr = ship.get_cntr(cntr)
    selected_cntr.selected = selecting

    return selected_cntr
