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
                 iterations=None,
                 size=20,
                 snake=DEFAULT_SNAKE,
                 initial_direction=Direction.RIGHT
                 ):
        self._size = size
        self._snake = [x for x in snake]
        self._iterations = iterations
        self._ui = ui
        self._direction = initial_direction
        self._lost = False

    def run(self):
        while not self._lost:
            self._ui.draw([position for position in self._snake])

            try:
                self._move_snake(self._ui.direction())
            except Game.GameOverError:
                self._lost = True

            if self._iterations:
                self._iterations -= 1

            if self._iterations == 0:
                break

        return not self._lost

    def _move_snake(self, direction=None):
        head = self._snake[0]
        self._snake.pop()
        if Direction.should_update(self._direction, direction):
            self._direction = direction

        new_head = ((head[0] + self._direction[0]) % self._size,
                    (head[1] + self._direction[1]) % self._size)

        if new_head in self._snake:
            raise Game.GameOverError()

        self._snake.insert(0, new_head)

    class GameOverError(Exception):
        pass
