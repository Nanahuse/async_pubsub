from __future__ import annotations
from typing import Generic, TypeVar, TYPE_CHECKING


from .topic import Topic

if TYPE_CHECKING:
    from .hub import Hub


T = TypeVar("T")


class Publisher(Generic[T]):
    def __init__(self, hub: Hub, topic: Topic[T]):
        self.__hub = hub
        self.__topic = topic

    async def publish(self, value: T):
        await self.__hub.publish(self.__topic.key, value)

    def count_subscribers(self):
        return self.__hub.count_subscribers(self.__topic.key)
