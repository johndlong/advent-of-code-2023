# pylint: skip-file
import unittest
from main import Almanac, Range, process_range


class TestDay5(unittest.TestCase):
    def setUp(self):
        self.almanac = Almanac.process_input("2023/05/testdata/testdata.txt", seed_range=True)

    def test_process_range(self):
        source = (1, 1)
        dest = (2, 1)
        self.assertEqual(process_range(source, dest), None)

        # 1 2 3 4 5
        #   2 3
        source = (1, 5)
        dest = (2, 2)
        expected = Range((2, 2), (1, 1), (4, 2))
        self.assertEqual(process_range(source, dest), expected)

        # 1 2 3 4 5
        #   2 3 4 5 6
        source = (1, 5)
        dest = (2, 5)
        expected = Range((2, 4), before=(1, 1), after=None)
        self.assertEqual(process_range(source, dest), expected)

        #     3 4 5 6 7
        #   2 3 4 5 6
        source = (3, 5)
        dest = (2, 5)
        expected = Range((3, 4), before=None, after=(7, 1))
        self.assertEqual(process_range(source, dest), expected)

        #     3 4 5
        #   2 3 4 5 6
        source = (3, 2)
        dest = (2, 5)
        expected = Range((3, 2), before=None, after=None)
        self.assertEqual(process_range(source, dest), expected)

        source = (2010168426, 158205686)
        dest = (1531317439, 615453278)
        expected = Range(within=(2010168426, 136602291), before=None, after=(2146770717, 21603395))
        self.assertEqual(process_range(source, dest), expected)

    def test_main(self):
        self.assertEqual(self.almanac.closest_location(), 46)


if __name__ == "__main__":
    unittest.main()
