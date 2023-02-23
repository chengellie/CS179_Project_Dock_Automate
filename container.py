class Container:
    def __init__(self, pos: str, weight: int, name: str) -> None:
        self.pos = pos
        self.weight = weight
        self.name = name

    def __str__(self) -> str:
        """Inputs None. Returns representation of container object as a string."""
        return f"Container {self.pos}, Weight: {self.weight} kg, Name: {self.name}"

    def get_shortened_name(self) -> str:
        """Inputs None. Returns shortened version of container name."""
        return str(self.name)[:6].ljust(6)

    def get_str_weight(self) -> str:
        """Inputs None. Returns weight as a 5-character string."""
        return str(self.weight).rjust(5, "0")

    def format_container(self) -> str:
        """Inputs None. Returns formatted container for outbound manifest."""
        return self.pos + ", {" + self.get_str_weight() + "}, " + self.name
