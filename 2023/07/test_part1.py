# pylint: skip-file
import unittest
from main import Card, Hand, HandRank, part1


class TestDay7(unittest.TestCase):
    def test_card(self):
        self.assertEqual(Card.to_card("A"), Card(14))
        self.assertEqual(Card.to_card(5), Card(5))

    def test_hand_rank(self):
        five = Hand([Card(13) for _ in range(5)])
        self.assertEqual(five.rank(), HandRank.FIVE_OF_A_KIND)

        four = Hand([Card(13), Card(13), Card(13), Card(13), Card(12)])
        self.assertEqual(four.rank(), HandRank.FOUR_OF_A_KIND)

        fh = Hand([Card(13), Card(13), Card(13), Card(12), Card(12)])
        self.assertEqual(fh.rank(), HandRank.FULL_HOUSE)

        three = Hand([Card(13), Card(13), Card(13), Card(12), Card(11)])
        self.assertEqual(three.rank(), HandRank.THREE_OF_A_KIND)

        two_pair = Hand([Card(13), Card(13), Card(12), Card(12), Card(11)])
        self.assertEqual(two_pair.rank(), HandRank.TWO_PAIR)

        pair = Hand([Card(13), Card(13), Card(12), Card(11), Card(10)])
        self.assertEqual(pair.rank(), HandRank.ONE_PAIR)

        hk = Hand([Card(13), Card(12), Card(11), Card(10), Card(9)])
        self.assertEqual(hk.rank(), HandRank.HIGH_CARD)

    def test_hand_compare(self):
        pair = Hand([Card(13), Card(13), Card(12), Card(11), Card(10)])
        hk = Hand([Card(13), Card(12), Card(11), Card(10), Card(9)])
        hk2 = Hand([Card(12), Card(11), Card(10), Card(9), Card(8)])

        self.assertTrue(pair > hk)
        self.assertTrue(hk > hk2)
        self.assertFalse(pair < hk)
        self.assertEqual(pair, pair)

    def test_example_hands(self):
        # 33332 >  2AAAA
        ex1_a = Hand([Card(3), Card(3), Card(3), Card(3), Card(2)])
        ex1_b = Hand([Card(2), Card.to_card("A"), Card.to_card("A"), Card.to_card("A"), Card.to_card("A")])
        self.assertTrue(ex1_a > ex1_b)

        # 77888 > 77788
        ex2_a = Hand([Card(7), Card(7), Card(8), Card(8), Card(8)])
        ex2_b = Hand([Card(7), Card(7), Card(7), Card(8), Card(8)])
        self.assertTrue(ex2_a > ex2_b)

    def test_part1(self):
        hands = Hand.read_file("2023/07/testdata/data.txt")
        self.assertEqual(part1(hands), 6440)


if __name__ == "__main__":
    unittest.main()
