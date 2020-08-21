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
- mypy typings seemed painful...

**Possible TODOs:**

- [x] Extract Snake class
- [x] Retry my hand at typings
- [ ] Try swapping in a TermUI interface
- [ ] Apply "nullable infrastructure" patterns and test without mocks (not sure it makes a lot of sense here, we'll see)
- [ ] Refactor: make the game not square

## V2, thoughts

- Python typings are okay-ish
  - Not great integration in VSCode, I expected more warnings
  - Requires a lot of extra splitting in where you define types vs where you use them (there are cyclic dependency issues)
  - Doesn't play nice with properties when you want a T property that you could update with Optional[T] (None = no update, T = update) ; had to revert to a method (`snake.update_direction()`). Another trick was to introduce a new "DEFAULT" enum value.
  - Structural & nominal typing mix-and-match is weird, I probably have to get to the bottom of it
- Extracted Snake class is much nicer, handles everything about the snake: how it updates its direction, how it grows, what movement is allowed or not
  - There is a dependency on the Board to know how to loop over. I'm not sure I like it, but this is required to know what is a valid movement and what's not valid
- In the Game class, I don't like the two-instruction update of the snake + egg ; there is temporal coupling here

  ```python
  egg_eaten = self._snake.will_eat_egg(self._egg)
  self._snake.move(egg_eaten)
  ```

- I tried mutation testing with `cosmic-ray`, but it didn't work really well. Then I tried `mutmut`, it's much easier to run.
  - The results are interesting but there is a lot of what I would consider false positives, e.g. changing the values of enums.
  - Not sure it would help students check whether their tests are good or bad.

**Possible TODOs:**

- [ ] Fix the typings in the tests
- [ ] Apply "nullable infrastructure" patterns and test without mocks (not sure it makes a lot of sense here, we'll see)
- [ ] Try swapping in a TermUI interface -> probably not compatible with Nullable infrastructure, as it would be a _different_ UI. Would that one need to be nullable as well ?
- [ ] Refactor: make the game not square
