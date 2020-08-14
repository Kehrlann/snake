from snake.game import Snake, Direction, Board
import pytest


class TestSnake():

    board = Board(4, 4)

    def test_create_default_positions(self):
        snake = Snake(self.board)
        assert snake.positions == [(1, 0), (0, 0)]
        assert snake.direction == Direction.RIGHT

    def test_create_given_positions(self):
        snake = Snake(self.board, positions=[(0, 0), (1, 0)])
        assert snake.positions == [(0, 0), (1, 0)]

    def test_create_must_have_two_or_more_positions(self):
        with pytest.raises(Exception) as e:
            snake = Snake(self.board, positions=[])
        assert str(e.value) == "snake should have a length of at least 2"

        with pytest.raises(Exception) as e:
            snake = Snake(self.board, positions=[(0, 0)])
        assert str(e.value) == "snake should have a length of at least 2"

    def test_compute_direction(self):
        # TODO: test through the public API ; direction should not be part of the public api
        assert Snake(self.board, positions=[(1, 0), (0, 0)]).direction \
            == Direction.RIGHT
        assert Snake(self.board, positions=[(0, 0), (1, 0)]).direction \
            == Direction.LEFT
        assert Snake(self.board, positions=[(0, 0), (0, 1)]).direction \
            == Direction.UP
        assert Snake(self.board, positions=[(0, 1), (0, 0)]).direction \
            == Direction.DOWN

        assert Snake(self.board, positions=[(3, 0), (0, 0)]).direction \
            == Direction.LEFT
        assert Snake(self.board, positions=[(0, 0), (3, 0)]).direction \
            == Direction.RIGHT
        assert Snake(self.board, positions=[(0, 3), (0, 0)]).direction \
            == Direction.UP
        assert Snake(self.board, positions=[(0, 0), (0, 3)]).direction \
            == Direction.DOWN

    def test_move_right(self):
        snake = Snake(self.board, positions=[(1, 0), (0, 0)])
        snake.move(False)
        assert snake.positions == [(2, 0), (1, 0)]

    def test_move_left(self):
        snake = Snake(self.board, positions=[(1, 0), (2, 0)])
        snake.move()
        assert snake.positions == [(0, 0), (1, 0)]

    def test_move_up(self):
        snake = Snake(self.board, positions=[(0, 1), (0, 2)])
        snake.move()
        assert snake.positions == [(0, 0), (0, 1)]

    def test_move_down(self):
        snake = Snake(self.board, positions=[(0, 1), (0, 0)])
        snake.move()
        assert snake.positions == [(0, 2), (0, 1)]

    def test_move_keep_tail(self):
        snake = Snake(self.board, positions=[(1, 0), (0, 0)])
        snake.move(True)
        assert snake.positions == [(2, 0), (1, 0), (0, 0)]

    def test_bite_itself(self):
        snake = Snake(self.board, positions=[
                      (0, 1), (0, 0), (1, 0), (1, 1), (1, 2)])
        snake.direction = Direction.RIGHT
        with pytest.raises(Snake.BitesItselfError):
            snake.move()

    def test_fills_board(self):
        board = Board(2, 3)
        small_snake = Snake(board, positions=[(0, 0), (1, 0)])
        big_snake = Snake(board, positions=[
            (0, 2), (0, 1), (0, 0), (1, 0), (1, 1), (1, 2)])
        assert small_snake.fills_board() is False
        assert big_snake.fills_board() is True

    def test_will_eat_egg(self):
        snake = Snake(self.board, positions=[(1, 0), (0, 0)])
        assert snake.will_eat_egg((2, 0)) is True
        assert snake.will_eat_egg((1, 1)) is False

    def test_iter(self):
        snake = Snake(self.board, positions=[(0, 1), (0, 0)])
        assert [pos for pos in snake] == [(0, 1), (0, 0)]

    def test_length(self):
        snake = Snake(self.board, positions=[(0, 1), (0, 0)])
        assert len(snake) == 2


class TestLoopOver():
    board = Board(width=4, height=6)

    def test_left(self):
        snake = Snake(self.board, positions=[(0, 0), (1, 0)])
        snake.move()
        assert snake.positions == [(3, 0), (0, 0)]

    def test_right(self):
        snake = Snake(self.board, positions=[(3, 0), (2, 0)])
        snake.move()
        assert snake.positions == [(0, 0), (3, 0)]

    def test_up(self):
        snake = Snake(self.board, positions=[(0, 0), (0, 1)])
        snake.move()
        assert snake.positions == [(0, 5), (0, 0)]

    def test_down(self):
        snake = Snake(self.board, positions=[(0, 0), (0, 1)])
        snake.move()
        assert snake.positions == [(0, 5), (0, 0)]


class TestChangeDirection():
    board = Board(width=4, height=6)

    def test_left(self):
        snake = Snake(self.board, positions=[(0, 0), (1, 0)])
        snake.direction = Direction.RIGHT
        snake.move()
        assert snake.positions == [(3, 0), (0, 0)]

    def test_right(self):
        snake = Snake(self.board, positions=[(3, 0), (2, 0)])
        snake.direction = Direction.LEFT
        snake.move()
        assert snake.positions == [(0, 0), (3, 0)]

    def test_up(self):
        snake = Snake(self.board, positions=[(0, 0), (0, 1)])
        snake.direction = Direction.DOWN
        snake.move()
        assert snake.positions == [(0, 5), (0, 0)]

    def test_down(self):
        snake = Snake(self.board, positions=[(0, 0), (0, 1)])
        snake.direction = Direction.UP
        snake.move()
        assert snake.positions == [(0, 5), (0, 0)]

    def test_no_change(self):
        snake = Snake(self.board, positions=[(0, 0), (1, 0)])
        snake.direction = None
        snake.move()
        assert snake.positions == [(3, 0), (0, 0)]
