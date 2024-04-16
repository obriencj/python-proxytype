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

:author: Christopher O'Brien  <obriencj@preoccupied.net>
:license: GPL v3
"""


from preoccupied.proxytype import proxytype
from unittest import TestCase


class RuntimeTest(TestCase):

    def test_decorator_noop(self):
        # test that the decorator does nothing at runtime.

        class Foo:
            ...

        Bar = proxytype(None, None)(Foo)

        self.assertIs(Foo, Bar)


    def test_decorator_unary_noop(self):
        # test that the unary variation of the decorator also does
        # nothing at runtime.

        class Foo:
            ...

        Bar = proxytype(None)(Foo)

        self.assertIs(Foo, Bar)


# The end.
