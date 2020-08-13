# snake

Snake game &amp; TDD

## V1, thoughts

- Tests are all testing against the UI, which is probably overkill
  - However that's a strong regression suite
- Especially the loop-over / cannot go back
  - Cannot go back could have been tested on the Direction class itself
- Didn't really know where to start, so started with "draws a snake"
  - Which set me in the mindset of doing everything from the UI
  - Should probably have started with "there is a snake, it can move, it can eat an egg, etc"
- Very nice UI abstraction without knowing too much how the underlying graphical library works
  - Plugged in pygame, almost nothing to change and it Just Worked™
- IoC was nice: the Game knows about an abstraction of the UI; and therefore the game loop is implemented in the Game itself, without any UI stuff

**Possible TODOs:**

- [ ] Extract Snake class
- [ ] Try swapping in a TermUI interface
- [ ] Apply "nullable infrastructure" patterns and test without mocks (not sure it makes a lot of sense here, we'll see)
- [ ] Refactor: make the game not square
