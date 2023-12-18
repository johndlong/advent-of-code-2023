import unittest
from main import read_file, part2


class TestDay16Part2(unittest.TestCase):
    def test_part2(self):
        platform = read_file("2023/16/testdata/1.txt")
        retval = part2(platform)
        self.assertEqual(retval, 51)


if __name__ == "__main__":
    unittest.main()
