import unittest
from main import Movement, Node, read_file, traverse_part1


class TestDay8(unittest.TestCase):
    def test_read_file(self):
        nodes, sequence = read_file("2023/08/testdata/1.txt")
        self.assertEqual(sequence, [Movement.RIGHT, Movement.LEFT])
        self.assertEqual(nodes["AAA"], Node("AAA", "BBB", "CCC"))

    def test_traverse(self):
        testdata = {
            "2023/08/testdata/1.txt": 2,
            "2023/08/testdata/2.txt": 6,
        }

        for file, expected_result in testdata.items():
            nodes, sequence = read_file(file)
            steps = traverse_part1(nodes, sequence)
            self.assertEqual(steps, expected_result)


if __name__ == "__main__":
    unittest.main()
