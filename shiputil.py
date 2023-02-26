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
