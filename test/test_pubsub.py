import pytest

from async_pubsub import Key, Hub, Publisher, Subscriber


class Comparator:
    def __init__(self, value) -> None:
        self.counter = 0
        self.value = value
        self.received = None

    async def receive(self, value):
        global counter
        self.received = value
        self.counter += 1

    def check_value(self):
        return self.value == self.received

    def check_count(self, count: int):
        return count == self.counter


def test_key():
    key = Key(("one", "two", "three"))

    assert key.match(Key(("one", "two", "three")))
    assert not key.match(Key(("one", "two", "none")))
    assert not key.match(Key(("one", "two")))


@pytest.mark.asyncio
async def test_sub():
    comps = [Comparator(str(i)) for i in range(2)]

    hub = Hub()
    key = Key("key")
    subs = [Subscriber[str](hub, key, cmp.receive) for cmp in comps]

    for sub, cmp, expected in zip(subs, comps, (True, False)):
        await sub.subscribe(key, "0")
        assert cmp.check_value() == expected and cmp.check_count(1)

    await hub.publish(key, "1")

    for _, cmp, expected in zip(subs, comps, (False, True)):
        assert cmp.check_value() == expected and cmp.check_count(2)

    await hub.publish(key, "none")
    for _, cmp, expected in zip(subs, comps, (False, False)):
        assert cmp.check_value() == expected and cmp.check_count(3)


@pytest.mark.asyncio
async def test_pub():
    hub = Hub()
    comps = [Comparator(str(i)) for i in range(3)]
    keys = [Key(str(i)) for i in range(3)]

    subs = [Subscriber[str](hub, key, cmp.receive) for key, cmp in zip(keys, comps)]
    pubs = [Publisher[str](hub, key) for key in keys]

    await pubs[0].publish("0")
    assert comps[0].check_value()
    for cmp, count in zip(comps, (1, 0, 0)):
        assert cmp.check_count(count)

    await pubs[1].publish("none")
    assert not comps[1].check_value()
    for cmp, count in zip(comps, (1, 1, 0)):
        assert cmp.check_count(count)

    subs.clear()

    for pub in pubs:
        pub.publish("")

    for cmp, count in zip(comps, (1, 1, 0)):
        assert cmp.check_count(count)
