import unittest
from main import read_file, Grid, Position, Pipe


class TestDay10Part1(unittest.TestCase):
    def test_read_file(self):
        grid = read_file("2023/10/testdata/1.txt")
        self.assertIsInstance(grid, Grid)
        self.assertIsInstance(grid.positions[0][0], Position)
        self.assertEqual(grid.positions[0][0].pipe, Pipe.GROUND)

    def test_find_starting(self):
        grid = read_file("2023/10/testdata/1.txt")
        self.assertEqual(grid.find_starting(), (1, 1))

    def test_distances(self):
        testdata = {
            "2023/10/testdata/1.txt": 4,
            "2023/10/testdata/2.txt": 8,
        }

        for file, expected_result in testdata.items():
            grid = read_file(file)
            self.assertEqual(grid.max_distance(), expected_result)


if __name__ == "__main__":
    unittest.main()
