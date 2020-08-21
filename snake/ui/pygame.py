import random
import sys
from itertools import product
from typing import Iterable, Optional, Tuple, Type

import pygame  # type: ignore
from pygame import constants  # type: ignore

from ..direction import Direction
from ..types import Position
from .protocol import UiProtocol

CELL_SIZE = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
Color = Tuple[int, int, int]


class PygameUi(UiProtocol):
    def __init__(self, size: int):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (size * CELL_SIZE, size * CELL_SIZE))
        self.clock = pygame.time.Clock()
        self.screen.fill(BLACK)

    def draw_cell(self, position: Position, color: Color) -> None:
        x = position[0] * CELL_SIZE
        y = position[1] * CELL_SIZE
        pygame.draw.rect(self.screen, color, pygame.Rect(
            x, y, CELL_SIZE, CELL_SIZE))

    def direction(self) -> Direction:
        for event in pygame.event.get():
            if event.type == constants.KEYDOWN:
                if event.key == constants.K_q:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                elif event.key == constants.K_UP:
                    return Direction.UP
                elif event.key == constants.K_DOWN:
                    return Direction.DOWN
                elif event.key == constants.K_LEFT:
                    return Direction.LEFT
                elif event.key == constants.K_RIGHT:
                    return Direction.RIGHT
        return Direction.DEFAULT

    def draw(self, snake: Iterable[Position], egg: Position) -> None:
        self.screen.fill(BLACK)

        for position in snake:
            self.draw_cell(position, WHITE)
        self.draw_cell(egg, YELLOW)

        pygame.display.update()
        self.clock.tick(5)
