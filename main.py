from ship import Ship
from shiputil import *
from log import Log


def create_ship(manifest_filename, op_filename, outbound_filename):
    """Input filename of manifest, parses file contents. Returns ship object."""
    # https://www.pythontutorial.net/python-basics/python-read-text-file/
    with open(manifest_filename) as f:
        manifest_cntnt = [line for line in f.readlines()]
    with open(op_filename) as f:
        loads = f.readline().strip().split(",")
        unloads = f.readline().strip().split(",")

    ret = Ship(manifest_cntnt, loads, unloads)
    # ret.ship_state = [['UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED'],
    #                   ['UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED'],
    #                   ['UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED'],
    #                   ['UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED'],
    #                   ['UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED'],
    #                   ['UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED'],
    #                   ['UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED'],
    #                   ['NAN',    'Cat'   , 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'NAN']]

    print(ret)
    # ret.print_weights()
    # print(ret.is_balanced())
    print(get_moves(ret, [7, 2], [7, 4]))
    outbound_contents = ret.get_outbound_manifest()

    with open(outbound_filename, "w+") as f:
        f.write(outbound_contents)

    return ret


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
