import random
from pickle import load, dump

from Deck import Deck, Card


class AI(object):

    def __init__(self, path):
        self.ratingList = self.loadData()
        self.path = path
        self.time = 45

    def loadData(self):
        try:
            inputFile = open(self.path + 'AIdata.pkl', 'rb')
            data = load(inputFile)
            inputFile.close()
            return data
        except:
            return {}

    def dumpData(self):
        output = open(self.path + 'AIdata.pkl', 'wb')
        dump(self.ratingList, output)
        output.close()

    def reset(self):
        output = open(self.path + 'AIdata.pkl', 'wb')
        dump({}, output)
        output.close()

    def suggestion(self, table):
        all_sets = Deck.allSets(table)
        set_difficulties = []

        for the_set in all_sets:
            set_difficulties.append(self.get_difficulties(the_set))

        time, index = self.get_time(set_difficulties)
        set_cards1, set_cards2, set_cards3 = all_sets[index]

        return time, (set_cards1, set_cards2, set_cards3)

    def get_difficulties(self, the_set):
        try:
            return self.ratingList[Deck.idOfSet(the_set)]
        except KeyError:
            return 1500

    def get_time(self, set_difficulties):
        #        the_time = 90
        length = len(set_difficulties)
        index = random.randint(0, length-1)
        #        difficulty = set_difficulties[index]
        #        time = the_time - 4*(4-difficulty)*length
        return self.time, index

    def newRatings(self, winnerRating, loserRating, K=32):
        '''calculates ratings of winner and loser according to ELO
        http://en.wikipedia.org/wiki/Elo_rating_system'''
        QWinner = 10**(winnerRating/float(400))
        QLoser = 10**(loserRating/float(400))
        EWinner = QWinner/(QWinner+QLoser)
        ELoser = 1-EWinner
        newWinnerRating = winnerRating + K*(1-EWinner)
        newLoserRating = loserRating + K*(0-ELoser)
        return newWinnerRating, newLoserRating

    def updateRatingsAI(self, table, setFound, the_time):
        '''AI was faster, so all sets involved are actually harder
        than we thought, ie increase their rating
        Please call whenever an AI finds a set
        '''

        allSets = Deck.allSets(table)
        for the_set in allSets:
            try:
                self.ratingList[Deck.idOfSet(the_set)] += 50
            except:
                self.ratingList[Deck.idOfSet(the_set)] = 1550
        self.dumpData()

    def updateRatingsHuman(self, table, setFound, the_time):
        '''updates the ratings of all sets involved in this round
        Please call whenever a human finds a set
        '''
        initialRating = 1500
        setFoundKey = Deck.idOfSet(setFound)
        try:
            setFoundRating = self.ratingList[setFoundKey]
        except KeyError:  # first time this set shows up
            setFoundRating = initialRating

        losingSets = set(Deck.allSets(table)) - set(setFound)
        for the_set in losingSets:
            losingSetKey = Deck.idOfSet(the_set)
            try:
                losingSetRating = self.ratingList[losingSetKey]
            except KeyError:  # first time this set shows up
                losingSetRating = initialRating
            newWinnerRating, newLoserRating = self.newRatings(setFoundRating,
                                                              losingSetRating)
            self.ratingList[setFoundKey] = newWinnerRating
            self.ratingList[losingSetKey] = newLoserRating
        self.dumpData()

    def pprint(self):
        return [(key, self.ratingList[key]) for
                key in self.ratingList if self.ratingList[key] != 1500]

if __name__ == "__main__":
    demo()
