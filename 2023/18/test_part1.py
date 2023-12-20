import unittest
from main import read_file, part1, Field, State


class TestDay18Part1(unittest.TestCase):
    def test_read_file(self):
        field, instructions = read_file("2023/18/testdata/1.txt")
        self.assertIsInstance(field, Field)
        self.assertEqual(field.grid[0][0].state, State.DUG)
        self.assertEqual(len(instructions), 14)

    def test_part1(self):
        field, instructions = read_file("2023/18/testdata/1.txt")
        retval = part1(field, instructions)
        self.assertEqual(retval, 62)

        field, instructions = read_file("2023/18/testdata/2.txt")
        retval = part1(field, instructions)
        self.assertEqual(retval, 55)


if __name__ == "__main__":
    unittest.main()
