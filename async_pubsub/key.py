from typing import Self


class Key(object):
    def __init__(self, keys: tuple[str, ...] | str):
        match keys:
            case str():
                self.__keys = tuple((keys,))
            case tuple():
                self.__keys = keys

    def __str__(self) -> str:
        return "/".join(f'"{key}"' for key in self.__keys)

    def __repr__(self) -> str:
        return str(self)

    def __len__(self):
        return self.__keys.__len__()

    def match(self, key: Self):
        if len(self) != len(key):
            return False
        return all(self_key == key for self_key, key in zip(self.__keys, key.__keys))
