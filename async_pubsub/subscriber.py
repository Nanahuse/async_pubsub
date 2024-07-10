from __future__ import annotations
from typing import Awaitable, Callable, Generic, TypeVar, TYPE_CHECKING

from .key import Key
from .topic import Topic

if TYPE_CHECKING:
    from .controller import Controller


T = TypeVar("T")


class Subscriber(Generic[T]):
    def __init__(self, controller: Controller, topic: Topic[T], callback: Callable[[T], Awaitable[None]]):
        controller.add_subscriber(self)
        self.__controller = controller
        self.__topic = topic
        self.__callback = callback

    def __del__(self):
        self.__controller.delete_subscriber(self)

    def is_match(self, key: Key):
        return self.__topic.key.match(key)

    async def subscribe(self, key: Key, value: T):
        if self.is_match(key):
            await self.__callback(value)
