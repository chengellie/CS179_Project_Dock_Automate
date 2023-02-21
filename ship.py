from container import Container


class Ship:
    def __init__(self, manifest, loads, unloads):
        self.ship_state = []
        self.curr_state = {}
        self.goal_state = {}
        self.row = 8
        self.col = 12
        self.__init_ship_state(manifest)
        self.__init_goal_state(loads, unloads)
        print(self)

    def __init_ship_state(self, manifest):
        """Input list of strings from manifest, constructs container objects and fills ship object with containers. Returns None."""
        self.ship_state = [[None for j in range(self.col)] for i in range(self.row)]

        # extract container details from manifest list
        containers = []
        for item in manifest:
            c = Container(item[0:7], int(item[10:15]), item[18:].strip())
            containers.append(c)

        # fill in 2d list for ship_state, constructing container order in grid view
        k = 0
        for i in range(self.row - 1, -1, -1):
            for j in range(self.col):
                self.ship_state[i][j] = containers[k]
                k += 1

    def __init_goal_state(self, loads, unloads):
        """Inputs None, constructs map and fills dictionary with number of each type of container for starting state of ship,
        constructs dictionary with goal state of number of each type of container. Returns None.
        """
        for row in self.ship_state:
            for cntr_obj in row:
                cntr_name = cntr_obj.name
                if cntr_name == "UNUSED" or cntr_name == "NAN":
                    continue
                if cntr_name in self.goal_state.keys():
                    self.goal_state[cntr_name] += 1
                else:
                    self.goal_state[cntr_name] = 1

        # Construct goal state by simulating ship state after all actions completed
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

    def check_goal_state(self) -> bool:
        """Inputs None, Returns if current ship_state matches goal_state"""
        for row in self.ship_state:
            for cntr_obj in row:
                cntr_name = cntr_obj.name
                if cntr_name == "UNUSED" or cntr_name == "NAN":
                    continue
                if cntr_name in self.curr_state.keys():
                    self.curr_state[cntr_name] += 1
                else:
                    self.curr_state[cntr_name] = 1
        return self.curr_state == self.goal_state

    def __str__(self) -> str:
        ret = ""
        for row in self.ship_state:
            for cntr in row:
                shortened = cntr.name[:6].ljust(6)
                ret += shortened + " "
            ret += "\n"
        return ret
