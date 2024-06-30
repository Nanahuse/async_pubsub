from __future__ import annotations
from typing import Awaitable, Callable, Generic, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from .key import Key
    from .hub import Hub

T = TypeVar("T")


class Subscriber(Generic[T]):
    def __init__(self, hub: Hub, key: Key, callback: Callable[[T], Awaitable[None]]):
        hub.add_subscriber(self)
        self.__hub = hub
        self.__key = key
        self.__callback = callback

    def __del__(self):
        self.__hub.delete_subscriber(self)

    def is_match(self, key: Key):
        return self.__key.match(key)

    async def subscribe(self, key: Key, value: T):
        if self.is_match(key):
            await self.__callback(value)
