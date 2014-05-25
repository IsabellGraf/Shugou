from itertools import combinations
from random import sample
from collections import namedtuple
from itertools import product

# Enums for cards.
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

# We extend the class to help with its representation


def index(self):
    ''' card -> int - returns an index base on a card for
    the purpose of looking up filenames of the associated card'''
    return (str(self.number) + str(self.colour)
            + str(self.filling) + str(self.shape))
Card.index = index


def normalimage(self):
    ''' Where the file should be stored for the card's image'''
    # This will need to be changed once we have the file structure workedout.
    return "images/" + self.index() + ".png"
Card.normalimage = normalimage


def downimage(self):
    ''' Where the file should be stored for the card's image'''
    # This will need to be changed once we have the file structure workedout.
    return "images/" + self.index() + "_down.png"
Card.downimage = downimage


def cardPrint(self):
    ''' Returns a basic formating for a card '''
    shapes = ['!', '@', '#']
    colours = ['ff3333', '3333ff', '33ff33']
    fillings = ['_', '*', '']  # easier to read than bold and italics
    string = shapes[self.shape - 1] * self.number
    string = fillings[self.filling - 1] + string + fillings[
        self.filling - 1] if self.filling != 3 else string
    string = '[color=' + colours[self.colour - 1] + ']' + string + '[/color]'

    return string

Card.__str__ = cardPrint


class Deck(object):

    '''A deck class that stores all playable cards along
    with ways of checking properties of subsets of the deck '''

    def __init__(self):
        # a complete set of cards stored in a set
        # thus, can never be taken out "in order"
        self.fill()

    def fill(self):
        '''Fill the deck with a new sets of cards'''
        self.cards = set()
        for property in product([1, 2, 3], repeat=4):
            card = Card(*property)
            self.cards.add(card)

    @staticmethod
    def allSameOrAllDifferent(*args):
        '''objects -> bool -- Returns True if
        all the args are different or all the same'''
        return len(set(args)) == 1 or len(set(args)) == len(args)

    @staticmethod
    def similarities(*cards):
        ''' cards -> int -- returns the number
        of similarities in the sets of cards'''
        similarities = 0
        for i in range(0, 4):
            similarities += Deck.allSame(*[card[i] for card in cards])
        return similarities

    @staticmethod
    def allSame(*args):
        ''' Helper method to check if all given elements are the same '''
        return len(set(args)) == 1

    @staticmethod
    def allSets(cards):
        ''' Returns all sets in a shugous of cards '''
        return [c for c in combinations(cards, 3) if Deck.checkSet(*c)]

    @staticmethod
    def hint(cards):
        ''' Returns 2 cards that belong to a set amongs
        the cards or returns None if no set is found'''
        return Deck.aSet(cards)[0:2]

    @staticmethod
    def aSet(cards):
        ''' Returns a set of 3 cards or returns None if no set is found'''
        for c in combinations(cards, 3):
            if Deck.checkSet(*c):
                return c

    @staticmethod
    def checkSet(card1, card2, card3):
        '''(card, card,card) -> bool -- Return True if
        these three cards form a valid set'''
        return all(Deck.allSameOrAllDifferent(card1[i], card2[i], card3[i])
                   for i in range(0, 4))

    @staticmethod
    def numberOfSets(cards):
        ''' cards -> int -- Returns the number of sets
        in a shugous of cards '''
        return sum(Deck.checkSet(*c) for c in combinations(cards, 3))

    @staticmethod
    def idOfSet(cards):
        sortedCards = sorted(cards)
        return ''.join([sortedCards[i].index() for i in range(len(cards))])

    @staticmethod
    def hasSet(cards):
        ''' list -> bool -- returns true if the cards contains an set'''
        return any(Deck.checkSet(*c) for c in combinations(cards, 3))

    def __iter__(self):
        for card in self.cards:
            yield card

    def draw(self, numberofcards=12):
        return self.drawGuarantee(numberofcards=12)

    def drawGuarantee(self, othercards=set(), numberofcards=3):
        ''' (list, int) -> list of cards -- Returns a numberofcards cards,
        which will once combined with othercards form a set it or
        raise an error if impossible'''
        # verify that we have atleast one possible set
        if ((len(othercards) + numberofcards < 3) or
                not Deck.hasSet(othercards | self.cards)):
            raise ValueError("No set can be found")
        newCards = set(sample(self.cards, numberofcards))
        while not Deck.hasSet(newCards | othercards):
            newCards = set(sample(self.cards, numberofcards))
        for card in newCards:
            self.cards.remove(card)
        return list(newCards)