import unittest
from main import read_file, part1, Land, Item


class TestDay13Part1(unittest.TestCase):
    def test_read_file(self):
        lands = read_file("2023/13/testdata/complete.txt")
        self.assertIsInstance(lands[0], Land)
        self.assertIsInstance(lands[0].positions[0][0], Item)
        self.assertEqual(lands[0].positions[0][0], Item.ROCK)
        self.assertEqual(lands[0].positions[0][1], Item.ASH)

    def test_vertical_mirror(self):
        lands = read_file("2023/13/testdata/complete.txt")
        retval = lands[0].veritical_mirror()
        self.assertEqual(retval, 5)
        fail_horizontal = lands[0].horizontal_mirror()
        self.assertEqual(fail_horizontal, None)

    def test_horizontal_mirror(self):
        lands = read_file("2023/13/testdata/complete.txt")
        retval = lands[1].horizontal_mirror()
        self.assertEqual(retval, 4)

    def test_part1(self):
        lands = read_file("2023/13/testdata/complete.txt")
        retval = part1(lands)
        self.assertEqual(retval, 405)

    def test_part1_debug(self):
        lands = read_file("2023/13/testdata/debug.txt")
        retval = part1(lands)
        self.assertEqual(retval, 709)


if __name__ == "__main__":
    unittest.main()
