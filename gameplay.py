from kivy.properties import *
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from Deck import Deck

from Rotator import Rotator

class GamePlayScreen(Screen):
    numberofsets = NumericProperty(0)
    restart = ObjectProperty()
    screenManager = ObjectProperty()
    aiScore = StringProperty(0)
    
    hintActivated = BooleanProperty(False)
    number_of_players = NumericProperty(1)
    name_of_players = ListProperty(['','','',''])
    scores_of_players = ListProperty([0, 0, 0, 0])

    cards = ListProperty()
    displayHintTimer = NumericProperty(5)
    def __init__(self,*args, **kwargs):
        super(GamePlayScreen, self).__init__(*args, **kwargs)
        self.rotator = Rotator()
        #self.buttons = self.ids.cards_layout.children
        #print(self.buttons)

    def on_enter(self):
        self.buttons = self.ids.cards_layout.children
        self.updateGrid()
        self.game.active = True
        self.setUpHint()
        self.game.setUpAI()

    def updateGrid(self):
        for i, card in enumerate(self.cards):
            self.buttons[i].card = card
            self.buttons[i].state = 'normal'
        self.setUpHint()
        #self.t0 = datetime.datetime.now()
        #if self.aiActivated:
        #    self.setUpAI()        


    def stopRotation(self):
        self.rotator.endRotate()

    def selected(self):
        '''Returns the indices of all the selected ToggleButton'''
        down = []
        for index, button in enumerate(self.buttons):
            if button.state == 'down':
                down.append(index)
        return down

    def buttonFromCard(self, card):
        ''' Returns the instance of the button that contains the given card'''
        for button in self.buttons:
            if button.card == card:
                return button

    def selectCards(self, cards):
        ''' selects the given cards if they are in the given cards '''
        for index, button in enumerate(self.buttons):
            if self.cards[index] in cards:
                button.state = 'down'

    def setUpHint(self):
        ''' unschedule any current hint and loads up the next one if appropriate'''
        # Need to remove any previous call or else it might be activated too
        # quickly    
        Clock.unschedule(self.displayHint)
        Clock.unschedule(self.displayHintSecond)
        print("setUpHint called")
        # After some time in seconds show a hint
        if self.hintActivated:
            self.hint = Deck.hint(self.cards)
            Clock.schedule_once(self.displayHint, self.displayHintTimer)

    def displayHint(self, *arg):
        ''' Displays the first card in the hint and sets-up the display of the second card in the hint'''

        print("displayHint called")
        if self.selected() == []:  # no cards have been selected
            # displays on the first card in a hint
            buttonToRotate = self.buttonFromCard(self.hint[0])
            self.rotator.rotateThisButton(buttonToRotate)
            self.selectCards([self.hint[0]])
            Clock.schedule_once(self.displayHintSecond, self.displayHintTimer)
        else:  # if the player has a card selected, try calling it again later
            self.setUpHint()

    def displayHintSecond(self, *arg):
        ''' Displays the second of two cards in a hint if the current selected card is the first card of the hint'''
        selectedcards = self.selected()
        # One card is selected and it is a specific card.
        if len(selectedcards) == 1 and self.buttons[selectedcards[0]].card == self.hint[0]:
            self.selectCards([self.hint[1]])
            buttonToRotate = self.buttonFromCard(self.hint[1])
            self.rotator.rotateThisButton(buttonToRotate)