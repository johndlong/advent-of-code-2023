import unittest
from main import read_file, part2, part2_prediction


class TestDay9Part2(unittest.TestCase):
    def test_prediction(self):
        testdata = [
            ([0, 3, 6, 9, 12, 15], -3),
            ([1, 3, 6, 10, 15, 21], 0),
            ([10, 13, 16, 21, 30, 45], 5),
        ]

        for test in testdata:
            values = test[0]
            expected_result = test[1]
            pred = part2_prediction(values)
            self.assertEqual(pred, expected_result)

    def test_part1(self):
        sequences = read_file("2023/09/testdata/part1.txt")
        self.assertEqual(part2(sequences), 2)


if __name__ == "__main__":
    unittest.main()
