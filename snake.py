class Direction:
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


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

        if self._direction == Direction.UP:
            self._snake.insert(0, (head[0], (head[1] - 1) % self._size))
        elif self._direction == Direction.DOWN:
            self._snake.insert(0, (head[0], (head[1] + 1) % self._size))
        elif self._direction == Direction.RIGHT:
            self._snake.insert(0, ((head[0] + 1) % self._size, head[1]))
        elif self._direction == Direction.LEFT:
            self._snake.insert(0, ((head[0] - 1) % self._size, head[1]))
