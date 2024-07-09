import pytest

from async_pubsub import Hub, Key, Topic, Publisher, Subscriber
from async_pubsub.controller import Controller


class Comparator:
    def __init__(self, value) -> None:
        self.counter = 0
        self.value = value
        self.received = None

    async def receive(self, value):
        self.received = value
        self.counter += 1

    def check_value(self) -> bool:
        return self.value == self.received

    def check_count(self, count: int) -> bool:
        return count == self.counter


def test_key():
    key = Key(("one", "two", "three"))

    assert key.match(Key(("one", "two", "three")))
    assert not key.match(Key(("one", "two", "none")))
    assert not key.match(Key(("one", "two")))


@pytest.mark.asyncio
async def test_hub():
    hub = Hub()

    topic = Topic(str, Key("key"))

    comp = Comparator("test")

    sub = hub.create_subscriber(topic, comp.receive)
    pub = hub.create_publisher(topic)

    await pub.publish("test")

    assert comp.check_value()

    await pub.publish("ng")

    assert not comp.check_value()


@pytest.mark.asyncio
async def test_sub():
    comps = [Comparator(str(i)) for i in range(2)]

    controller = Controller()
    topic = Topic(str, Key("key"))
    subs = [Subscriber(controller, topic, cmp.receive) for cmp in comps]

    for sub, cmp, expected in zip(subs, comps, (True, False)):
        await sub.subscribe(topic.key, "0")
        assert cmp.check_value() == expected and cmp.check_count(1)

    await controller.publish(topic.key, "1")

    for _, cmp, expected in zip(subs, comps, (False, True)):
        assert cmp.check_value() == expected and cmp.check_count(2)

    await controller.publish(topic.key, "none")
    for _, cmp, expected in zip(subs, comps, (False, False)):
        assert cmp.check_value() == expected and cmp.check_count(3)


@pytest.mark.asyncio
async def test_pub():
    controller = Controller()
    comps = [Comparator(str(i)) for i in range(3)]
    topics = [Topic(str, Key(str(i))) for i in range(3)]

    subs = [Subscriber(controller, topic, cmp.receive) for topic, cmp in zip(topics, comps)]
    pubs = [Publisher(controller, topic) for topic in topics]

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
    controller = Controller()
    assert controller.count_subscribers(Key("")) == 0

    topics = [Topic(str, Key(str(i))) for i in range(3)]
    comps = [Comparator(str(i)) for i in range(3)]

    subs = [Subscriber(controller, topic, cmp.receive) for topic, cmp in zip(topics, comps)]
    pub = Publisher(controller, topics[0])

    assert controller.count_subscribers(Key("1")) == 1
    assert pub.count_subscribers() == 1
