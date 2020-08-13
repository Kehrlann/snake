from random import randint


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


class RandomEggCreator():
    def __init__(self, size):
        self._size = size

    def create(self):
        return (randint(0, self._size - 1), randint(0, self._size - 1))


class Game:
    DEFAULT_SNAKE = [(7, 5), (6, 5), (5, 5)]

    def __init__(self,
                 *args,
                 ui=None,
                 iterations=None,
                 size=20,
                 egg_creator=None,
                 snake=DEFAULT_SNAKE,
                 initial_direction=Direction.RIGHT
                 ):
        self._size = size
        self._snake = [x for x in snake]
        self._iterations = iterations
        self._ui = ui
        self._direction = initial_direction
        self._lost = False
        if egg_creator:
            self._egg_creator = egg_creator
        else:
            self._egg_creator = RandomEggCreator(size)

    def run(self):
        self._place_egg()
        while not self._lost:
            self._ui.draw(
                snake=[position for position in self._snake],
                egg=self._egg
            )

            try:
                direction = self._ui.direction()
                egg_eaten = self._egg_eaten(direction)
                self._move_snake(direction, egg_eaten)
                if len(self._snake) == self._size * self._size:
                    self._lost = False
                    break

                if egg_eaten:
                    self._place_egg()
            except Game.GameOverError:
                self._lost = True

            if self._iterations:
                self._iterations -= 1

            if self._iterations == 0:
                break

        return not self._lost

    def _move_snake(self, direction, egg_eaten):
        new_head = self._compute_new_head(direction)

        if not egg_eaten:
            self._snake.pop()

        if new_head in self._snake:
            raise Game.GameOverError()

        self._snake.insert(0, new_head)

    def _egg_eaten(self, direction):
        return self._compute_new_head(direction) == self._egg

    def _compute_new_head(self, direction):
        head = self._snake[0]

        if Direction.should_update(self._direction, direction):
            self._direction = direction

        new_head = ((head[0] + self._direction[0]) % self._size,
                    (head[1] + self._direction[1]) % self._size)

        return new_head

    def _place_egg(self):
        while True:
            new_egg = self._egg_creator.create()
            if not new_egg in self._snake:
                self._egg = new_egg
                break

    class GameOverError(Exception):
        pass
