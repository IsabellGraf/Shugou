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
    num_similar = Deck.similarities(the_set[0], the_set[1], the_set[2])
    difficulty = 4-num_similar
    return difficulty
    
    
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

if __name__ == "__main__":
    demo()
