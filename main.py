if __name__ == "__main__":
    from snake import Game
    from snake.ui import Ui

    Game(ui=Ui(20), size=20).run()
