import unittest

from edulib import economics, mathematics, physics, chemistry, text
from edulib.text import prints


class PackageImportTests(unittest.TestCase):
    def test_all_package_modules_are_importable(self):
        modules = (economics, mathematics, physics, chemistry, text, prints)
        self.assertEqual(len(modules), 6)


if __name__ == "__main__":
    unittest.main()
