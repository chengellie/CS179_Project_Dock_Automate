from ship import Ship
import pandas as pd

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

    ship1 = Ship()
    ship1.init_ship_state_manifest(manifest_cntnt)
    # ship1.init_goal_state(loads, unloads)

    # cntr_names = []
    # with open("ShipState1.txt") as f:
    #     cntr_names = list(csv.reader(f))

    # ship2 = Ship(cntr_names=cntr_names)

    # print(ship1)

    # ship1.print_weights()
    # print(ship1.is_balanced())
    # print(get_moves(ship1, [7, 2], [7, 4]))
    # outbound_contents = ship1.get_outbound_manifest()

    # with open(outbound_filename, "w+") as f:
    #     f.write(outbound_contents)

    return ship1

def unpack_actions(op_filename:str):
    actions = pd.read_csv(op_filename)
    loads = []
    unloads = []
    for i in actions.index:
        if actions['type'][i] == "Unload":
            unloads.append([int(x) for x in actions['coords'][i].split('_')])
        else:
            loads.extend([actions['name'][i].split('_')*int(actions['qty'][i])])

    return loads, unloads