# pylint: skip-file
import unittest
from main import Card, Hand, HandRank, winning_total


class TestDay7(unittest.TestCase):
    def test_card(self):
        self.assertEqual(Card.to_card("J", joker=True), Card(1))

    def test_hand_rank(self):
        five = Hand([Card(13), Card(13), Card(13), Card(13), Card(1)])
        self.assertEqual(five.rank(), HandRank.FIVE_OF_A_KIND)

        four = Hand([Card(13), Card(13), Card(13), Card(1), Card(12)])
        self.assertEqual(four.rank(), HandRank.FOUR_OF_A_KIND)

        fh = Hand([Card(13), Card(13), Card(12), Card(12), Card(1)])
        self.assertEqual(fh.rank(), HandRank.FULL_HOUSE)

        three = Hand([Card(13), Card(13), Card(1), Card(12), Card(11)])
        self.assertEqual(three.rank(), HandRank.THREE_OF_A_KIND)

        pair = Hand([Card(13), Card(1), Card(12), Card(11), Card(10)])
        self.assertEqual(pair.rank(), HandRank.ONE_PAIR)

        hk = Hand([Card(1), Card(12), Card(11), Card(10), Card(9)])
        self.assertEqual(hk.rank(), HandRank.ONE_PAIR)

    def test_example_hands(self):
        # QQQQ2 > JKKK2
        ex1_a = Hand(
            [
                Card.to_card("Q"),
                Card.to_card("Q"),
                Card.to_card("Q"),
                Card.to_card("Q"),
                Card.to_card("2"),
            ]
        )
        ex1_b = Hand(
            [Card.to_card("J", joker=True), Card.to_card("K"), Card.to_card("K"), Card.to_card("K"), Card.to_card("2")]
        )
        self.assertTrue(ex1_a > ex1_b)

    def test_part2(self):
        hands = Hand.read_file("2023/07/testdata/data.txt", joker=True)
        self.assertEqual(winning_total(hands), 5905)


if __name__ == "__main__":
    unittest.main()
