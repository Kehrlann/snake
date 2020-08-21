from enum import Enum

# In a specific package because this is the glue between
# UI and Game, and needs a specific package for avoiding
# cyclic dependencies.


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    DEFAULT = 5

    @property
    def x(self) -> int:
        if self is self.RIGHT:
            return 1
        elif self is self.LEFT:
            return -1
        else:
            return 0

    @property
    def y(self) -> int:
        if self is self.DOWN:
            return 1
        elif self is self.UP:
            return -1
        else:
            return 0

    @staticmethod
    def from_delta(x: int, y: int) -> 'Direction':
        if x == 0 and y == 1:
            return Direction.DOWN
        elif x == 0 and y == -1:
            return Direction.UP
        elif x == 1 and y == 0:
            return Direction.RIGHT
        elif x == -1 and y == 0:
            return Direction.LEFT
        else:
            raise ValueError(
                "Invalid delta for direction, x and y should be integers in [-1, 0, 1]")
