from abc import abstractmethod
from typing import Iterable, Optional, Protocol

from ..direction import Direction
from ..types import Position


class UiProtocol(Protocol):
    @abstractmethod
    def draw(self, snake: Iterable[Position], egg: Position) -> None:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def direction(self) -> Direction:  # pragma: no cover
        raise NotImplementedError
