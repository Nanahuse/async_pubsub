from __future__ import annotations

from .key import Key
from .subscriber import Subscriber


class Hub(object):
    def __init__(self):
        self.__subscribers = set[Subscriber]()

    async def publish(self, key: Key, value):
        for sub in self.__subscribers:
            await sub.subscribe(key, value)

    def add_subscriber(self, subscriber: Subscriber):
        self.__subscribers.add(subscriber)

    def delete_subscriber(self, subscriber: Subscriber):
        self.__subscribers.discard(subscriber)
