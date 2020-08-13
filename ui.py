import sys
from itertools import product
from snake import Direction
import random
import pygame
from pygame.locals import *

CELL_SIZE = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


class Ui:
    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (size * CELL_SIZE, size * CELL_SIZE))
        self.clock = pygame.time.Clock()
        self.screen.fill(BLACK)

    def draw_cell(self, position, color):
        x = position[0] * CELL_SIZE
        y = position[1] * CELL_SIZE
        pygame.draw.rect(self.screen, color, pygame.Rect(
            x, y, CELL_SIZE, CELL_SIZE))

    def direction(self):
        print("direction")
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_q:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                elif event.key == K_UP:
                    return Direction.UP
                elif event.key == K_DOWN:
                    return Direction.DOWN
                elif event.key == K_LEFT:
                    return Direction.LEFT
                elif event.key == K_RIGHT:
                    return Direction.RIGHT

    def draw(self, *args, snake, egg):
        print("draw")
        self.screen.fill(BLACK)

        for position in snake:
            self.draw_cell(position, WHITE)
        self.draw_cell(egg, YELLOW)

        pygame.display.update()
        self.clock.tick(5)
