import unittest


from Deck import *


class TestDeck(unittest.TestCase):

    def test_deck(self):
        a = Card(ONE, RED, FILLED, STAR)
        b = Card(TWO, RED, FILLED, STAR)
        c = Card(THREE, RED, FILLED, STAR)
        d = Card(THREE, RED, FILLED, CIRCLE)
        e = Card(THREE, RED, FILLED, SQUARE)
        self.assertEqual(Deck.numberOfSets([a, b, c, d, e]), 2)
        self.assertTrue(Deck.hasSet([a, b, c, d, e]))
        badSet = {Card(number=3, colour=5, filling=8, shape=11),
                  Card(number=2, colour=6, filling=7, shape=12),
                  Card(number=2, colour=6, filling=9, shape=11)}
        self.assertFalse(Deck.hasSet(badSet))
        self.assertEqual(Deck.similarities(*list(badSet)), 0)

        self.assertTrue(
            Deck.hasSet({Card(number=3, colour=5, filling=8, shape=11),
                         Card(number=2, colour=6, filling=7, shape=12),
                         Card(number=2, colour=6, filling=9, shape=11)} | {a}))

        deck = Deck()
        threeCards = deck.drawGuarantee()
        self.assertTrue(Deck.hasSet(threeCards))
        self.assertRaises(
            ValueError, lambda x: deck.drawGuarantee(numberofcards=x), 0)

    def test_card(self):
        a = Card(ONE, RED, BLANK, STAR)
        self.assertEqual(a.index(), '1111')
        self.assertEqual(filename(a), 'images/1111.png')
        self.assertEqual(str(a), '[color=ff3333]_!_[/color]')

if __name__ == "__main__":
    unittest.main()
