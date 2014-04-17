
# A sample AI- 1-game

from Deck import *

from AI import AI

cards = [Card(number=1, colour=3, filling=2, shape=1), Card(number=3, colour=3, filling=1, shape=1), Card(number=2, colour=3, filling=3, shape=1), Card(number=3, colour=3, filling=3, shape=1), Card(number=3, colour=2, filling=3, shape=3), Card(number=3, colour=1, filling=2, shape=2), Card(number=1, colour=1, filling=1, shape=2), Card(number=1, colour=2, filling=2, shape=2), Card(number=1, colour=2, filling=1, shape=3), Card(number=3, colour=1, filling=2, shape=1), Card(number=1, colour=2, filling=3, shape=2), Card(number=2, colour=3, filling=3, shape=3)]

allSets = [(Card(number=1, colour=3, filling=2, shape=1), Card(number=3, colour=3, filling=1, shape=1), Card(number=2, colour=3, filling=3, shape=1)), (Card(number=3, colour=3, filling=1, shape=1), Card(number=3, colour=2, filling=3, shape=3), Card(number=3, colour=1, filling=2, shape=2)), (Card(number=2, colour=3, filling=3, shape=1), Card(number=3, colour=1, filling=2, shape=2), Card(number=1, colour=2, filling=1, shape=3))]

playerSet = allSets[0]

AISet = allSets[1]

ai = AI()

for i in range(10):
	ai.updateRatingsHuman(cards,playerSet)
	print(ai.pprint())

ai.updateRatingsAI(cards)

print("Ai")
print(ai.pprint())

print(ai.suggestion(cards))