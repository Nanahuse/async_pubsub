from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from .controller import Controller
    from .topic import Topic


T = TypeVar("T")


class Publisher(Generic[T]):
    def __init__(self, controller: Controller, topic: Topic[T]) -> None:
        self._controller = controller
        self._topic = topic

    async def publish(self, value: T) -> None:
        await self._controller.publish(self._topic.key, value)

    def count_subscribers(self) -> int:
        return self._controller.count_subscribers(self._topic)
