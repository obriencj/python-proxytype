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
MyPy plugin for preoccupied.proxytype

Enable this plugin in MyPy to use the static analysis decoration of
the proxytype class decorator.

```ini filename=setup.cfg
[mypy]
plugins =
  preoccupied.proxytype.mypy
```

:author: Christopher O'Brien  <obriencj@preoccupied.net>
:license: GPL v3
"""


from mypy.nodes import Decorator, FuncDef, OverloadedFuncDef, TypeInfo
from mypy.plugin import ClassDefContext, MethodContext, Plugin
from mypy.types import CallableType, Instance


# This string needs to refer to the fully-qualified identifier for the
# above class, which stands as our sentinel to trigger the plugin's
# behavior.
PTB_CALL = "preoccupied.proxytype.ProxyTypeBuilder.__call__"


def clone_func(
        fn: FuncDef,
        cls: TypeInfo,
        returntype: Instance) -> FuncDef:

    tp = cast(CallableType, fn.type)
    cpt = tp.copy_modified()

    # overwrite self
    slf = cast(Instance, cpt.arg_types[0])
    slf = slf.copy_modified()
    slf.type = cls
    cpt.arg_types[0] = slf

    # overwrite return type
    if returntype is not None:
        n = returntype.copy_modified()
        n.args = (tp.ret_type, )
        cpt.ret_type = n

    cp = FuncDef(fn._name, None)
    cp.type = cpt
    cp.info = cls  # this particular field took so long to debug

    return cp


def clone_decorator(
        dec: Decorator,
        cls: TypeInfo,
        returntype: Instance) -> Decorator:

    cp = Decorator(clone_func(dec.func, cls, returntype),
                   dec.decorators, dec.var)
    cp.is_overload = dec.is_overload

    return cp


def clone_overloaded(
        ov: OverloadedFuncDef,
        cls: TypeInfo,
        returntype: Instance) -> OverloadedFuncDef:

    items: List[Union[Decorator, FuncDef]] = []
    for item in ov.items:
        if isinstance(item, Decorator):
            item = clone_decorator(item, cls, returntype)
        elif isinstance(item, FuncDef):
            item = clone_func(item, cls, returntype)
        items.append(item)

    cp = OverloadedFuncDef(items)
    cp._fullname = ov.fullname

    return cp


def decorate_proxytype(wrap: TypeInfo, orig: Instance, virt: Instance):
    """
    Creates methods on wrap cloned from orig, modified to return
    virt wrappers.

    :param wrap: the type definition as decorated by
    ``@proxytype(orig, virt)``

    :param orig: the type definition to copy fields from

    :param virt: the type definition for wrapping the original result
    types in
    """

    for name, sym in orig.type.names.items():

        if name.startswith("_") or name in wrap.names:
            # don't copy hidden methods, nor methods that are
            # explicitly defined already in the decorated class
            continue

        node = sym.node
        if isinstance(node, FuncDef):
            nsym = sym.copy()
            nsym.node = clone_func(node, wrap, virt)
            wrap.names[name] = nsym

        elif isinstance(node, OverloadedFuncDef):
            nsym = sym.copy()
            nsym.node = clone_overloaded(node, wrap, virt)
            wrap.names[name] = nsym

        else:
            # ignore others
            pass


def handle_proxytype_hook(ctx: MethodContext):
    wrap = ctx.context.info     # type: ignore
    orig, virt = ctx.type.args  # type: ignore

    decorate_proxytype(wrap, orig, virt)

    return ctx.default_return_type


class ProxyTypePlugin(Plugin):

    def get_method_hook(self, fullname: str):
        if fullname == PTB_CALL:
            return handle_proxytype_hook
        return None


def plugin(version: str):
    # mypy plugin loading point

    return ProxyTypePlugin


# The end.
