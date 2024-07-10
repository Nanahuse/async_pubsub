from __future__ import annotations

import logging

from .key import Key
from .subscriber import Subscriber

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Controller(object):
    def __init__(self):
        self.__subscribers = set[Subscriber]()

    async def publish(self, key: Key, value):
        logger.debug(f"publish: {key}")
        for sub in self.__subscribers:
            await sub.subscribe(key, value)

    def add_subscriber(self, subscriber: Subscriber):
        self.__subscribers.add(subscriber)

    def delete_subscriber(self, subscriber: Subscriber):
        self.__subscribers.discard(subscriber)

    def count_subscribers(self, key: Key):
        return sum(1 for sub in self.__subscribers if sub.is_match(key))
