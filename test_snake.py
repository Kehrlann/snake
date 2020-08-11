from snake import Game, Direction
from unittest.mock import Mock, call


# class TestSnake:
#   def setup_method(self):
#     self._ui = Mock()
#     self._ui.direction = Mock(return_value=None)

#   def test_hi(self):
#     print("hello")
#     assert self.game is not None


class TestSnake():
    DEFAULT_PARAMS = {"snake": [(7, 5), (6, 5), (5, 5)], "size": 20}

    def setup_method(self):
        self.ui = Mock()
        self.ui.direction = Mock(return_value=None)

    def test_snake_moves_right(self):
        game = Game(iterations=2, ui=self.ui, **self.DEFAULT_PARAMS)
        game.run()
        assert self.ui.draw_snake.call_args_list == [
            call([(7, 5), (6, 5), (5, 5)]),
            call([(8, 5), (7, 5), (6, 5)])
        ]

    def test_snake_changes_direction(self):
        self.ui.direction = Mock(
            side_effect=[Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT, None])
        game = Game(iterations=5, ui=self.ui, **self.DEFAULT_PARAMS)
        game.run()
        assert self.ui.draw_snake.call_args_list == [
            call([(7, 5), (6, 5), (5, 5)]),
            call([(7, 4), (7, 5), (6, 5)]),
            call([(6, 4), (7, 4), (7, 5)]),
            call([(6, 5), (6, 4), (7, 4)]),
            call([(7, 5), (6, 5), (6, 4)])
        ]

    def test_snake_keeps_direction(self):
        self.ui.direction = Mock(side_effect=[Direction.UP, None, None])
        game = Game(iterations=3, ui=self.ui, **self.DEFAULT_PARAMS)
        game.run()
        assert self.ui.draw_snake.call_args_list == [
            call([(7, 5), (6, 5), (5, 5)]),
            call([(7, 4), (7, 5), (6, 5)]),
            call([(7, 3), (7, 4), (7, 5)])
        ]


class TestLoopOver:
    def test_snake_loops_over(self):
        ui = Mock()
        ui.direction = Mock(return_value=None)
        game = Game(iterations=14, ui=ui)
        game.run()
        ui.draw_snake.assert_any_call([(0, 5), (19, 5), (18, 5)])
