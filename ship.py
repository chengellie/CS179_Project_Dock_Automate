from container import Container


class Ship:
    def __init__(self, manifest: str, loads=[], unloads=[]) -> None:
        self.ship_state = []
        self.curr_state = {}
        self.goal_state = {}
        self.row = 8
        self.col = 12
        self.__init_ship_state(manifest)
        self.__init_goal_state(loads, unloads)

    def __init_ship_state(self, manifest: str) -> None:
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

    def __init_goal_state(self, loads, unloads) -> None:
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
                return

    def is_goal_state(self) -> bool:
        """Inputs None, Returns if current ship_state matches goal_state."""
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
        """Inputs None, prints ship names in grid format. Returns None."""
        ret = ""
        for row in self.ship_state:
            for cntr in row:
                ret += cntr.get_shortened_name() + " "
            ret += "\n"
        return ret

    def print_weights(self) -> None:
        """Inputs None, prints ship weights in grid format. Returns None."""
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
        for i, row in enumerate(self.ship_state):
            for j, cntr in enumerate(row):
                if j >= 0 and j <= self.row / 2:
                    left += cntr.weight
                else:
                    right += cntr.weight

        print(left, right)

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
                ret += self.ship_state[i][j].format_container()
                if not (i == 0 and j == self.col - 1):
                    ret += "\n"

        return ret

    def get_ship_indices(self, cntr: Container):
        """Inputs container. Returns contaier's position converted to ship indices as a list."""
        return [self.row - cntr.x, cntr.y - 1]

    def update_cntr_pos(self, cntr: Container, i: int, j: int) -> None:
        """Inputs container's new indices in ship, updates position for container object. Returns None."""
        cntr.set_pos(i + 1, self.row - j)

    def get_container_depth(self, cntr: Container) -> int:
        """Inputs container. Returns number of containers above current container."""
        i, j = self.get_ship_indices(cntr)
        count = 0
        while i >= 0 and self.ship_state[i - 1][j] != "UNUSED":
            count += 1
            i -= 1
        return count
