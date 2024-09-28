from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from .subscriber import Subscriber

if TYPE_CHECKING:
    from .key import Key
    from .topic import Topic

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self) -> None:
        self._subscribers = set[Subscriber]()

    async def publish(self, key: Key, value: Any) -> None:  # noqa: ANN401
        logger.debug("publish: %s", key)
        for sub in self._subscribers:
            await sub.subscribe(key, value)

    def add_subscriber(self, subscriber: Subscriber) -> None:
        self._subscribers.add(subscriber)

    def delete_subscriber(self, subscriber: Subscriber) -> None:
        self._subscribers.discard(subscriber)

    def count_subscribers(self, topic: Topic) -> int:
        return sum(1 for sub in self._subscribers if sub.is_match(topic.key))
