from __future__ import print_function

from itertools import combinations
from random import sample
'''
Building this class under the assumption that each card is unique in the world
i.e. there won't be more than 81 one cards in existance
'''
'''
TODO: Should the deck behave as some endless source of cards?
Improve the speed of checking if a list of cards contains a set or not (currently slow on my old iPad)

'''
# Constants:
# All constants must be capitalized.
# Its a bit silly to make constants out of 1,2,3 but
# I hope we all understand stylistically why I did this.
# I think theses should typically handled with enums, but there is no
# built in enum classes in python2 (they are available via pip or by
# default in python3)
ONE = 1
TWO = 2
THREE = 3
NUMBERS = [ONE, TWO, THREE]
RED = 4
GREEN = 5
BLUE = 6
COLOURS = [RED, GREEN, BLUE]
BLANK = 7
STRIPED = 8
FILLED = 9
FILLINGS = [BLANK, STRIPED, FILLED]
STAR = 10
SQUARE = 11
CIRCLE = 12
SHAPES = [STAR, SQUARE, CIRCLE]
NUMVISIBLECARDS = 12
NUMCARDS = 81

from collections import namedtuple
Card = namedtuple('Card', ['number', 'colour', 'filling', 'shape'])


def indexFromCard(card):
    ''' card -> int - returns an index base on a card for the purpose of looking up filenames of the associated card'''
    return str(card.number) + str(card.colour) + str(card.filling) + str(card.shape)


class Deck(object):

    '''A deck class that stores all cards and all remaining cards in a game. '''

    def __init__(self):
        # a complete set of cards
        self.cards = set()
        for number in NUMBERS:
            for colour in COLOURS:
                for filling in FILLINGS:
                    for shape in SHAPES:
                        card = Card(
                            number=number, colour=colour, filling=filling, shape=shape)
                        self.cards.add(card)

    @staticmethod
    def allSameOrAllDifferent(*args):
        '''Returns True if all the args are different or all the same'''
        return len(set(args)) == 1 or len(set(args)) == len(args)

    @staticmethod
    def checkSet(card1, card2, card3):
        '''Return true if these cards form a valid set, false otherwise'''
        return all(Deck.allSameOrAllDifferent(card1[i], card2[i], card3[i]) for i in range(0, 4))

    @staticmethod
    def numberOfSets(cards):
        ''' Returns the number of sets in a collections of cards '''
        return sum(Deck.checkSet(*c) for c in combinations(cards, 3))

    @staticmethod
    def hasSet(cards):
        ''' list -> bool -- returns true if the cards contains an set'''
        return Deck.numberOfSets(cards) > 0

    def drawGuarantee(self, othercards, numberofcards=3):
        ''' Returns a number of cards cards, if you pass a list of other cards, it will return a set of cards that form a set along with the cards of othercards (or raise an error if impossible)'''
        print("before picking new cards")
        # verify that we have atleast one possible set
        if not Deck.hasSet(othercards | self.cards) or (len(othercards) + numberofcards < 3):
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

if __name__ == "__main__":
    unittest.main()
