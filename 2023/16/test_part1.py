import unittest
from main import read_file, part1, Space, Direction, Item


class TestDay16Part1(unittest.TestCase):
    def test_read_file(self):
        space = read_file("2023/16/testdata/1.txt")
        self.assertIsInstance(space, Space)
        self.assertEqual(space.grid[0][0].value, Item.EMPTY_SPACE)
        self.assertEqual(space.grid[0][1].value, Item.VERTICAL_SPLITTER)

    def test_next_positions(self):
        platform = read_file("2023/16/testdata/1.txt")
        testdata = [
            [(0, 0, Direction.EAST), [(1, 0, Direction.EAST)]],
            [(1, 0, Direction.EAST), [(1, 1, Direction.SOUTH)]],
            [(1, 1, Direction.SOUTH), [(1, 2, Direction.SOUTH)]],
            [(1, 6, Direction.SOUTH), [(1, 7, Direction.SOUTH)]],
            [(1, 7, Direction.SOUTH), [(2, 7, Direction.EAST), (0, 7, Direction.WEST)]],
            [(2, 7, Direction.EAST), [(3, 7, Direction.EAST)]],
            [(0, 7, Direction.WEST), []],
            [(3, 7, Direction.EAST), [(4, 7, Direction.EAST)]],
            [(4, 7, Direction.EAST), [(4, 6, Direction.NORTH)]],
            [(4, 6, Direction.NORTH), [(5, 6, Direction.EAST)]],
            [(5, 6, Direction.EAST), [(6, 6, Direction.EAST)]],
            [(6, 6, Direction.EAST), [(6, 7, Direction.SOUTH)]],
        ]

        for position, expected in testdata:
            next_positions = platform._get_next_positions(position[0], position[1], position[2])
            self.assertEqual(next_positions, expected)

    def test_part1(self):
        platform = read_file("2023/16/testdata/1.txt")
        retval = part1(platform)
        self.assertEqual(retval, 46)


if __name__ == "__main__":
    unittest.main()
