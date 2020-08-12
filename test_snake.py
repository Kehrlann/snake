import signal
from snake import Game, Direction
from unittest.mock import Mock, call, DEFAULT


class TestSnake():
    def setup_method(self):
        self.ui = Mock()
        self.ui.direction = mock_direction()
        self.default_params = {
            "snake": [(7, 5), (6, 5), (5, 5)], "size": 20, "ui": self.ui
        }

    def test_snake_moves_right(self):
        game = Game(iterations=2, **self.default_params)
        game.run()
        assert self.ui.draw_snake.call_args_list == [
            call([(7, 5), (6, 5), (5, 5)]),
            call([(8, 5), (7, 5), (6, 5)])
        ]

    def test_snake_changes_direction(self):
        self.ui.direction = mock_direction(
            [Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT]
        )
        game = Game(iterations=5, **self.default_params)
        game.run()
        assert self.ui.draw_snake.call_args_list == [
            call([(7, 5), (6, 5), (5, 5)]),
            call([(7, 4), (7, 5), (6, 5)]),
            call([(6, 4), (7, 4), (7, 5)]),
            call([(6, 5), (6, 4), (7, 4)]),
            call([(7, 5), (6, 5), (6, 4)])
        ]

    def test_snake_keeps_direction(self):
        self.ui.direction = mock_direction(Direction.UP)
        game = Game(iterations=3, **self.default_params)
        game.run()
        assert self.ui.draw_snake.call_args_list == [
            call([(7, 5), (6, 5), (5, 5)]),
            call([(7, 4), (7, 5), (6, 5)]),
            call([(7, 3), (7, 4), (7, 5)])
        ]

    def test_infinite_iterations(self):
        try:
            with Timeout(seconds=2):
                Game(iterations=None, **self.default_params).run()
        except TimeoutError:
            pass
        else:
            raise AssertionError('Expected the thing to timeout!')


class TestCannotGoBack:
    def setup_method(self):
        self.ui = Mock()
        self.ui.direction = mock_direction()

    def test_left(self):
        snake = [(1, 0), (0, 0)]
        self.ui.direction = mock_direction([Direction.RIGHT, Direction.LEFT])
        game = Game(iterations=3, snake=snake, size=4, ui=self.ui)
        game.run()
        assert self.ui.draw_snake.call_args_list == [
            call([(1, 0), (0, 0)]),
            call([(2, 0), (1, 0)]),
            call([(3, 0), (2, 0)])
        ]

    def test_right(self):
        snake = [(2, 0), (3, 0)]
        self.ui.direction = mock_direction([Direction.LEFT, Direction.RIGHT])
        game = Game(iterations=3, snake=snake, size=4,
                    ui=self.ui, initial_direction=Direction.LEFT)
        game.run()
        assert self.ui.draw_snake.call_args_list == [
            call([(2, 0), (3, 0)]),
            call([(1, 0), (2, 0)]),
            call([(0, 0), (1, 0)])
        ]

    def test_down(self):
        snake = [(0, 2), (0, 3)]
        self.ui.direction = mock_direction([Direction.UP, Direction.DOWN])
        game = Game(iterations=3, snake=snake, size=4, ui=self.ui)
        game.run()
        assert self.ui.draw_snake.call_args_list == [
            call([(0, 2), (0, 3)]),
            call([(0, 1), (0, 2)]),
            call([(0, 0), (0, 1)])
        ]

    def test_up(self):
        snake = [(0, 1), (0, 0)]
        self.ui.direction = mock_direction([Direction.DOWN, Direction.UP])
        game = Game(iterations=3, snake=snake, size=4, ui=self.ui)
        game.run()
        assert self.ui.draw_snake.call_args_list == [
            call([(0, 1), (0, 0)]),
            call([(0, 2), (0, 1)]),
            call([(0, 3), (0, 2)])
        ]


class TestLoopOver:
    def setup_method(self):
        self.ui = Mock()
        self.ui.direction = Mock(return_value=None)
        self.default_params = {"iterations": 2, "size": 4, "ui": self.ui}

    def test_right(self):
        snake = [(3, 0), (0, 0)]
        self.ui.direction = mock_direction(Direction.RIGHT)
        game = Game(snake=snake, **self.default_params)
        game.run()
        self.ui.draw_snake.assert_any_call([(0, 0), (3, 0)])

    def test_left(self):
        snake = [(0, 0), (1, 0)]
        self.ui.direction = mock_direction(Direction.LEFT)
        game = Game(snake=snake, initial_direction=Direction.LEFT,
                    **self.default_params)
        game.run()
        self.ui.draw_snake.assert_any_call([(3, 0), (0, 0)])

    def test_up(self):
        snake = [(0, 0), (0, 1)]
        self.ui.direction = mock_direction(Direction.UP)
        game = Game(snake=snake, **self.default_params)
        game.run()
        self.ui.draw_snake.assert_any_call([(0, 3), (0, 0)])

    def test_down(self):
        snake = [(0, 3), (0, 0)]
        self.ui.direction = mock_direction(Direction.DOWN)
        game = Game(snake=snake, **self.default_params)
        game.run()
        self.ui.draw_snake.assert_any_call([(0, 0), (0, 3)])


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
