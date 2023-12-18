import unittest
from main import read_file, part1, calculate_hash


class TestDay15Part1(unittest.TestCase):
    def test_read_file(self):
        data = read_file("2023/15/testdata/1.txt")
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 11)

    def test_calc_hash(self):
        testdata = [
            ("HASH", 52),
            ("rn=1", 30),
            ("cm-", 253),
            ("qp=3", 97),
            ("cm=2", 47),
            ("qp-", 14),
            ("pc=4", 180),
            ("ot=9", 9),
            ("ab=5", 197),
            ("pc-", 48),
            ("pc=6", 214),
            ("ot=7", 231),
        ]

        for h, expected in testdata:
            self.assertEqual(calculate_hash(h), expected)

    def test_part1(self):
        data = read_file("2023/15/testdata/1.txt")
        retval = part1(data)
        self.assertEqual(retval, 1320)


if __name__ == "__main__":
    unittest.main()
