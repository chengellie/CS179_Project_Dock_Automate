import copy
from container import Container
from typing import List, Optional

# modify or remove get columns, unneeded. instead have search and find depth go rowwise instead. (search algo will mark matching containers. list stores them in depth order (will shift accordingly)


class Ship:
    def __init__(self, ship_state: Optional[List[Container]] = []) -> None:
        self.ship_state = ship_state
        self.goal_state = {}
        self.row = 8
        self.col = 12
        self.crane_loc = -1
        self.crane_mode = None
        self.moves = []
        self.cntrs_in_row = []

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

    def init_goal_state(self, loads: List[str], unloads: List[str]) -> None:
        """Inputs None, constructs goal state dictionary with number of each type of container. Returns None."""
        for row in self.ship_state:
            for cntr in row:
                cntr_name = cntr.name
                if cntr_name == "UNUSED" or cntr_name == "NAN":
                    continue
                if cntr_name in self.goal_state.keys():
                    self.goal_state[cntr_name] += 1
                else:
                    self.goal_state[cntr_name] = 1

        # simulating ship state after all actions completed
        for cntr_name in loads:
            if cntr_name in self.goal_state.keys():
                self.goal_state[cntr_name] += 1
            else:
                self.goal_state[cntr_name] = 1

        for cntr_name in unloads:
            if cntr_name in self.goal_state.keys():
                self.goal_state[cntr_name] -= 1
                if self.goal_state[cntr_name] == 0:
                    del self.goal_state[cntr_name]
            else:
                print("Error: trying to unload item that is not in ship")
                return

    def is_goal_state(self) -> bool:
        """Inputs None, Returns if current ship_state matches goal_state."""
        curr_state = {}
        for row in self.ship_state:
            for cntr in row:
                cntr_name = cntr.name
                if cntr_name == "UNUSED" or cntr_name == "NAN":
                    continue
                if cntr_name in self.curr_state.keys():
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
        ret += str(self.crane_loc) + str(self.move_crane)
        return ret

    def is_balanced(self) -> bool:
        """Inputs None, Returns if ship is balanced.
        Balanced ship: mass of the lighter side is within 10% the mass of the heavier side
        (including exactly 10%)
        """
        # find mass of left and right half
        left = 0
        right = 0
        for row in self.ship_state:
            for j, cntr in enumerate(row):
                if j >= 0 and j < self.col / 2:
                    left += cntr.weight
                else:
                    right += cntr.weight

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
        # i, j = cntr.ship_coord[5, 1][1, 2]
        # i -= 1  # start check at cell above current container
        # count = 0
        # while i >= 0 and self.ship_state[i][j] != "UNUSED":
        #     count += 1
        #     i -= 1
        # return count

    """Takes in a Container and finds the container that is best to unload (given it was not marked)"""
    # TODO: Find a way to mark containers that are already considered
    # TODO: If remove coords in container, just take in a size 2 list instead and do a trycatch
    def find_best_cntr(self, unload_cntr:Container) -> Container:
        cntr_name = unload_cntr.name
        orig_cntr_coord = unload_cntr.ship_coord
        curr_cntr_coord = orig_cntr_coord
        curr_cntr_depth = orig_cntr_coord[0] - self.top_columns[orig_cntr_coord[1]]

        # compute depth and choose this container if smaller depth (preferably choose one in higher point)
        for i, row in enumerate(self.cntrs_in_row):
            if cntr_name in row and orig_cntr_coord not in row[cntr_name]:   # container exists in this row and isn't the original (we can skip)
                for pot_cntr in row[cntr_name]:
                    if i - self.top_columns[pot_cntr[1]] < curr_cntr_depth:
                        unload_cntr = self.ship_state[i][pot_cntr[1]]

        return unload_cntr

    def add_cntr(self, cntr:Container, col:int) -> None:
        row = self.top_columns[col]
        if row <= -1:
            print("Full")
            return
        cntr.ship_coord = [row, col]
        
        # Mark container coord as used
        self.ship_state[row][col] = cntr
        self.top_columns[col] -= 1
        self.cntrs_in_row[row]["UNUSED"].remove([row,col])
        
        # Add container to row list
        if cntr.name not in self.cntrs_in_row[row]:
            self.cntrs_in_row[row][cntr.name] = []
        self.cntrs_in_row[row][cntr.name].append([row, col])
    
    def remove_cntr(self, col:int) -> Container:
        row = self.top_columns[col]+1

        if self.top_columns[col] >= 7 or self.ship_state[row][col].name == "NAN":
            print("Empty")
            return None 

        # Get container being removed
        removed_cntr = self.ship_state[row][col]

        # Mark top coord of column unused
        self.ship_state[row][col] = Container([row, col], 0, "UNUSED", [self.row, self.col])
        if "UNUSED" not in self.cntrs_in_row[row]:
            self.cntrs_in_row[row]["UNUSED"] = []
        self.cntrs_in_row[row]["UNUSED"].append([row,col])

        # Remove container from row list and update top columns
        self.cntrs_in_row[row][removed_cntr.name].remove([row, col])
        self.top_columns[col] = row

        return removed_cntr

    def get_col_top_cntr_depth(self, col: int) -> int:
        """Inputs column. Returns row index of first container in ship_state or -1 if col is empty."""
        i = 0
        while i < self.row and self.ship_state[i][col].name == "UNUSED":
            i += 1

        if i >= self.row or self.ship_state[i][col].name == "NAN":
            return -1
        else:
            return i

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

    def get_ship_columns(self, indx: int = -1):
        """Gets list of all containers of all or a single column. Returns None."""
        rowlength = len(self.ship_state[0])
        columns = [[] for i in range(0, rowlength if indx == -1 else 1)]

        for row in self.ship_state:
            if indx == -1:
                for i in range(0, rowlength):
                    columns[i].append(row[i])
            else:
                columns[0].append(row[indx])

        return columns

    def swap_cntr_pos(self, pos1: List[int], pos2: List[int]) -> None:
        temp = self.ship_state[pos1[0]][pos1[1]]
        self.ship_state[pos1[0]][pos1[1]] = self.ship_state[pos2[0]][pos2[1]]
        self.ship_state[pos2[0]][pos2[1]] = temp
        temp = self.ship_state[pos1[0]][pos1[1]].get_manifest_coord()
        self.ship_state[pos1[0]][pos1[1]].set_manifest_coord(
            self.ship_state[pos2[0]][pos2[1]].get_manifest_coord()
        )
        self.ship_state[pos2[0]][pos2[1]].set_manifest_coord(temp)

    def move_cntr(self, col_get: int, col_put: int) -> None:
        """Inputs column to get container from and move container to. Returns None."""
        row_get = self.get_col_top_cntr_depth(col_get)
        if row_get == -1:
            print("Error: No container to get in column", col_get)
            return

        row_put = self.get_col_top_empty_depth(col_put)
        if row_put == -1:
            print("Error: Cannot put container in this column, column is full.")
            return

        self.swap_cntr_pos([row_put, col_put], [row_get, col_get])
        # self.ship_state[row_put][col_put] = self.ship_state[row_get][col_get]
        # new_cntr = self.ship_state[row_put][col_put]
        # new_cntr.set_manifest_coord([row_put, col_put])

        # old_cntr = self.ship_state[row_get][col_get]
        # old_cntr.name = "UNUSED"
        # old_cntr.weight = 0
        # print(self)

    def move_crane(self, col: int):
        """Inputs column to move crane to. Returns new Ship object after move, None if move not valid."""
        if self.crane_mode == "get":
            new_crane_mode = "put"
        elif self.crane_mode == "put" or self.crane_mode == None:
            new_crane_mode = "get"
            self.crane_loc = -1
        else:
            print("Error: current crane_mode is not a valid option")

        # check if crane is getting container from empty col
        if new_crane_mode == "get" and self.is_empty_col(col):
            # print("get empty", col)
            return None

        # check if crane is getting container from col of NAN
        if new_crane_mode == "get" and self.ship_state[0][col].name == "NAN":
            # print("get NAN", col)
            return None

        # check if crane is putting container to full col, including col of NAN
        if new_crane_mode == "put" and self.is_full_col(col):
            # print("put full", col)
            return None

        # check crane_loc is not being moved to same col
        if col == self.crane_loc:
            # print("same col", col)
            return None

        new_ship = copy.deepcopy(self)
        new_ship.crane_loc = col
        new_ship.crane_mode = new_crane_mode

        # perform move if new_crane_mode is put
        if new_crane_mode == "put":
            get_col = self.crane_loc
            new_ship.move_cntr(get_col, col)

        return new_ship
