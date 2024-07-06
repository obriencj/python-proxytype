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


from mypy.build import build
from mypy.modulefinder import BuildSource
from mypy.options import Options
from os.path import dirname
from unittest import TestCase


def load_sample(name, enable=True):

    # pkg_resources is deprecated and importlib.resources is a PITA
    # so... screw it, back to basics.
    datadir = f"{dirname(__file__)}/data"

    opts = Options()
    opts.mypy_path = [datadir, ]
    opts.show_traceback = True

    # if config_file is left None then the plugins value will be
    # ignored, because reasons.
    opts.config_file =  f"{datadir}/mypy.cfg"

    if enable:
        opts.plugins = ["preoccupied.proxytype", ]

    src = BuildSource(f"{datadir}/{name}.pyi", module=name,
                      text=None, base_dir=datadir, followed=False)

    return build([src, ], opts)


class BinaryTest(TestCase):


    def test_plugin_disabled(self):
        bld = load_sample("binary", enable=False)
        data = bld.files["binary"]

        normal = data.names["Normal"].node
        delayed = data.names["Delayed"].node
        delres = data.names["DelayedResult"].node

        self.assertTrue(bld.errors)

        self.assertIn('"Delayed" has no attribute "doSomething"',
                      bld.errors[0])
        self.assertIn('"Delayed" has no attribute "doAnother"',
                      bld.errors[1])

        self.assertIn("doSomething", normal.names)
        self.assertIn("doAnother", normal.names)
        self.assertIn("getName", normal.names)
        self.assertIn("getStatic", normal.names)

        self.assertNotIn("doSomething", delayed.names)
        self.assertNotIn("doAnother", delayed.names)
        self.assertIn("getName", delayed.names)
        self.assertNotIn("getStatic", delayed.names)


    def test_plugin_enabled(self):
        bld = load_sample("binary", enable=True)
        data = bld.files["binary"]

        normal = data.names["Normal"].node
        delayed = data.names["Delayed"].node
        delres = data.names["DelayedResult"].node

        self.assertEqual(bld.errors, [])

        self.assertIn("doSomething", normal.names)
        self.assertIn("doAnother", normal.names)
        self.assertIn("getName", normal.names)
        self.assertIn("getStatic", normal.names)

        self.assertIn("doSomething", delayed.names)
        self.assertIn("doAnother", delayed.names)
        self.assertIn("getName", delayed.names)
        self.assertIn("getStatic", delayed.names)


class UnaryTest(TestCase):


    def test_plugin_disabled(self):
        bld = load_sample("unary", enable=False)
        data = bld.files["unary"]

        normal = data.names["Normal"].node
        delayed = data.names["Delayed"].node

        self.assertTrue(bld.errors)

        self.assertIn('"Delayed" has no attribute "doSomething"',
                      bld.errors[0])
        self.assertIn('"Delayed" has no attribute "doAnother"',
                      bld.errors[1])

        self.assertIn("doSomething", normal.names)
        self.assertIn("doAnother", normal.names)
        self.assertIn("getName", normal.names)
        self.assertIn("getStatic", normal.names)

        self.assertNotIn("doSomething", delayed.names)
        self.assertNotIn("doAnother", delayed.names)
        self.assertIn("getName", delayed.names)
        self.assertNotIn("getStatic", delayed.names)


    def test_plugin_enabled(self):
        bld = load_sample("unary", enable=True)
        data = bld.files["unary"]

        normal = data.names["Normal"].node
        delayed = data.names["Delayed"].node

        self.assertEqual(bld.errors, [])

        self.assertIn("doSomething", normal.names)
        self.assertIn("doAnother", normal.names)
        self.assertIn("getName", normal.names)
        self.assertIn("getStatic", normal.names)

        self.assertIn("doSomething", delayed.names)
        self.assertIn("doAnother", delayed.names)
        self.assertIn("getName", delayed.names)
        self.assertIn("getStatic", delayed.names)


# The end.
