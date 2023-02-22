class Container:
    def __init__(self, pos: str, weight: int, name: str) -> None:
        self.pos = pos
        self.weight = weight
        self.name = name

    def __str__(self) -> str:
        return f"Container {self.pos}, Weight: {self.weight} kg, Name: {self.name}"
