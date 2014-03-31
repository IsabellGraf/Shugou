from __future__ import print_function

from itertools import combinations
from random import sample
from collections import namedtuple

'''
Building this class under the assumption that each card is unique in the world
i.e. there won't be more than 81 one cards in existance
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
PROPERTIES = [NUMBERS, COLOURS, FILLINGS, SHAPES]
NUMVISIBLECARDS = 12
NUMCARDS = 81

# A simple immutable card class
Card = namedtuple('Card', ['number', 'colour', 'filling', 'shape'])


def indexFromCard(card):
    ''' card -> int - returns an index base on a card for the purpose of looking up filenames of the associated card'''
    return str(card.number) + str(card.colour) + str(card.filling) + str(card.shape)


def completeSet(card1, card2):
    ''' card, card -> card -- Returns a third card that completes a set'''
    if card1.number == card2.number:
        number = card1.number
    else:
        number = (set(NUMBERS) ^ {card1.number, card2.number}).pop()
    if card1.colour == card2.colour:
        colour = card1.colour
    else:
        colour = (set(COLOURS) ^ {card1.colour, card2.colour}).pop()
    if card1.filling == card2.filling:
        filling = card1.filling
    else:
        filling = (set(FILLINGS) ^ {card1.filling, card2.filling}).pop()
    if card1.shape == card2.shape:
        shape = card1.shape
    else:
        shape = (set(SHAPES) ^ {card1.shape, card2.shape}).pop()

    return Card(number, colour, filling, shape)


class Deck(object):

    '''A deck class that stores all playable cards along with ways of checking properties of subsets of the deck '''

    def __init__(self):
        # a complete set of cards
        self.cards = set()
        for number in PROPERTIES[0]:
            for colour in PROPERTIES[1]:
                for filling in PROPERTIES[2]:
                    for shape in PROPERTIES[3]:
                        card = Card(
                            number=number, colour=colour, filling=filling, shape=shape)
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
        return Deck.numberOfSets(cards) > 0

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
        self.assertEqual(indexFromCard(a), '14910')
        self.assertRaises(
            ValueError, lambda x: deck.drawGuarantee(numberofcards=x), 0)

    def test_card(self):
        a = Card(ONE, RED, FILLED, STAR)
        b = Card(TWO, RED, FILLED, STAR)
        self.assertEqual(completeSet(a, b), Card(THREE, RED, FILLED, STAR))

if __name__ == "__main__":
    unittest.main()
