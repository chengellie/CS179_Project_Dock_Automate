from ship import Ship
from log import Log


def create_ship(manifest_filename, op_filename):
    """Input filename of manifest, parses file contents. Returns ship object."""
    # https://www.pythontutorial.net/python-basics/python-read-text-file/
    with open(manifest_filename) as f:
        manifest_cntnt = [line for line in f.readlines()]
    with open(op_filename) as f:
        loads = f.readline().strip().split(",")
        unloads = f.readline().strip().split(",")
    ret = Ship(manifest_cntnt, loads, unloads)
    print(ret.check_goal_state())
    return ret


if __name__ == "__main__":
    create_ship("ShipCase1.txt", "load_unload.txt")
    Log("").writelog("Testing Log")
