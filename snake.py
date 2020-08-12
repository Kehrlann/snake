class Direction:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Game:
    DEFAULT_SNAKE = [(7, 5), (6, 5), (5, 5)]

    def __init__(self,
                 *args,
                 ui=None,
                 iterations=20,
                 size=20,
                 snake=DEFAULT_SNAKE
                 ):
        self._size = size
        self._snake = [x for x in snake]
        self.iterations = iterations
        self._ui = ui
        self._direction = Direction.RIGHT

    def run(self):
        for _ in range(self.iterations, 0, -1):
            self._ui.draw_snake([position for position in self._snake])
            self._move_snake(self._ui.direction())

    def _move_snake(self, direction=None):
        head = self._snake[0]
        self._snake.pop()
        if direction is not None:
            self._direction = direction

        new_head = ((head[0] + self._direction[0]) % self._size,
                    (head[1] + self._direction[1]) % self._size)
        self._snake.insert(0, new_head)
