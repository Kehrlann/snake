import pytest
import signal
from snake.types import Position
from snake.game import Game, RandomEggCreator, EggCreator
from snake.direction import Direction
from unittest.mock import Mock, call, DEFAULT
from snake.ui.protocol import UiProtocol
from typing import Callable, Any, List, Union, Generator


class BaseTestCase:
    ui: Any
    egg_creator: Any

    def get_drawn_snakes(self) -> List[List[Position]]:
        call_args = [call.kwargs for call in self.ui.draw.call_args_list]
        return [args["snake"] for args in call_args]


class TestGame(BaseTestCase):
    snake: List[Position] = [(7, 5), (6, 5), (5, 5)]
    size: int = 20

    def setup_method(self) -> None:
        self.ui = Mock()
        self.ui.direction = mock_direction()
        self.egg_creator = Mock()
        self.egg_creator.create.return_value = (0, 0)

    def test_snake_moves_right(self) -> None:
        game = Game(iterations=2,
                    snake=self.snake,
                    size=self.size,
                    ui=self.ui,
                    egg_creator=self.egg_creator)
        game.run()
        assert self.get_drawn_snakes() == [
            [(7, 5), (6, 5), (5, 5)],
            [(8, 5), (7, 5), (6, 5)]
        ]

    def test_snake_size_zero_fails(self) -> None:
        with pytest.raises(Exception):
            # don't really care how it fails ...
            game = Game(iterations=2, snake=[], size=20,
                        ui=self.ui, egg_creator=self.egg_creator)
            game.run()

    def test_snake_changes_direction(self) -> None:
        self.ui.direction = mock_direction(
            [Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT]
        )
        game = Game(iterations=5, snake=self.snake,
                    size=self.size,
                    ui=self.ui,
                    egg_creator=self.egg_creator)
        game.run()
        assert self.get_drawn_snakes() == [
            [(7, 5), (6, 5), (5, 5)],
            [(7, 4), (7, 5), (6, 5)],
            [(6, 4), (7, 4), (7, 5)],
            [(6, 5), (6, 4), (7, 4)],
            [(7, 5), (6, 5), (6, 4)]
        ]

    def test_snake_keeps_direction(self) -> None:
        self.ui.direction = mock_direction(Direction.UP)
        game = Game(iterations=3, snake=self.snake,
                    size=self.size,
                    ui=self.ui,
                    egg_creator=self.egg_creator)
        game.run()
        assert self.get_drawn_snakes() == [
            [(7, 5), (6, 5), (5, 5)],
            [(7, 4), (7, 5), (6, 5)],
            [(7, 3), (7, 4), (7, 5)]
        ]

    def test_cannot_go_back(self) -> None:
        self.ui.direction = mock_direction([Direction.RIGHT, Direction.LEFT])
        self.egg_creator.create.return_value = (3, 3)
        game = Game(
            snake=[(1, 0), (0, 0)],
            iterations=3,
            size=4,
            ui=self.ui,
            egg_creator=self.egg_creator
        )
        game.run()
        assert self.get_drawn_snakes() == [
            [(1, 0), (0, 0)],
            [(2, 0), (1, 0)],
            [(3, 0), (2, 0)]
        ]

    def test_loop_over(self) -> None:
        snake = [(3, 0), (2, 0)]
        self.egg_creator.create.return_value = [3, 3]
        self.ui.direction = mock_direction(Direction.RIGHT)
        game = Game(
            snake=[(3, 0), (2, 0)],
            iterations=2,
            size=4,
            ui=self.ui,
            egg_creator=self.egg_creator
        )
        game.run()
        assert [(0, 0), (3, 0)] in self.get_drawn_snakes()

    def test_infinite_iterations(self) -> None:
        try:
            with Timeout():
                Game(iterations=None, snake=self.snake,
                     size=self.size,
                     ui=self.ui,
                     egg_creator=self.egg_creator).run()
        except TimeoutError:
            pass
        else:
            raise AssertionError('Expected the thing to timeout!')

    def test_snake_eats_itself(self) -> None:
        self.ui.direction = mock_direction(Direction.RIGHT)
        game = Game(size=20, ui=self.ui, snake=[
                    (0, 1), (0, 0), (1, 0), (1, 1), (1, 2)])
        with Timeout():
            assert game.run() is False


class TestEggInteraction(BaseTestCase):
    def get_drawn_eggs(self) -> List[Position]:
        call_args = [call.kwargs for call in self.ui.draw.call_args_list]
        return [args["egg"] for args in call_args]

    def setup_method(self) -> None:
        self.ui = Mock()
        self.ui.direction = mock_direction()
        self.default_params = {
            "snake": [(1, 0), (0, 0)], "size": 20, "ui": self.ui
        }

    def test_place_egg(self) -> None:
        egg_creator = Mock()
        egg_creator.create.side_effect = [(10, 10), (15, 15)]
        game = Game(iterations=2, egg_creator=egg_creator,
                    ui=self.ui, snake=[(1, 0), (0, 0)])
        game.run()
        assert self.get_drawn_eggs() == [
            (10, 10),  # draw once
            (10, 10)  # it hasn't moved
        ]

    def test_eat_egg_place_new_egg(self) -> None:
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

    def test_eat_egg_snake_grows(self) -> None:
        egg_creator = Mock()
        egg_creator.create.side_effect = [(2, 0), (10, 10)]
        game = Game(iterations=2, egg_creator=egg_creator,
                    ui=self.ui, snake=[(1, 0), (0, 0)])
        game.run()
        assert self.get_drawn_snakes() == [
            [(1, 0), (0, 0)],
            [(2, 0), (1, 0), (0, 0)]
        ]

    def test_egg_cannot_be_placed_on_snake(self) -> None:
        egg_creator = Mock()
        egg_creator.create.side_effect = [(0, 0), (15, 15)]
        game = Game(iterations=1, egg_creator=egg_creator,
                    ui=self.ui, snake=[(1, 0), (0, 0)])
        game.run()
        assert self.get_drawn_eggs() == [
            (15, 15)
        ]

    def test_eat_last_egg(self) -> None:
        egg_creator = Mock()
        egg_creator.create.return_value = (1, 1)
        self.ui.direction = mock_direction(Direction.RIGHT)
        game = Game(egg_creator=egg_creator,
                    ui=self.ui,
                    snake=[(0, 1), (0, 0), (1, 0)],
                    size=2)

        with Timeout():
            result = game.run()
            assert result is True


class TestRandomEggCreator():
    def test_create_in_bounds(self) -> None:
        creator = RandomEggCreator(23)
        for _ in range(1000):
            egg = creator.create()
            assert egg[0] in list(range(23))
            assert egg[1] in list(range(23))

    def test_create_is_random(self) -> None:
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


def mock_direction(directions: Union[Direction, List[Direction]] = None) -> Callable[[], Direction]:
    if directions is None:
        return Mock(return_value=None)
    elif not isinstance(directions, list):
        directions = [directions]

    def func() -> Generator[Direction, None, None]:
        for direction in directions:  # type: ignore
            yield direction
        while True:
            yield DEFAULT

    generator = func()

    def effect(*args: Any, **kwargs: Any) -> Direction:
        return next(generator)

    return Mock(
        side_effect=effect,
        return_value=None
    )


class Timeout:
    def __init__(self, seconds: float = .1, error_message: str = 'Timeout'):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum: Any, frame: Any) -> None:
        raise TimeoutError(self.error_message)

    def __enter__(self) -> None:
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.setitimer(signal.ITIMER_REAL, self.seconds)

    def __exit__(self, type: Any, value: Any, traceback: Any) -> None:
        signal.alarm(0)
