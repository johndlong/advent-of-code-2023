import unittest
from main import read_file, part1, part1_prediction


class TestDay8Part2(unittest.TestCase):
    def test_read_file(self):
        sequences = read_file("2023/09/testdata/part1.txt")
        self.assertTrue(len(sequences) == 3)
        self.assertEqual(sequences[0], [0, 3, 6, 9, 12, 15])
        self.assertEqual(sequences[1], [1, 3, 6, 10, 15, 21])
        self.assertEqual(sequences[2], [10, 13, 16, 21, 30, 45])

    def test_prediction(self):
        testdata = [
            ([0, 3, 6, 9, 12, 15], 18),
            ([1, 3, 6, 10, 15, 21], 28),
            ([10, 13, 16, 21, 30, 45], 68),
        ]

        for test in testdata:
            values = test[0]
            expected_result = test[1]
            pred = part1_prediction(values)
            self.assertEqual(pred, expected_result)

    def test_part1(self):
        sequences = read_file("2023/09/testdata/part1.txt")
        self.assertEqual(part1(sequences), 114)


if __name__ == "__main__":
    unittest.main()
