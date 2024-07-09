from __future__ import annotations
from typing import Generic, TypeVar, TYPE_CHECKING


from .topic import Topic

if TYPE_CHECKING:
    from .controller import Controller


T = TypeVar("T")


class Publisher(Generic[T]):
    def __init__(self, controller: Controller, topic: Topic[T]):
        self.__controller = controller
        self.__topic = topic

    async def publish(self, value: T):
        await self.__controller.publish(self.__topic.key, value)

    def count_subscribers(self):
        return self.__controller.count_subscribers(self.__topic.key)
