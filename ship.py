from container import Container
from typing import List, Optional


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
        
    # def __init__(
    #     self,
    #     manifest: Optional[List[str] or List[Container]] = None,
    #     loads: Optional[list] = [],
    #     unloads: Optional[list] = [],
    #     cntr_names: Optional[List[List[str]]] = None,
    # ) -> None:
    #     self.ship_state = []
    #     self.goal_state = {}
    #     self.row = 8
    #     self.col = 12
    #     if manifest != None and cntr_names == None:
    #         self.__init_ship_state_manifest(manifest)
    #     elif manifest == None and cntr_names != None:
    #         self.__init_ship_state_names(cntr_names)
    #     self.__init_goal_state(loads, unloads)

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

    """Gets list of all containers of all or a single column"""
    def get_ship_columns(self, indx: int = -1):
        rowlength = len(self.ship_state[0])
        columns = [[] for i in range(0, rowlength if indx == -1 else 1)]

        for row in self.ship_state:
            if indx == -1:
                for i in range(0, rowlength):
                    columns[i].append(row[i])
            else:
                columns[0].append(row[indx])

        return columns

