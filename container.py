class Container:
    def __init__(self, pos: str, weight: int, name: str) -> None:
        self.x = int(pos[1:3])
        self.y = int(pos[4:6])
        self.weight = weight
        self.name = name

    def get_pos(self) -> str:
        """Inputs None. Returns position in format [xx,yy]."""
        return "[" + str(self.x).rjust(2, "0") + "," + str(self.y).rjust(2, "0") + "]"

    def __str__(self) -> str:
        """Inputs None. Returns representation of container object as a string."""
        return (
            f"Container {self.get_pos()}, Weight: {self.weight} kg, Name: {self.name}"
        )

    def get_shortened_name(self) -> str:
        """Inputs None. Returns shortened version of container name."""
        return str(self.name)[:6].ljust(6)

    def get_str_weight(self) -> str:
        """Inputs None. Returns weight as a 5-character string."""
        return str(self.weight).rjust(5, "0")

    def format_container(self) -> str:
        """Inputs None. Returns formatted container for outbound manifest."""
        return self.get_pos() + ", {" + self.get_str_weight() + "}, " + self.name

    def set_pos(self, new_x: int, new_y: int) -> None:
        """Inputs new positions, updates x and y. Returns None."""
        self.x = new_x
        self.y = new_y
