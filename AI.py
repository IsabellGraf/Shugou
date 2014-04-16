import random
from Deck import Deck,Card
    
def AI(table):
    all_sets = Deck.allSets(table)
    set_difficulties = []

    for the_set in all_sets:
        set_difficulties.append(get_difficulties(the_set))

    time,index = get_time(set_difficulties)
    set_cards1, set_cards2, set_cards3 = all_sets[index]

    return time, set_cards1, set_cards2, set_cards3


def get_difficulties(the_set):
#    num_similar = Deck.similarities(the_set[0], the_set[1], the_set[2])
#    difficulty = 4-num_similar
    return ratingList[Deck.setIdentifier(the-set)]
    
    
def get_time(set_difficulties):
    # For a 'normal' table an advanced player needs about 15s, the beginner needs about 120s to find a set.

    the_time = 90
    length = len(set_difficulties)
    index = random.randint(0,length-1)
    difficulty = set_difficulties[index]
    time = the_time - 4*(4-difficulty)*length
    
    return time, index


def demo():
    c1=Card(1,1,1,1)
    c2=Card(2,3,1,2)
    c3=Card(1,2,3,1)
    c4=Card(2,1,3,3)
    c5=Card(1,3,1,1)
    c6=Card(3,2,1,2)
    c7=Card(1,3,2,3)
    c8=Card(2,2,1,3)
    c9=Card(2,1,3,1)
    c10=Card(3,3,2,1)
    c11=Card(3,1,2,1)
    c12=Card(3,1,2,2)
    table=[c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12]    
    time,card1,card2,card3 = AI(table)
    print 'Time when AI reveals set:', time
    print 'AI reveals the set:'
    print card1
    print card2
    print card3

    
def newRatings(winnerRating, loserRating, K = 32):
    '''calculates ratings of winner and loser according to ELO http://en.wikipedia.org/wiki/Elo_rating_system'''
    QWinner = 10**(winnerRating/float(400))
    QLoser = 10**(loserRating/float(400))
    EWinner = QWinner/(QWinner+QLoser)
    ELoser = 1-EWinner
    newWinnerRating = winnerRating + K*(1-EWinner)
    newLoserRating = loserRating + K*(0-ELoser)
    return newWinnerRating, newLoserRating

        
def updateRatings(table, setFound):
    '''updates the ratings of all sets involved in this round
    
    Please call
    >> updateRatings(table, setFound)
    whenever a human finds a set
    '''
    initialRating = 1500 #any number would work, chess uses something like this usually, so why not...
    setFoundKey = Deck.setIdentifier(setFound)
    try:
        setFoundRating = ratingList[setFoundKey]
    except KeyError: #first time this set shows up
        setFoundRating = initialRating
    
    losingSets = Deck.allSets(table)-setFound
    for the_set in losingSets:
        losingSetKey = Deck.setIdentifier(the_set)
        try:
            losingSetRating = ratingList[losingSetKey]
        except KeyError: #first time this set shows up
            losingSetRating = initialRating
        newWinnerRating, newLoserRating = newRatings(setFoundRating, losingSetRating)
        ratingList[setFoundKey] = newWinnerRating
        ratingList[losingSetKey] = newLoserRating
        
# does this update ratingList automatically?
        
    
    
if __name__ == "__main__":
    demo()
