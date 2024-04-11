# Overview

preoccupied.proxytype is a [Python] package providing a [MyPy] plugin and a
class decorator for triggering that plugin. The decorator can be used
to indicate that a decorated class should be considered during static
analysis to posess all of the methods from another class.

[python]: https://python.org

[MyPy]: https://mypy-lang.org

This pattern is distinct from inheritance, in that it will also apply
a transformation to the return type of the copied methods. It is valid
for this transformed return type to be incompatible with the original
template class's method signature.

This is useful in situations where a dynamic class wraps or proxies
its calls to another instance, optionally decorating them in the
process.

The class decorator has no behavior at runtime -- it does not
implement the proxying. It is only there to provide a way to declare
such behavior during static analysis.


## Installation

Install from the latest PyPI release

```bash
pip install --user preoccupied.proxytype
```

Install from git master

```bash
pip install --user git+https://github.com/obriencj/proxytype
```


## Enable plugin

At runtime the proxytype class decorator does not introduce a MyPy
dependency. However in order for it to operate during MyPy's static
analysis checks the plugin must be enabled. For example:

```ini filename=setup.cfg
[mypy]
plugins =
  preoccupied.proxytype.mypy
```


## Usage of proxytype

```python

from preoccupied.proxytype import proxytype


class ClientSession:
    def doSomething(self, how_many: int, etc: Any) -> List[int]:
        ...

    def doAnother(self, wut: Any, **kwds: Any) -> bool:
        ...

    def getName(self) -> str:
        ...


RT = TypeVar("RT")

class DelayResult(Generic[RT]):
    resultValue: RT


@proxytype(ClientSession, DelayResult)
class DelayClientSession:
    def getName(self) -> str:
        ...
```

This will cause static analysys via MyPy of the `DelayClientSession`
to appear as if it had been declared as:

```python

class DelayClientSession:
    def doSomething(self, how_many: int, etc: Any) -> DelayResult[List[int]]:
        ...

    def doAnother(self, wut: Any, **kwds: Any) -> DelayResult[bool]:
        ...

    def getName(self) -> str:
        ...
```


## Contact

author: Christopher O'Brien  <obriencj@preoccupied.net>

original git repository: <https://github.com/obriencj/preoccupied-proxytype>


## License

This library is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation; either version 3 of the
License, or (at your option) any later version.

This library is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, see
<http://www.gnu.org/licenses/>.
