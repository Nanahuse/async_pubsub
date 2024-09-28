from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from .controller import Controller
    from .key import Key
    from .topic import Topic


T = TypeVar("T")


class Subscriber(Generic[T]):
    def __init__(self, controller: Controller, topic: Topic[T], callback: Callable[[T], Awaitable[None]]) -> None:
        controller.add_subscriber(self)
        self._controller = controller
        self._topic = topic
        self._callback = callback

    def __del__(self) -> None:
        self._controller.delete_subscriber(self)

    def is_match(self, key: Key) -> bool:
        return self._topic.key.match(key)

    async def subscribe(self, key: Key, value: T) -> None:
        if self.is_match(key):
            await self._callback(value)
