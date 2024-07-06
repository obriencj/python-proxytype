"""
Sample for mypy to operator on so we can verify our plugin works.
"""


from typing import Any, Generic, List, Tuple, TypeVar
from preoccupied.proxytype import proxytype


class Normal:
    def doSomething(self, how_many: int, etc: Any) -> List[int]:
        ...

    def doAnother(self, wut: Any, **kwds: Any) -> bool:
        ...

    def getName(self) -> str:
        ...

    @staticmethod
    def getStatic() -> int:
        ...


@proxytype(Normal)
class Delayed:
    def getName(self) -> str:
        ...


def check_normal(obj: Normal) -> Tuple[str, List[int], bool]:
    name = obj.getName()
    li = obj.doSomething(1, None)
    bi = obj.doAnother("hello")
    return (name, li, bi)


def check_delayed(obj: Delayed) -> Tuple[str, List[int], bool]:
    name = obj.getName()
    li = obj.doSomething(1, None)
    bi = obj.doAnother("hello")
    return (name, li, bi)


# The end.
