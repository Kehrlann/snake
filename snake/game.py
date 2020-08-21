from dataclasses import dataclass
from random import randint
from typing import Tuple, List, Optional, Protocol, Iterator
from enum import Enum
from .types import Position
from .direction import Direction
from .ui.protocol import UiProtocol


class EggCreator(Protocol):
    def create(self) -> Position:
        raise NotImplementedError()


class RandomEggCreator():
    def __init__(self, size: int):
        self._size = size

    def create(self) -> Position:
        return (randint(0, self._size - 1), randint(0, self._size - 1))


@dataclass(frozen=True)
class Board:
    width: int
    height: int

    @property
    def size(self) -> int:
        return self.width * self.height


class Snake:
    _positions: List[Position]
    _direction: Direction
    _board: Board

    def __init__(self, board: Board, positions: List[Position] = [(1, 0), (0, 0)]):
        if len(positions) < 2:
            raise Exception("snake should have a length of at least 2")
        self._positions = positions
        head = positions[0]
        previous_head = positions[1]
        # TODO: make a neat little function ?
        delta_x = head[0] - previous_head[0]
        delta_y = head[1] - previous_head[1]
        if delta_x == board.width - 1:
            delta_x = -1
        elif delta_x == 1 - board.width:
            delta_x = 1
        if delta_y == board.height - 1:
            delta_y = -1
        elif delta_y == 1 - board.height:
            delta_y = 1

        self._direction = Direction.from_delta(delta_x, delta_y)
        self._board = board

    @property
    def positions(self) -> List[Position]:
        return self._positions

    @property
    def direction(self) -> Direction:
        return self._direction

    @direction.setter
    def direction(self, direction: Direction) -> None:
        if (direction is not None and direction is not Direction.DEFAULT
                and not (direction == Direction.UP and self._direction == Direction.DOWN)
                and not (direction == Direction.DOWN and self._direction == Direction.UP)
                and not (direction == Direction.RIGHT and self._direction == Direction.LEFT)
                and not (direction == Direction.LEFT and self._direction == Direction.RIGHT)):
            self._direction = direction

    def move(self, keep_tail: bool = False) -> None:
        if not keep_tail:
            self._positions.pop()

        new_head = self._compute_new_head()

        if new_head in self.positions:
            raise Snake.BitesItselfError()

        self._positions.insert(0, new_head)

    def will_eat_egg(self, egg: Position) -> bool:
        return egg == self._compute_new_head()

    def _compute_new_head(self) -> Position:
        head = self._positions[0]
        return ((head[0] + self._direction.x) % self._board.width,
                (head[1] + self._direction.y) % self._board.height)

    def fills_board(self) -> bool:
        return len(self._positions) == self._board.size

    def __iter__(self) -> Iterator[Position]:
        return iter(self.positions)

    class BitesItselfError(Exception):
        pass


class Game:
    DEFAULT_SNAKE = [(7, 5), (6, 5), (5, 5)]
    _snake: Snake
    _board: Board
    _iterations: Optional[int]
    _lost: bool
    _egg_creator: EggCreator
    _ui: UiProtocol

    def __init__(self,
                 ui: UiProtocol,
                 iterations: Optional[int] = None,
                 size: int = 20,
                 egg_creator: EggCreator = None,
                 snake: List[Position] = DEFAULT_SNAKE):
        self._board = Board(size, size)
        self._snake = Snake(self._board, [x for x in snake])
        self._iterations = iterations
        self._ui = ui
        self._lost = False
        if egg_creator:
            self._egg_creator = egg_creator
        else:
            self._egg_creator = RandomEggCreator(size)

    def run(self) -> bool:
        self._place_egg()
        while not self._lost:
            self._ui.draw(
                snake=[position for position in self._snake],
                egg=self._egg
            )

            try:
                self._snake.direction = self._ui.direction()
                egg_eaten = self._snake.will_eat_egg(self._egg)
                self._snake.move(egg_eaten)
                if self._snake.fills_board():
                    self._lost = False
                    break

                if egg_eaten:
                    self._place_egg()
            except Snake.BitesItselfError:
                self._lost = True
                break

            if self._iterations:
                self._iterations -= 1

            if self._iterations == 0:
                break

        return not self._lost

    def _place_egg(self) -> None:
        while True:
            new_egg = self._egg_creator.create()
            if not new_egg in self._snake:
                self._egg = new_egg
                break

    class GameOverError(Exception):
        pass
