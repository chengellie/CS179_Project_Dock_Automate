class Container:
    def __init__(self, pos, weight, name):
        self.pos = pos
        self.weight = weight
        self.name = name

    def __str__(self) -> str:
        return f"Container {self.pos}, Weight: {self.weight} kg, Name: {self.name}"
