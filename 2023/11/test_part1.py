import unittest
from main import read_file, distance, Universe, CosmicEntity, NamedGalaxy, Position


class TestDay11Part1(unittest.TestCase):
    def test_read_file(self):
        universe = read_file("2023/11/testdata/1.txt")
        self.assertIsInstance(universe, Universe)
        self.assertIsInstance(universe.positions[0][0], Position)
        self.assertEqual(universe.positions[0][0].val, CosmicEntity.EMPTY)
        self.assertEqual(universe.positions[0][3].val, CosmicEntity.GALAXY)

    def test_expanded(self):
        grid = read_file("2023/11/testdata/1.txt")
        expected_expanded = read_file("2023/11/testdata/expanded.txt")
        expanded = grid.expand()
        for row in expanded.positions:
            for pos in row:
                if pos.val == CosmicEntity.GALAXY:
                    self.assertEqual(pos.val, expected_expanded.positions[pos.y][pos.x].val)
                    self.assertEqual(pos.x, expected_expanded.positions[pos.y][pos.x].x)
                    self.assertEqual(pos.y, expected_expanded.positions[pos.y][pos.x].y)

    def test_distances(self):
        testdata = [
            (NamedGalaxy(5, 1, 6), NamedGalaxy(9, 5, 11), 9),
            (
                NamedGalaxy(1, 4, 0),
                NamedGalaxy(7, 9, 10),
                15,
            ),
            (
                NamedGalaxy(3, 0, 2),
                NamedGalaxy(6, 12, 7),
                17,
            ),
            (NamedGalaxy(8, 0, 11), NamedGalaxy(9, 5, 11), 5),
        ]
        for data in testdata:
            retval = distance(data[0], data[1])
            self.assertEqual(retval, data[2])

    def test_shortest_pairs(self):
        grid = read_file("2023/11/testdata/1.txt")
        expanded = grid.expand()
        retval = expanded.shortest_pairs()
        self.assertEqual(retval, 374)


if __name__ == "__main__":
    unittest.main()
