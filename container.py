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
