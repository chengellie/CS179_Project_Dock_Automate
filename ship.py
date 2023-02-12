from container import Container


class Ship:
    def __init__(self, manifest):
        self.ship_state = []
        self.row = 8
        self.col = 12
        self.__init_ship(manifest)
        print(self)

    def __init_ship(self, manifest):
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

    def __str__(self) -> str:
        ret = ""
        for row in self.ship_state:
            for cntr in row:
                shortened = cntr.name[:6].ljust(6)
                ret += shortened + " "
            ret += "\n"
        return ret
