import pytest

from async_pubsub import Key, Topic, Hub, Publisher, Subscriber


class Comparator:
    def __init__(self, value) -> None:
        self.counter = 0
        self.value = value
        self.received = None

    async def receive(self, value):
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
    topic = Topic(str, Key("key"))
    subs = [Subscriber(hub, topic, cmp.receive) for cmp in comps]

    for sub, cmp, expected in zip(subs, comps, (True, False)):
        await sub.subscribe(topic.key, "0")
        assert cmp.check_value() == expected and cmp.check_count(1)

    await hub.publish(topic.key, "1")

    for _, cmp, expected in zip(subs, comps, (False, True)):
        assert cmp.check_value() == expected and cmp.check_count(2)

    await hub.publish(topic.key, "none")
    for _, cmp, expected in zip(subs, comps, (False, False)):
        assert cmp.check_value() == expected and cmp.check_count(3)


@pytest.mark.asyncio
async def test_pub():
    hub = Hub()
    comps = [Comparator(str(i)) for i in range(3)]
    topics = [Topic(str, Key(str(i))) for i in range(3)]

    subs = [Subscriber(hub, topic, cmp.receive) for topic, cmp in zip(topics, comps)]
    pubs = [Publisher(hub, topic) for topic in topics]

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


def test_count():
    hub = Hub()
    assert hub.count_subscribers(Key("")) == 0

    keys = [Key(str(i)) for i in range(3)]
    comps = [Comparator(str(i)) for i in range(3)]

    subs = [Subscriber[str](hub, key, cmp.receive) for key, cmp in zip(keys, comps)]
    pub = Publisher[str](hub, keys[0])

    assert hub.count_subscribers(Key("1")) == 1
    assert pub.count_subscribers() == 1
