if __name__ == "__main__":
    from snake import Game, PygameUi

    Game(ui=PygameUi(20), size=20).run()
