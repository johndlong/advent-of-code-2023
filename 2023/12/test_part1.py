import unittest
from main import State, Spring, read_file, different_arrangements, is_valid


class TestDay12Part1(unittest.TestCase):
    def test_read_file(self):
        springs = read_file("2023/12/testdata/1.txt")
        self.assertEqual(springs[0].entries[0], State("#"))
        self.assertEqual(springs[0].entries[1], State("."))

    def test_is_valid(self):
        spring = Spring(
            entries=[State("#"), State("."), State("#"), State("."), State("#"), State("#"), State("#")],
            records=[1, 1, 3],
        )
        self.assertTrue(is_valid(spring.entries, spring.records))

        bad_spring = Spring(
            entries=[State("#"), State("#"), State("#"), State("."), State("#"), State("#"), State("#")],
            records=[1, 1, 3],
        )
        self.assertFalse(is_valid(bad_spring.entries, bad_spring.records))

    def test_different_arrangements(self):
        springs = read_file("2023/12/testdata/2.txt")

        testdata = [(0, 1), (1, 4), (2, 1), (3, 1), (4, 4), (5, 10)]
        for index, expected in testdata:
            arrangements = different_arrangements(springs[index])
            self.assertEqual(arrangements, expected)


if __name__ == "__main__":
    unittest.main()
