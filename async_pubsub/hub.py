from collections.abc import Awaitable, Callable
from typing import TypeVar

from .controller import Controller
from .publisher import Publisher
from .subscriber import Subscriber
from .topic import Topic

T = TypeVar("T")


class Hub:
    def __init__(self) -> None:
        self.__controller = Controller()

    def create_subscriber(self, topic: Topic[T], callback: Callable[[T], Awaitable[None]]) -> Subscriber[T]:
        return Subscriber(self.__controller, topic, callback)

    def create_publisher(self, topic: Topic[T]) -> Publisher[T]:
        return Publisher(self.__controller, topic)

    def count_subscribers(self, topic: Topic[T]) -> int:
        return self.__controller.count_subscribers(topic)
