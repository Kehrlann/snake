if __name__ == "__main__":
    from snake import Game
    from ui import Ui

    Game(ui=Ui(20), size=20).run()


import sys
import pygame
import random
from pygame.locals import *
from itertools import product

# on doit "initialiser" PyGame
pygame.init()

# et définir la taille de la fenêtre (400x400)
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

SLOW_DOWN = 10
CELL_SIZE = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
snake = [
    (1, 1),
    (2, 1),
    (2, 2),
    (3, 2),
    (4, 2),
    (5, 2)
]
egg = (10, 10)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def draw_snake():
    for position in snake:
        draw_cell(position, WHITE)


def draw_egg():
    draw_cell(egg, YELLOW)


def draw_cell(position, color):
    x = position[0] * CELL_SIZE
    y = position[1] * CELL_SIZE
    pygame.draw.rect(screen, color, pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))


def move_snake(direction):
    dx, dy = direction
    head_x, head_y = snake[0]
    new_position = ((head_x + dx) % 20, (head_y + dy) % 20)
    # We must mutate the existing array, reassignment is very local
    snake.insert(0, new_position)
    if egg != new_position:
        snake.pop()  # do not remove the tail if you eat the egg
        return False
    else:
        return True


def place_egg():
    return random.randint(0, 19), random.randint(0, 19)


def end_of_game():
    head = snake[0]
    for position in snake[1:]:
        if head == position:
            return True
    return False


direction = DOWN
egg = place_egg()
while True:
    clock.tick(60 / SLOW_DOWN)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_q:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif event.key == K_UP and direction != DOWN:
                direction = UP
            elif event.key == K_DOWN and direction != UP:
                direction = DOWN
            elif event.key == K_LEFT and direction != RIGHT:
                direction = LEFT
            elif event.key == K_RIGHT and direction != LEFT:
                direction = RIGHT

    screen.fill(BLACK)
    draw_snake()
    draw_egg()
    if move_snake(direction):
        egg = place_egg()
    if end_of_game():
        pygame.display.quit()
        pygame.quit()
        sys.exit()
    pygame.display.update()
