class Direction:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @staticmethod
    def should_update(old_direction, new_direction):
        return new_direction is not None \
            and not (new_direction == Direction.UP and old_direction == Direction.DOWN) \
            and not (new_direction == Direction.DOWN and old_direction == Direction.UP) \
            and not (new_direction == Direction.RIGHT and old_direction == Direction.LEFT) \
            and not (new_direction == Direction.LEFT and old_direction == Direction.RIGHT)


class Game:
    DEFAULT_SNAKE = [(7, 5), (6, 5), (5, 5)]

    def __init__(self,
                 *args,
                 ui=None,
                 iterations=20,
                 size=20,
                 snake=DEFAULT_SNAKE,
                 initial_direction=Direction.RIGHT
                 ):
        self._size = size
        self._snake = [x for x in snake]
        self.iterations = iterations
        self._ui = ui
        self._direction = initial_direction

    def run(self):
        while True:
            self._ui.draw_snake([position for position in self._snake])
            self._move_snake(self._ui.direction())

            if self.iterations:
                self.iterations -= 1

            if self.iterations == 0:
                break

    def _move_snake(self, direction=None):
        head = self._snake[0]
        self._snake.pop()
        if Direction.should_update(self._direction, direction):
            self._direction = direction

        new_head = ((head[0] + self._direction[0]) % self._size,
                    (head[1] + self._direction[1]) % self._size)
        self._snake.insert(0, new_head)
