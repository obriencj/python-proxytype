# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this library; if not, see <http://www.gnu.org/licenses/>.


"""
preoccupied.proxytype - static analysis decorator for dynamic proxy classes

The `proxytype` class decorator is for use in cases where we need to
provide static typing information for a class that dynamically proxies
the methods of some other class.

:author: Christopher O'Brien <obriencj@preoccupied.net>
:license: GPL v3
"""


from typing import Generic, List, Type, TypeVar, Union, cast, overload


__all__ = ( "proxytype", )


PT = TypeVar("PT")  # Original type to proxy
RT = TypeVar("RT")  # New return type
CT = TypeVar("CT")  # Class type to augment


class ProxyTypeBuilder(Generic[PT, RT]):
    # this class, and more specifically its __call__ method, are used
    # as the sentinel to trigger the mypy plugin hook.
    def __call__(self, cls: Type[CT]) -> Type[CT]:
        return cls


def proxytype(
        orig_class: Type[PT],
        return_wrapper: Type[RT]) -> ProxyTypeBuilder[PT, RT]:

    """
    class decorator which, via its ProxyTypeBuilder return type,
    triggers augmentation of its wrapper class with the methods found
    in the orig_class type, having their first (self) argument changed
    to match the decorated class, and their return type to match the
    return_wrapper's generic

    The canonical example is MultiCallSession, eg.

    ```
    class ClientSession:
        # lots of methods here
        ...

    class VirtualCall(Generic[T]):
        result: T

    @proxytype(ClientSession, VirtualCall)
    class MultiCallSession:
        # all methods from ClientSession magically copied into
        # this during static analysys
        ...
    ```

    for example then, a method on ClientSession such as
      ``getPerms(self: ClientSession) -> List[str]``

    will be recreated on MultiCallSession as
      ``getPerms(self: MultiCallSession) -> VirtualCall[List[str]]``

    """

    return ProxyTypeBuilder()


# The end.
