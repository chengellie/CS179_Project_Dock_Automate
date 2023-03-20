from ship import Ship


def get_moves(ship: Ship, start_pos, end_pos):
    """Input ship, start and end pos. Returns list of coordinates to move container from start to end."""
    coord = []

    # find higest row container needs to move to, first empty row between start_pos and end_pos
    if start_pos[1] < end_pos[1]:
        left = start_pos
        right = end_pos
        inc = 1
    else:
        left = end_pos
        right = start_pos
        inc = -1
    max_height = left[0]
    for j in range(left[1] + 1, right[1] + 1):
        while ship.ship_state[max_height][j].name != "UNUSED":
            max_height -= 1

    # insert moves up
    for i in range(start_pos[0], max_height - 1, -1):
        coord.append([i, start_pos[1]])

    # insert horizontal moves
    if inc == 1:
        for j in range(start_pos[1] + 1, end_pos[1] + 1, 1):
            coord.append([max_height, j])
    else:
        for j in range(start_pos[1] - 1, end_pos[1] - 1, -1):
            coord.append([max_height, j])

    # insert moves down
    for i in range(max_height + 1, end_pos[0] + 1, 1):
        coord.append([i, end_pos[1]])

    return coord


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
