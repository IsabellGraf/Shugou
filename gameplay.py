from kivy.properties import *
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from Deck import Deck
from AI import AI

from Rotator import Rotator

import datetime

class SelectPlayersPopup(Popup):

    '''controls the values shown in the player selection popup'''
    playscreen = ObjectProperty()
    def __init__(self, playscreen, **kwards):
        super(SelectPlayersPopup, self).__init__()
        # More UI that I can't quite put in the kv file
        self.playscreen = playscreen
        self.content = GridLayout(cols=2, spacing='10dp')
        self.buttons = [None] * self.playscreen.number_of_players
        for i in range(self.playscreen.number_of_players):
            self.buttons[i] = Button()
            self.buttons[i].text = self.playscreen.name_of_players[i]
            self.buttons[i].value = i
            self.buttons[i].bind(on_press=self.click)
            self.content.add_widget(self.buttons[i])

    def click(self,button):
        self.update_scores(button.value)
        self.dismiss()

    def get_players_name(self, value):
        return self.playscreen.name_of_players[value]

    def update_scores(self, value):
        '''need to other lines to update the score display'''
        self.playscreen.scores_of_players[int(value)] += 1

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

    aiPlayed = BooleanProperty(False)
    aiActivated = BooleanProperty(False)

    def __init__(self,*args, **kwargs):
        super(GamePlayScreen, self).__init__(*args, **kwargs)
        self.rotator = Rotator()
        #self.buttons = self.ids.cards_layout.children
        #print(self.buttons)

    # Dealing with multiplayer ###
    def select_player_popup(self, *args):
        '''called when three cards are selected'''
        popup = SelectPlayersPopup(self)
        
        popup.open()

    def unselectAll(self):
        ''' Unselect all the toggle buttons '''
        for button in self.buttons:
            button.state = 'normal'

    def on_enter(self):
        self.deck = Deck()

        self.buttons = self.ids.cards_layout.children
        for i in range(12):
            self.buttons[i].bind(on_press=self.checkIfSetOnBoard)
        self.setupGame()
        self.updateGrid()
        self.game.active = True
        self.setUpHint()
        self.game.setUpAI()

        self.t0 = datetime.datetime.now()
    def setupGame(self):
        ''' sets up a the deck and draws up some cards'''
        self.cards = self.deck.drawGuarantee(numberofcards=12)
        #self.updateGrid()
        self.ai = AI()

    def checkIfSetOnBoard(self, obj):
        '''Called when a button is pressed, checks if there is a set. If there is one, then refill the display cards'''
        down = self.selected()

        if len(down) == 3:
            if Deck.checkSet(self.cards[down[0]], self.cards[down[1]], self.cards[down[2]]):
                selectedcards = {self.cards[i] for i in down}
                try:
                    newcards = self.deck.drawGuarantee(
                        othercards=set(self.cards) ^ selectedcards, numberofcards=3)
                except ValueError:  # no more sets available
                    self.screens.current = 'screen3'
                    # need to clear the selection
                    self.unselectAll()
                    self.stopRotation()
                    self.setupGame()
                    return
                if self.aiPlayed:
                    self.aiScore += 1
                else:
                    if self.number_of_players > 1:
                        # Load the popup
                        self.select_player_popup()
                    else:
                        self.scores_of_players[0] += 1
                for index, i in enumerate(down):
                    self.cards[i] = newcards[index]
                self.aiUpdates()
                self.aiPlayed = False
                self.updateGrid()
                self.stopRotation()
            else:  # The cards were not a set
                self.unselectAll()
        else:
            self.stopRotation()
            self.setUpHint()

    def updateGrid(self):
        for i, card in enumerate(self.cards):
            self.buttons[i].card = card
            self.buttons[i].state = 'normal'
        self.setUpHint()
        self.t0 = datetime.datetime.now()
        if self.aiActivated:
            self.setUpAI()        


    def aiUpdates(self):
        timeDifference = datetime.datetime.now() - self.t0
        if self.aiActivated:
            if self.aiPlayed:
                self.ai.updateRatingsAI(
                    self.cards, self.aiCards, timeDifference)
            else:
                self.ai.updateRatingsHuman(
                    self.cards, selectedcards, timeDifference)

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