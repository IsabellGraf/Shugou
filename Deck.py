from __future__ import print_function

from itertools import combinations
from random import sample
from collections import namedtuple
from itertools import product

# Enums for cards. A temporary solution. Should be handled in python3.4 or
# by the enum34 module
ONE, TWO, THREE = NUMBERS = [1, 2, 3]
RED, GREEN, BLUE = COLOURS = [1, 2, 3]
BLANK, STRIPED, FILLED = FILLINGS = [1, 2, 3]
STAR, SQUARE, CIRCLE = SHAPES = [1, 2, 3]
PROPERTIES = [NUMBERS, COLOURS, FILLINGS, SHAPES]

# A simple immutable card class
# Each has three states which takes on values 1,2,3
# Thus, ONE, RED, FILLED, STAR is 1132
# This allows each card to be represented by a unique integer
Card = namedtuple('Card', ['number', 'colour', 'filling', 'shape'])

# We extend the class so that it can fetch its own picture resource.


def index(self):
    ''' card -> int - returns an index base on a card for the purpose of looking up filenames of the associated card'''
    return str(self.number) + str(self.colour) + str(self.filling) + str(self.shape)
Card.index = index


def filename(self):
    ''' Where the file should be stored for the card's image'''
    # This will need to be changed once we have the file structure workedout.
    return "images/" + self.index() + ".png"
Card.filename = filename


class Deck(object):

    '''A deck class that stores all playable cards along with ways of checking properties of subsets of the deck '''

    def __init__(self):
        # a complete set of cards
        self.cards = set()
        for property in product([1, 2, 3], repeat=4):
            card = Card(*property)
            self.cards.add(card)

    @staticmethod
    def allSameOrAllDifferent(*args):
        '''objects -> bool -- Returns True if all the args are different or all the same'''
        return len(set(args)) == 1 or len(set(args)) == len(args)

    @staticmethod
    def checkSet(card1, card2, card3):
        '''(card, card,card) -> bool -- Return true if these three cards form a valid set'''
        return all(Deck.allSameOrAllDifferent(card1[i], card2[i], card3[i]) for i in range(0, 4))

    @staticmethod
    def numberOfSets(cards):
        ''' cards -> int -- Returns the number of sets in a collections of cards '''
        return sum(Deck.checkSet(*c) for c in combinations(cards, 3))

    @staticmethod
    def hasSet(cards):
        ''' list -> bool -- returns true if the cards contains an set'''
        return any(Deck.checkSet(*c) for c in combinations(cards, 3))

    def drawGuarantee(self, othercards=set(), numberofcards=3):
        ''' (list, int) -> list of cards -- Returns a numberofcards cards,
        which will once combined with othercards form a set it or raise an error if impossible'''
        # verify that we have atleast one possible set
        if (len(othercards) + numberofcards < 3) or not Deck.hasSet(othercards | self.cards):
            raise ValueError("Can't form a set")

        newCards = set(sample(self.cards, numberofcards))
        while not Deck.hasSet(newCards | othercards):
            newCards = set(sample(self.cards, numberofcards))
        for card in newCards:
            self.cards.remove(card)
        return newCards

import unittest


class TestDeck(unittest.TestCase):

    def test_deck(self):
        a = Card(ONE, RED, FILLED, STAR)
        b = Card(TWO, RED, FILLED, STAR)
        c = Card(THREE, RED, FILLED, STAR)
        d = Card(THREE, RED, FILLED, CIRCLE)
        e = Card(THREE, RED, FILLED, SQUARE)
        self.assertEqual(Deck.numberOfSets([a, b, c, d, e]), 2)
        self.assertTrue(Deck.hasSet([a, b, c, d, e]))
        self.assertFalse(
            Deck.hasSet(set([Card(number=3, colour=5, filling=8, shape=11), Card(number=2, colour=6, filling=7, shape=12), Card(number=2, colour=6, filling=9, shape=11)])))
        self.assertTrue(Deck.hasSet(set([Card(number=3, colour=5, filling=8, shape=11), Card(number=2, colour=6, filling=7, shape=12), Card(number=2, colour=6, filling=9, shape=11)]) | {a}))

        deck = Deck()
        threeCards = deck.drawGuarantee()
        self.assertTrue(Deck.hasSet(threeCards))
        a = Card(ONE, RED, BLANK, STAR)
        self.assertEqual(a.index(), '1111')
        self.assertRaises(
            ValueError, lambda x: deck.drawGuarantee(numberofcards=x), 0)
if __name__ == "__main__":
    unittest.main()
