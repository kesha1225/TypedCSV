from typing import Union, Type, Any
from typing_extensions import Protocol
from _csv import Dialect

_DialectLike = Union[str, Dialect, Type[Dialect]]


class _Writer(Protocol):
    def write(self, s: str) -> Any:
        ...
