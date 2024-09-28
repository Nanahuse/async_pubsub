from dataclasses import dataclass
from typing import Generic, TypeVar

from .key import Key

T = TypeVar("T")


@dataclass(frozen=True)
class Topic(Generic[T]):
    type: type[T]
    key: Key
