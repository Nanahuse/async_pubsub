from __future__ import annotations
from typing import Generic, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from .key import Key
    from .hub import Hub


T = TypeVar("T")


class Publisher(Generic[T]):
    def __init__(self, hub: Hub, key: Key):
        self.__hub = hub
        self.__key = key

    async def publish(self, value: T):
        await self.__hub.publish(self.__key, value)

    def count_subscribers(self):
        return self.__hub.count_subscribers(self.__key)
