from typing import Self


class Key:
    def __init__(self, keys: tuple[str, ...] | str) -> None:
        match keys:
            case str():
                self._keys = tuple((keys,))  # noqa: C409
            case tuple():
                self._keys = keys

    def __str__(self) -> str:
        return "/".join(f'"{key}"' for key in self._keys)

    def __repr__(self) -> str:
        return str(self)

    def __len__(self) -> int:
        return self._keys.__len__()

    def match(self, key: Self) -> bool:
        if len(self) != len(key):
            return False
        return all(self_key == key for self_key, key in zip(self._keys, key._keys, strict=False))  # noqa: SLF001
