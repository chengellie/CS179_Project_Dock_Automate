from typing import List


class Container:
    def __init__(
        self, manifest_coord: List[int], weight: int, name: str, ship_size: List[int]
    ) -> None:
        self.manifest_coord = manifest_coord
        self.ship_coord = [ship_size[0] - manifest_coord[0], manifest_coord[1] - 1]
        self.ship_size = ship_size
        self.weight = weight
        self.name = name
        self.selected = False

    def __str__(self) -> str:
        """Inputs None. Returns 6-character shortened version of container name."""
        return self.get_shortened_name()

    def get_manifest_format(self) -> str:
        """Inputs None. Returns formatted container for outbound manifest."""
        str_manifest_coord = (
            "["
            + str(self.manifest_coord[0]).rjust(2, "0")
            + ","
            + str(self.manifest_coord[1]).rjust(2, "0")
            + "]"
        )
        str_weight = "{" + str(self.weight).rjust(5, "0") + "}"
        return str_manifest_coord + ", " + str_weight + ", " + self.name

    def get_shortened_name(self) -> str:
        """Inputs None. Returns 6-character shortened version of container name.
        If name is shorter than 6-characters, appends spaces to fill in string up to 6 characters.
        """
        return str(self.name)[:6].ljust(6, " ")

    def set_manifest_coord(self, new_manifest_coord: List[int]) -> None:
        """Inputs manifest version of new coordinates, updates both manifest and ship coordinates. Returns None."""
        self.manifest_coord = new_manifest_coord
        self.ship_coord = [
            self.ship_size[0] - new_manifest_coord[0],
            new_manifest_coord[1] - 1,
        ]

    def set_ship_coord(self, new_ship_coord: List[int]) -> None:
        """Inputs ship version of new coordinates, updates both manifest and ship coordinates. Returns None."""
        self.ship_coord = new_ship_coord
        self.manifest_coord = [
            self.ship_size[0] - new_ship_coord[0],
            new_ship_coord[1] + 1,
        ]
