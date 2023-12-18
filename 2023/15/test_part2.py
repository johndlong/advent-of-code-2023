import unittest
from main import read_file, part2, Operation


class TestDay15Part2(unittest.TestCase):
    def test_read_file(self):
        data = read_file("2023/15/testdata/1.txt", label=True)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 11)
        self.assertEqual(data[0].label.name, "rn")
        self.assertEqual(data[0].operation, Operation.ADD)
        self.assertEqual(data[0].label.number, 1)

    def test_part2(self):
        data = read_file("2023/15/testdata/1.txt", label=True)
        retval = part2(data)
        self.assertEqual(retval, 145)


if __name__ == "__main__":
    unittest.main()
