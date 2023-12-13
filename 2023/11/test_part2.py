import unittest
from main import read_file, distance, Universe, CosmicEntity, NamedGalaxy


class TestDay11Part2(unittest.TestCase):
    def test_part2_example(self):
        grid = read_file("2023/11/testdata/1.txt")

        e10 = grid.expand(expansion_number=10)
        r10 = e10.shortest_pairs()
        self.assertEqual(r10, 1030)

        e100 = grid.expand(expansion_number=100)
        r100 = e100.shortest_pairs()
        self.assertEqual(r100, 8410)


if __name__ == "__main__":
    unittest.main()
