import copy
from container import Container
from typing import List, Set, Optional

# modify or remove get columns, unneeded. instead have search and find depth go rowwise instead. (search algo will mark matching containers. list stores them in depth order (will shift accordingly)


class Ship:
    def __init__(self, ship_state: Optional[List[Container]] = []) -> None:
        self.ship_state = ship_state
        self.loads = []
        self.unloads = {}
        self.goal_state = {}
        self.row = 8
        self.col = 12
        self.crane_loc = -1
        self.crane_mode = None
        self.balance_mass = -1
        self.time_cost = 0
        self.cntr_cross_bal_heuristic = 0
        self.cntr_lu_heuristic = 0
        self.col_move_bal_heuristic = 0
        self.moves = []
        self.cntrs_in_row = []

    def __init_balance_mass(self):
        """Input None,, computes minimum mass of lighter half for balanced ship. Returns None."""
        left, right, _, _ = self.get_left_right_mass()
        self.balance_mass = (0.9 * (left + right)) // 1.9
        # todo: is it floor or ceiling?

    def init_ship_state_manifest(self, manifest: List[str]) -> None:
        """Input manifest, constructs container objects and fills ship with containers. Returns None."""
        self.ship_state = [[None for j in range(self.col)] for i in range(self.row)]

        # extract container details from manifest list
        containers = []
        for item in manifest:
            coord = [int(item[1:3]), int(item[4:6])]
            weight = int(item[10:15])
            name = item[18:].strip()
            c = Container(coord, weight, name, [self.row, self.col])
            containers.append(c)

        # fill in 2d list for ship_state with containers
        k = 0
        for i in range(self.row - 1, -1, -1):
            cntr_row = {}
            for j in range(self.col):
                self.ship_state[i][j] = containers[k]
                k += 1

        # get count of all containers in a row from top to bottom and depth to the top of that column
        self.top_columns = [-1] * self.col
        for i, row in enumerate(self.ship_state):
            cntr_row = {}
            for j, cntr in enumerate(row):
                if cntr.name not in cntr_row:
                    cntr_row[cntr.name] = []
                    # cntr_row[cntr.name] = 0
                cntr_row[cntr.name].append([i, j])
                # cntr_row[cntr.name] += 1
                if cntr.name == "UNUSED":
                    self.top_columns[j] += 1
            self.cntrs_in_row.append(cntr_row)

        self.__init_balance_mass()

    def init_goal_state(self) -> None:
        """Inputs None, constructs goal state dictionary with number of each type of container. Returns None."""
        for row in self.ship_state:
            for cntr in row:
                cntr_name = cntr.name
                if cntr_name == "UNUSED" or cntr_name == "NAN":
                    continue
                # TODO: temporarily using selected to identify unloads
                if cntr.selected == True:
                    continue
                # TODO: defaultdict?
                if cntr_name in self.goal_state.keys():
                    self.goal_state[cntr_name] += 1
                else:
                    self.goal_state[cntr_name] = 1

        # simulating ship state after all actions completed
        for cntr in self.loads:
            cntr_name = cntr.name
            if cntr_name in self.goal_state.keys():
                self.goal_state[cntr_name] += 1
            else:
                self.goal_state[cntr_name] = 1

        # for cntr_name in unloads:
        #     if cntr_name in self.goal_state.keys():
        #         self.goal_state[cntr_name] -= 1
        #         if self.goal_state[cntr_name] == 0:
        #             del self.goal_state[cntr_name]
        #     else:
        #         print("Error: trying to unload item that is not in ship")
        #         return

    def is_goal_state(self) -> bool:
        """Inputs None, Returns if current ship_state matches goal_state."""
        curr_state = {}
        for row in self.ship_state:
            for cntr in row:
                cntr_name = cntr.name
                if cntr_name == "UNUSED" or cntr_name == "NAN":
                    continue
                if cntr_name in curr_state.keys():
                    curr_state[cntr_name] += 1
                else:
                    curr_state[cntr_name] = 1
        return curr_state == self.goal_state

    def __str__(self) -> str:
        """Inputs None, prints container names in grid format. Returns None."""
        ret = ""
        for row in self.ship_state:
            for cntr in row:
                ret += cntr.get_shortened_name() + " "
            ret += "\n"
        return ret

    def print_weights(self) -> None:
        """Inputs None, prints container weights in grid format using -1 for NAN containers. Returns None."""
        ret = ""
        for row in self.ship_state:
            for cntr in row:
                if cntr.name != "NAN":
                    str_weight = str(cntr.weight)[:6]
                else:
                    str_weight = "NAN"
                shortened = str_weight.ljust(6)
                ret += shortened + " "
            ret += "\n"
        print(ret)

    def generate_ship_key(self) -> str:
        """Inputs None, Returns unique identifier for ship as a string."""
        ret = ""
        for row in self.ship_state:
            for cntr in row:
                ret += cntr.name
        ret += str(self.crane_loc)
        if self.crane_loc == self.col:
            ret += self.crane_mode
        return ret

    def get_left_right_mass(self) -> int:
        """Inputs None. Returns mass of the left and right half of the ship."""
        left = 0
        right = 0
        l_weights = []
        r_weights = []
        for row in self.ship_state:
            for j, cntr in enumerate(row):
                if j >= 0 and j < self.col / 2:
                    left += cntr.weight
                    if cntr.weight != 0:
                        l_weights.append((cntr.weight, j))
                else:
                    right += cntr.weight
                    if cntr.weight != 0:
                        r_weights.append((cntr.weight, j))
        return left, right, l_weights, r_weights

    def set_cntr_cross_bal_heuristic(self) -> None:
        """Inputs None, computes heuristic for balance. Returns None.
        h(n) = minimum number of containers that need to be moved across mid-line to achieve balanced ship
        """
        left, right, l_weights, r_weights = self.get_left_right_mass()
        deficit = self.balance_mass - min(left, right)
        weights = l_weights if left > right else r_weights
        weights.sort(reverse=True)
        # print(self.balance_mass, weights, deficit)

        cnt = 0
        for w in weights:
            if deficit <= 0:
                break
            if w[0] <= deficit:
                cnt += 1
                deficit -= w[0]

        self.cntr_cross_bal_heuristic = cnt

    def set_cntr_lu_heuristic(self) -> None:
        cnt = 0
        for cntr in self.unloads:
            cnt += self.get_container_depth(cntr)
        self.cntr_lu_heuristic = cnt

    # def set_col_move_bal_heuristic(self) -> None:
    #     """Inputs None, computes heuristic for balance. Returns None.
    #     h(n) = minimum number of columns to move the minimum number of containers across mid-line to achieve balanced ship
    #     """
    #     left, right, l_weights, r_weights = self.get_left_right_mass()
    #     deficit = self.balance_mass - min(left, right)
    #     weights = l_weights if left > right else r_weights
    #     weights.sort(reverse=True)
    #     # print(self.balance_mass, weights, deficit)

    #     cnt = 0
    #     for w in weights:
    #         if deficit <= 0:
    #             break
    #         if w <= deficit:
    #             cnt +=
    #             deficit -= w

    #     self.cntr_cross_bal_heuristic = cnt

    def is_balanced(self) -> bool:
        """Inputs None, Returns if ship is balanced.
        Balanced ship: mass of the lighter side is within 10% the mass of the heavier side
        (including exactly 10%)
        """
        left, right, _, _ = self.get_left_right_mass()

        # determine if ship is balanced
        if left < right and left >= 0.9 * right:
            return True
        elif right < left and right >= 0.9 * left:
            return True
        elif left == right:
            return True
        else:
            return False

    def get_outbound_manifest(self) -> str:
        """Inputs None, Returns contents for outbound manifest."""
        ret = ""
        for i in range(self.row - 1, -1, -1):
            for j in range(self.col):
                ret += self.ship_state[i][j].get_manifest_format()
                if not (i == 0 and j == self.col - 1):
                    ret += "\n"
        return ret

    def get_container_depth(self, cntr: Container) -> int:
        """Inputs container. Returns number of containers above current container."""
        i, j = cntr.ship_coord
        return i - self.top_columns[j] - 1

    """Takes in a Container and finds the container that is best to unload (given it was not marked)"""
    # TODO: Find a way to mark containers that are already considered
    # TODO: If remove coords in container, just take in a size 2 list instead and do a trycatch
    def find_best_cntr(self, unload_cntr: Container) -> Container:
        cntr_name = unload_cntr.name
        orig_cntr = unload_cntr
        curr_cntr = unload_cntr

        # compute depth and choose this container if smaller depth (preferably choose one in higher point)
        for i, row in enumerate(self.cntrs_in_row):
            if (
                cntr_name in row and orig_cntr.ship_coord not in row[cntr_name]
            ):  # container exists in this row and isn't the original
                for pot_cntr_coord in row[cntr_name]:
                    pot_cntr = self.get_cntr(pot_cntr_coord)
                    pot_cntr_depth = self.get_container_depth(pot_cntr)
                    curr_cntr_depth = self.get_container_depth(curr_cntr)
                    if not pot_cntr.selected:
                        if (pot_cntr_depth < curr_cntr_depth) or (
                            pot_cntr_depth == curr_cntr_depth
                            and pot_cntr_coord[0] < curr_cntr.ship_coord[0]
                        ):  # same depth, which one is higher? (Less crane movement time)
                            unload_cntr.selected = False
                            unload_cntr = pot_cntr
                            unload_cntr.selected = True
                            curr_cntr = unload_cntr

        return unload_cntr

    def get_cntr(self, coords):
        return self.ship_state[coords[0]][coords[1]]

    def add_cntr(self, cntr: Container, col: int) -> List[int]:
        if not cntr:
            # print("Add Failed: Empty Container")
            return

        row = self.top_columns[col]
        if row <= -1:
            # print(f"Add Failed: Full Column {col}")
            return
        cntr.set_ship_coord([row, col])
        # cntr.ship_coord = [row, col]

        # Mark container coord as used
        self.ship_state[row][col] = cntr
        self.top_columns[col] -= 1
        self.cntrs_in_row[row]["UNUSED"].remove([row, col])

        # Add container to row list
        if cntr.name not in self.cntrs_in_row[row]:
            self.cntrs_in_row[row][cntr.name] = []
        self.cntrs_in_row[row][cntr.name].append([row, col])

        return [row, col]

    def remove_cntr(self, col: int) -> Container:
        row = self.top_columns[col] + 1

        if row >= 8 or self.ship_state[row][col].name == "NAN":
            # print(f"Remove Failed: Empty Column {col}")
            return None

        # Get container being removed
        removed_cntr = self.ship_state[row][col]

        # Mark top coord of column unused
        self.ship_state[row][col] = Container(
            [-1, -1], 0, "UNUSED", [self.row, self.col]
        )
        self.ship_state[row][col].set_ship_coord([row, col])

        if "UNUSED" not in self.cntrs_in_row[row]:
            self.cntrs_in_row[row]["UNUSED"] = []
        self.cntrs_in_row[row]["UNUSED"].append([row, col])

        # Remove container from row list and update top columns
        self.cntrs_in_row[row][removed_cntr.name].remove([row, col])
        self.top_columns[col] = row

        return removed_cntr

    def get_col_top_cntr_coord(self, col: int):
        """Inputs column. Returns row index of first container in ship_state or -1 if col is empty."""
        return [self.get_columns[col] + 1, col]

    def get_col_top_cntr_depth(self, col: int) -> int:
        """Inputs column. Returns row index of first container in ship_state or -1 if col is empty."""
        # TODO: remove debug
        if col == 12:
            print("issue\n", self, self.crane_loc, col)

        i = 0
        while i < self.row and self.ship_state[i][col].name == "UNUSED":
            i += 1

        if i >= self.row or self.ship_state[i][col].name == "NAN":
            return -1
        else:
            return i

    def get_col_top_empty_coord(self, col: int):
        """Inputs column. Returns row index of last empty slot in ship_state or -1 if col is full."""
        return [self.top_columns[col], col]

    def get_col_top_empty_depth(self, col: int) -> int:
        """Inputs column. Returns row index of last empty slot in ship_state or -1 if col is full."""
        i = self.row - 1
        while i >= 0 and (self.ship_state[i][col].name != "UNUSED"):
            i -= 1

        if i < 0:
            return -1
        else:
            return i

    def is_full_col(self, col: int) -> bool:
        """Inputs column number. Returns whether column is full."""
        return self.ship_state[0][col].name != "UNUSED"

    # todo: deal with nan for empty cols and computation
    def is_empty_col(self, col: int) -> bool:
        """Inputs column number. Returns whe ther column is empty."""
        if self.ship_state[self.row - 1][col].name == "UNUSED":
            return True

        i = self.row - 1
        # print(i, col, self)
        while i >= 0 and self.ship_state[i][col].name != "UNUSED":
            i -= 1

        if i < 0:  # entire col is filled, either containers or NAN
            return False
        elif i >= 0 and self.ship_state[i + 1][col].name == "NAN":
            return True
        elif i >= 0 and self.ship_state[i + 1][col].name != "NAN":
            return False
        else:
            print("Error: uncaught condition for empty column")
            return False

    # def get_ship_columns(self, indx: int = -1):
    #     """Gets list of all containers of all or a single column. Returns None."""
    #     rowlength = len(self.ship_state[0])
    #     columns = [[] for i in range(0, rowlength if indx == -1 else 1)]

    #     for row in self.ship_state:
    #         if indx == -1:
    #             for i in range(0, rowlength):
    #                 columns[i].append(row[i])
    #         else:
    #             columns[0].append(row[indx])

    #     return columns

    def swap_cntr(self, col1: int, col2: int) -> None:
        self.add_cntr(self.remove_cntr(col1), col2)

    # def swap_cntr_pos(self, pos1: List[int], pos2: List[int]) -> None:
    #     temp = self.ship_state[pos1[0]][pos1[1]]
    #     print(temp.name, pos1, pos2)
    #     self.ship_state[pos1[0]][pos1[1]] = self.ship_state[pos2[0]][pos2[1]]
    #     self.ship_state[pos2[0]][pos2[1]] = temp
    #     temp = self.ship_state[pos1[0]][pos1[1]].get_manifest_coord()
    #     self.ship_state[pos1[0]][pos1[1]].set_manifest_coord(
    #         self.ship_state[pos2[0]][pos2[1]].get_manifest_coord()
    #     )
    #     self.ship_state[pos2[0]][pos2[1]].set_manifest_coord(temp)

    def get_moves(self, start_pos, end_pos):
        """Input start and end pos. Returns list of coordinates to move container from start to end."""
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

        # max_height = self.row - min(self.top_columns[(left[1] + 1):(right[1] + 1)]) - 1
        max_height = left[0]
        for j in range(left[1] + 1, right[1]):
            # TODO: is max_height fix ok?
            while max_height >= 0 and self.ship_state[max_height][j].name != "UNUSED":
                max_height -= 1
        max_height = min(max_height, right[0])

        # insert moves up
        for i in range(start_pos[0], max_height - 1, -1):
            coord.append([i, start_pos[1]])

        # insert horizontal moves
        for j in range(start_pos[1] + inc, end_pos[1] + inc, inc):
            coord.append([max_height, j])
        # if inc == 1:
        #     for j in range(start_pos[1] + 1, end_pos[1] + 1, 1):
        #         coord.append([max_height, j])
        # else:
        #     for j in range(start_pos[1] - 1, end_pos[1] - 1, -1):
        #         coord.append([max_height, j])

        # insert moves down
        for i in range(max_height + 1, end_pos[0] + 1, 1):
            coord.append([i, end_pos[1]])
        return coord

    def move_cntr(self, col_get: int, col_put: int) -> bool:
        """Inputs column to get container from and move container to. Returns None."""
        # return if moving container from and to same col
        if col_get == col_put:
            print("Error: Container is not being moved")
            return False

        row_get = self.get_col_top_cntr_depth(col_get)
        # row_get = self.top_columns[col_get] + 1
        # if row_get == self.row or self.ship_state[row_get][col_get].name == "NAN":
        if row_get == -1:
            print("Error: No container to get in column", col_get)
            return False
        elif self.ship_state[row_get][col_get].selected == True:
            print("Picking Up Desired Container")
            return False

        row_put = self.get_col_top_empty_depth(col_put)
        # row_put = self.top_columns[col_put]
        if row_put == -1:
            print("Error: Cannot put container in this column, column is full.")
            return False
        # update cost and moves
        self.time_cost += (
            len(self.get_moves([row_put, col_put], [row_get, col_get])) - 1
        )
        self.swap_cntr(col_get, col_put)
        # self.swap_cntr_pos([row_put, col_put], [row_get, col_get])
        self.moves.append([row_get, col_get])
        self.moves.append([row_put, col_put])

        return True

    def time_between_pink_cell(self, col: int, type: str) -> int:
        """Inputs column to move crane to and whether cell contains a container.
        Returns cost of moving crane from pink cell to top container of col.
        """
        if type == "cntr":
            row = self.get_col_top_cntr_depth(col)
            if row == -1:
                print("Error: cannot get from column", col)
                return -1
        elif type == "empty":
            row = self.get_col_top_empty_depth(col)
            if row == -1:
                print("Error: cannot put in column", col)
                return -1
        return col + row

    def time_between_col(self, start_col: int, end_col: int) -> int:
        """Inputs two columns. Returns cost of moving crane from top container of start col to top container of end col"""
        # return if moving container from and to same col
        if start_col == end_col:
            # print("Debug:", start_col, end_col)
            # print(self)
            # print("Error: Container is not being moved")
            return -1

        start_row = self.get_col_top_cntr_depth(start_col)
        # row_get = self.top_columns[col_get] + 1
        # if row_get == self.row or self.ship_state[row_get][col_get].name == "NAN":
        if start_row == -1:
            # print("Error: No container that was previously put in column", start_col)
            return -1

        end_row = self.get_col_top_cntr_depth(end_col)
        # row_put = self.top_columns[col_put]
        if end_row == -1:
            print("Error: No container to get from column", end_col)
            return -1
        # update cost and moves
        return len(self.get_moves([start_row, start_col], [end_row, end_col])) - 1

    def move_toward_loading_area(self):
        """Inputs heuristic. Returns new Ship object after move, None if move not valid."""
        if self.crane_mode == "get":
            new_crane_mode = "put"
        elif self.crane_mode == "put" or self.crane_mode == None:
            new_crane_mode = "get"
        else:
            print("Error: current crane_mode is not a valid option")
            return None

        if new_crane_mode == "get":
            # check if there is nothing else to load
            if not self.loads:
                print("Error: no containers to load onto ship")
                return None
            else:
                # cost from previous put to truck
                new_ship = copy.deepcopy(self)
                new_ship.crane_loc = self.col
                new_ship.crane_mode = new_crane_mode
                if self.crane_mode == None:
                    new_ship.time_cost += 2
                else:
                    new_ship.time_cost += (
                        new_ship.time_between_pink_cell(self.crane_loc, "cntr") + 2
                    )
        elif new_crane_mode == "put":
            start_col = self.crane_loc
            start_row = self.get_col_top_cntr_depth(start_col)
            # check if current container needs to be unloaded
            if self.ship_state[start_row][start_col].selected == True:
                # cost from previous put to truck
                new_ship = copy.deepcopy(self)
                new_ship.crane_loc = self.col
                new_ship.crane_mode = new_crane_mode
                new_ship.time_cost += (
                    new_ship.time_between_pink_cell(self.crane_loc, "cntr") + 2
                )
                removed_cntr = new_ship.remove_cntr(self.crane_loc)
                new_ship.moves.extend([removed_cntr.ship_coord, [-1, -1]])

                if removed_cntr in new_ship.unloads:
                    print(f"Removing {removed_cntr.name}")
                    new_ship.unloads.remove(removed_cntr)
            else:
                print("Error: Container does not need to be unloaded")
                return None

        return new_ship

    def move_away_loading_area(self, col: int):
        """Inputs column to move crane to and heuristic. Returns new Ship object after move, None if move not valid."""
        if self.crane_mode == "get":
            new_crane_mode = "put"
        elif self.crane_mode == "put" or self.crane_mode == None:
            new_crane_mode = "get"
        else:
            print("Error: current crane_mode is not a valid option")
            return None

        if new_crane_mode == "get":
            # cost from truck to current get
            new_ship = copy.deepcopy(self)
            new_ship.crane_loc = col
            new_ship.crane_mode = new_crane_mode
            new_ship.time_cost += new_ship.time_between_pink_cell(col, "cntr") + 2
        elif new_crane_mode == "put":
            # cost from previous put to truck
            new_ship = copy.deepcopy(self)
            new_ship.crane_loc = col
            new_ship.crane_mode = new_crane_mode
            new_ship.time_cost += new_ship.time_between_pink_cell(col, "empty") + 2
            new_cntr_coord = new_ship.add_cntr(new_ship.loads.pop(), col)

            new_ship.moves.extend([[-1, -1], new_cntr_coord])

        return new_ship

    def load_unload_loading_area(self):
        """Inputs None. Returns new Ship object after move, None if move not valid."""
        # check if there is nothing else to load
        if not self.loads:
            print("Error: no containers to load onto ship")
            return None
        else:
            # cost from previous put to truck
            new_ship = copy.deepcopy(self)
            new_ship.crane_loc = self.col
            new_ship.crane_mode = "get"

        return new_ship

    # TODO: when unload is reached, unload can be placed on any of other ship cols or truck
    def move_crane(self, col: int, heuristic: str = None):
        """Inputs column to move crane to. Returns new Ship object after move, None if move not valid."""
        if self.crane_mode == "get":
            new_crane_mode = "put"
        elif self.crane_mode == "put" or self.crane_mode == None:
            new_crane_mode = "get"
        else:
            print("Error: current crane_mode is not a valid option")
            return None

        # check if crane is getting container from empty col or NAN col
        if (
            new_crane_mode == "get"
            and col != self.col
            and (self.is_empty_col(col) or self.ship_state[0][col].name == "NAN")
        ):
            return None

        # check if crane is putting container to full col or NAN col
        if new_crane_mode == "put" and col != self.col and self.is_full_col(col):
            return None

        # check crane_loc is not being moved to same col as get
        # if new_crane_mode == "put" and col == self.crane_loc:
        if col == self.crane_loc:
            return None

        # check if crane is in loading area
        if col == self.col and self.crane_loc == self.col and new_crane_mode == "get":
            new_ship = self.load_unload_loading_area()
        elif col == self.col:
            new_ship = self.move_toward_loading_area()
        elif self.crane_loc == self.col:
            new_ship = self.move_away_loading_area(col)
        else:
            # construct new ship with move performed
            new_ship = copy.deepcopy(self)
            new_ship.crane_loc = col
            new_ship.crane_mode = new_crane_mode

            # perform move if new_crane_mode is put
            if new_crane_mode == "put":
                if new_ship.move_cntr(self.crane_loc, col) == False:
                    return
            elif new_crane_mode == "get":
                if self.crane_mode == None:
                    # TOOD: check functionality of code below
                    new_ship.time_cost += new_ship.time_between_pink_cell(
                        new_ship.crane_loc, "cntr"
                    )
                else:
                    new_ship.time_cost += new_ship.time_between_col(
                        self.crane_loc, new_ship.crane_loc
                    )

        if new_ship is None:
            return None
        elif heuristic == "cntr-cross":
            new_ship.set_cntr_cross_bal_heuristic()
        elif heuristic == "cntr-lu":
            new_ship.set_cntr_lu_heuristic()
        # TODO: if goal_state is reached, still need to move crane back to pink cell and include that in search
        return new_ship
