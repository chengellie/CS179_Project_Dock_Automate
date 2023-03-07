from container import Container
from typing import List, Optional

# modify or remove get columns, unneeded. instead have search and find depth go rowwise instead. (search algo will mark matching containers. list stores them in depth order (will shift accordingly)

class Ship:
    def __init__(self,  
        manifest:str or List[str] or List[Container],
        loads:List[str]=[], 
        unloads:List[str]=[]
    ) -> None:
        self.ship_state = []
        self.goal_state = {}
        self.row = 8
        self.col = 12
        self.cntrs_in_row = []
        if type(manifest) == str:   # read manifest from scratch
            with open(manifest) as f:
                containers = [line for line in f.readlines()]
            self.__init_ship_state_manifest(containers)
        else:   # list
            if not manifest:    # empty list
                raise Exception("Expected non-empty list of containers")
            elif isinstance(manifest[0], str):
                self.__init_ship_state_manifest(manifest)
            else:
                self.ship_state = manifest

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

        self.__init_goal_state(loads, unloads)

    def __init_ship_state_manifest(self, manifest: List[str]) -> None:
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

    def __init_ship_state_names(self, cntr_names: List[List[str]]) -> None:
        """Input 2d list of container names, constructs container objects and fills ship with containers. Returns None."""
        self.ship_state = [[None for j in range(self.col)] for i in range(self.row)]
        for i in range(self.row):
            for j in range(self.col):
                c = Container([-1, -1], -1, cntr_names[i][j], [self.row, self.col])
                self.ship_state[i][j] = c

    def __init_goal_state(self, loads: List[str], unloads: List[str]) -> None:
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
        """Inputs None, prints container weights in grid format. Returns None."""
        ret = ""
        for row in self.ship_state:
            for cntr in row:
                shortened = str(cntr.weight)[:6].ljust(6)
                ret += shortened + " "
            ret += "\n"
        print(ret)

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
        i, j = cntr.ship_coord[5, 1][1, 2]
        i -= 1  # start check at cell above current container
        count = 0
        while i >= 0 and self.ship_state[i][j] != "UNUSED":
            count += 1
            i -= 1
        return count

    """Takes in a Container and finds the container that is best to unload (given it was not marked)"""
    # TODO: Find a way to mark containers that are already considered
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