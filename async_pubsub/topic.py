from dataclasses import dataclass
from typing import Type, Generic, TypeVar

from .key import Key

T = TypeVar("T")


@dataclass(frozen=True)
class Topic(Generic[T]):
    type: Type[T]
    key: Key
