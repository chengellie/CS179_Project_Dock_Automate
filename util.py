from dataclasses import dataclass, field
from typing import Any

# https://stackoverflow.com/questions/66448588/is-there-a-way-to-make-a-priority-queue-sort-by-the-priority-value-in-a-tuple-on?noredirect=1&lq=1
@dataclass(order=True)
class PrioritizedShip:
    priority: int
    item: Any = field(compare=False)
