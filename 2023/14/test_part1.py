import unittest
from main import read_file, part1, Platform, Item


class TestDay14Part1(unittest.TestCase):
    def test_read_file(self):
        platform = read_file("2023/14/testdata/1.txt")
        self.assertIsInstance(platform, Platform)
        self.assertEqual(platform.positions[0][0], Item.ROUNDED_ROCK)
        self.assertEqual(platform.positions[0][1], Item.EMPTY_SPACE)

    def test_north_slide(self):
        platform = read_file("2023/14/testdata/1.txt")
        expected = read_file("2023/14/testdata/1-N-slide.txt")

        platform.slide()
        for i, row in enumerate(platform.positions):
            for j, entry in enumerate(row):
                self.assertEqual(entry, expected.positions[i][j])

    def test_part1(self):
        platform = read_file("2023/14/testdata/1.txt")
        retval = part1(platform)
        self.assertEqual(retval, 136)


if __name__ == "__main__":
    unittest.main()
