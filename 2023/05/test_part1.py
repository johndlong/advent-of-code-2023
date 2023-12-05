import unittest
from part1 import Almanac


class TestDay5(unittest.TestCase):
    def setUp(self):
        self.almanac = Almanac.process_input("2023/05/testdata/testdata.txt")

    def test_main(self):
        self.assertEqual(self.almanac.closest_location(), 35)


if __name__ == "__main__":
    unittest.main()
