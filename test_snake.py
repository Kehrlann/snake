import pytest
import signal
from snake import Game, Direction, RandomEggCreator
from unittest.mock import Mock, call, DEFAULT


class BaseTestCase:
    ui = None

    def get_drawn_snakes(self):
        call_args = [call.kwargs for call in self.ui.draw.call_args_list]
        return [args["snake"] for args in call_args]


class TestGame(BaseTestCase):
    def setup_method(self):
        self.ui = Mock()
        self.ui.direction = mock_direction()
        self.default_params = {
            "snake": [(7, 5), (6, 5), (5, 5)], "size": 20, "ui": self.ui
        }

    def test_snake_moves_right(self):
        game = Game(iterations=2, **self.default_params)
        game.run()
        assert self.get_drawn_snakes() == [
            [(7, 5), (6, 5), (5, 5)],
            [(8, 5), (7, 5), (6, 5)]
        ]

    def test_snake_size_zero_fails(self):
        game = Game(iterations=1, snake=[], ui=self.ui, size=42)
        with pytest.raises(Exception):
            # don't really care how it fails ...
            game.run()

    def test_snake_changes_direction(self):
        self.ui.direction = mock_direction(
            [Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT]
        )
        game = Game(iterations=5, **self.default_params)
        game.run()
        assert self.get_drawn_snakes() == [
            [(7, 5), (6, 5), (5, 5)],
            [(7, 4), (7, 5), (6, 5)],
            [(6, 4), (7, 4), (7, 5)],
            [(6, 5), (6, 4), (7, 4)],
            [(7, 5), (6, 5), (6, 4)]
        ]

    def test_snake_keeps_direction(self):
        self.ui.direction = mock_direction(Direction.UP)
        game = Game(iterations=3, **self.default_params)
        game.run()
        assert self.get_drawn_snakes() == [
            [(7, 5), (6, 5), (5, 5)],
            [(7, 4), (7, 5), (6, 5)],
            [(7, 3), (7, 4), (7, 5)]
        ]

    def test_infinite_iterations(self):
        try:
            with Timeout():
                Game(iterations=None, **self.default_params).run()
        except TimeoutError:
            pass
        else:
            raise AssertionError('Expected the thing to timeout!')

    def test_snake_eats_itself(self):
        self.ui.direction = mock_direction(Direction.UP)
        game = Game(size=20, ui=self.ui, snake=[
                    (0, 1), (0, 0), (1, 0), (1, 1), (1, 2)])
        with Timeout():
            assert game.run() is False


class TestEggInteraction(BaseTestCase):
    def get_drawn_eggs(self):
        call_args = [call.kwargs for call in self.ui.draw.call_args_list]
        return [args["egg"] for args in call_args]

    def setup_method(self):
        self.ui = Mock()
        self.ui.direction = mock_direction()
        self.default_params = {
            "snake": [(1, 0), (0, 0)], "size": 20, "ui": self.ui
        }

    def test_place_egg(self):
        egg_creator = Mock()
        egg_creator.create.side_effect = [(10, 10), (15, 15)]
        game = Game(iterations=2, egg_creator=egg_creator,
                    ui=self.ui, snake=[(1, 0), (0, 0)])
        game.run()
        assert self.get_drawn_eggs() == [
            (10, 10),  # draw once
            (10, 10)  # it hasn't moved
        ]

    def test_eat_egg_place_new_egg(self):
        egg_creator = Mock()
        egg_creator.create.side_effect = [(2, 0), (10, 10)]
        game = Game(iterations=3, egg_creator=egg_creator,
                    ui=self.ui, snake=[(1, 0), (0, 0)])
        game.run()
        assert self.get_drawn_eggs() == [
            (2, 0),
            (10, 10),
            (10, 10)
        ]

    def test_eat_egg_snake_grows(self):
        egg_creator = Mock()
        egg_creator.create.side_effect = [(2, 0), (10, 10)]
        game = Game(iterations=2, egg_creator=egg_creator,
                    ui=self.ui, snake=[(1, 0), (0, 0)])
        game.run()
        assert self.get_drawn_snakes() == [
            [(1, 0), (0, 0)],
            [(2, 0), (1, 0), (0, 0)]
        ]

    def test_egg_cannot_be_placed_on_snake(self):
        egg_creator = Mock()
        egg_creator.create.side_effect = [(0, 0), (15, 15)]
        game = Game(iterations=1, egg_creator=egg_creator,
                    ui=self.ui, snake=[(1, 0), (0, 0)])
        game.run()
        assert self.get_drawn_eggs() == [
            (15, 15)
        ]

    def test_eat_last_egg(self):
        egg_creator = Mock()
        egg_creator.create.return_value = (1, 1)
        game = Game(iterations=1,
                    egg_creator=egg_creator,
                    ui=self.ui,
                    snake=[(0, 1), (0, 0), (1, 0)],
                    size=2)

        with Timeout():
            result = game.run()
            assert result is True


class TestCannotGoBack(BaseTestCase):
    def setup_method(self):
        self.ui = Mock()
        self.ui.direction = mock_direction()
        self.egg_creator = Mock()
        # no snake will eat this egg
        self.egg_creator.create.return_value = [
            3, 3]
        self.default_params = {
            "ui": self.ui,
            "egg_creator": self.egg_creator,
            "iterations": 3,
            "size": 4
        }

    def test_left(self):
        snake = [(1, 0), (0, 0)]
        self.ui.direction = mock_direction([Direction.RIGHT, Direction.LEFT])
        game = Game(snake=snake, **self.default_params)
        game.run()
        assert self.get_drawn_snakes() == [
            [(1, 0), (0, 0)],
            [(2, 0), (1, 0)],
            [(3, 0), (2, 0)]
        ]

    def test_right(self):
        snake = [(2, 0), (3, 0)]
        self.ui.direction = mock_direction([Direction.LEFT, Direction.RIGHT])
        game = Game(snake=snake, initial_direction=Direction.LEFT,
                    **self.default_params)
        game.run()
        assert self.get_drawn_snakes() == [
            [(2, 0), (3, 0)],
            [(1, 0), (2, 0)],
            [(0, 0), (1, 0)]
        ]

    def test_down(self):
        snake = [(0, 2), (0, 3)]
        self.ui.direction = mock_direction([Direction.UP, Direction.DOWN])
        game = Game(snake=snake, **self.default_params)
        game.run()
        assert self.get_drawn_snakes() == [
            [(0, 2), (0, 3)],
            [(0, 1), (0, 2)],
            [(0, 0), (0, 1)]
        ]

    def test_up(self):
        snake = [(0, 1), (0, 0)]
        self.ui.direction = mock_direction([Direction.DOWN, Direction.UP])
        game = Game(snake=snake, **self.default_params)
        game.run()
        assert self.get_drawn_snakes() == [
            [(0, 1), (0, 0)],
            [(0, 2), (0, 1)],
            [(0, 3), (0, 2)]
        ]


class TestLoopOver(BaseTestCase):
    def setup_method(self):
        self.ui = Mock()
        self.ui.direction = Mock(return_value=None)
        self.default_params = {"iterations": 2, "size": 4, "ui": self.ui}

    def test_right(self):
        snake = [(3, 0), (0, 0)]
        self.ui.direction = mock_direction(Direction.RIGHT)
        game = Game(snake=snake, **self.default_params)
        game.run()
        assert [(0, 0), (3, 0)] in self.get_drawn_snakes()

    def test_left(self):
        snake = [(0, 0), (1, 0)]
        self.ui.direction = mock_direction(Direction.LEFT)
        game = Game(snake=snake, initial_direction=Direction.LEFT,
                    **self.default_params)
        game.run()
        assert [(3, 0), (0, 0)] in self.get_drawn_snakes()

    def test_up(self):
        snake = [(0, 0), (0, 1)]
        self.ui.direction = mock_direction(Direction.UP)
        game = Game(snake=snake, **self.default_params)
        game.run()
        assert [(0, 3), (0, 0)] in self.get_drawn_snakes()

    def test_down(self):
        snake = [(0, 3), (0, 0)]
        self.ui.direction = mock_direction(Direction.DOWN)
        game = Game(snake=snake, **self.default_params)
        game.run()
        assert [(0, 0), (0, 3)] in self.get_drawn_snakes()


class TestRandomEggCreator():
    def test_create_in_bounds(self):
        creator = RandomEggCreator(23)
        for _ in range(1000):
            egg = creator.create()
            assert egg[0] in list(range(23))
            assert egg[1] in list(range(23))

    def test_create_is_random(self):
        expected_positions = [
            (0, 0),
            (1, 0),
            (0, 1),
            (1, 1)
        ]
        creator = RandomEggCreator(2)
        with Timeout():
            while len(expected_positions) > 0:
                egg = creator.create()
                if egg in expected_positions:
                    expected_positions.remove(egg)


def mock_direction(directions=None):
    if directions is None:
        return Mock(return_value=None)
    elif not isinstance(directions, list):
        directions = [directions]

    def func():
        for direction in directions:
            yield direction
        while True:
            yield DEFAULT

    generator = func()

    def effect(*args, **kwargs):
        return next(generator)

    return Mock(
        side_effect=effect,
        return_value=None
    )


class Timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)
