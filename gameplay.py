from kivy.properties import *
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

from Deck import Deck
from AI import AI
from Rotator import Rotator

import datetime

class SelectPlayersPopup(Popup):

    '''controls the values shown in the player selection popup'''

    def __init__(self, playscreen, **kwards):
        super(SelectPlayersPopup, self).__init__()
        # More UI that I can't quite put in the kv file
        self.playscreen = playscreen
        self.content = GridLayout(cols=2, spacing='10dp')
        for i in range(self.playscreen.number_of_players):
            button = Button()
            button.text = self.playscreen.name_of_players[i]
            button.value = i
            button.bind(on_press=self.click)
            self.content.add_widget(button)

    def click(self,button):
        self.playscreen.scores_of_players[int(button.value)] += 1
        self.dismiss()

class CardToggle(ToggleButton):
    card = ObjectProperty()
    angle = NumericProperty(0)

class GamePlayScreen(Screen):
    numberofsets = NumericProperty(0)
    restart = ObjectProperty()
    screenManager = ObjectProperty()
    aiScore = NumericProperty(0)
    
    hintActivated = BooleanProperty(False)
    number_of_players = NumericProperty(1)
    name_of_players = ListProperty(['','','',''])
    scores_of_players = ListProperty([0, 0, 0, 0])

    cards = ListProperty()
    displayHintTimer = NumericProperty(5)

    aiPlayed = BooleanProperty(False)
    aiActivated = BooleanProperty(False)

    active = BooleanProperty(False)

    def __init__(self,*args, **kwargs):
        super(GamePlayScreen, self).__init__(*args, **kwargs)
        self.rotator = Rotator()
        self.ai = AI()

    # Dealing with multiplayer ###
    def select_player_popup(self, *args):
        '''called when three cards are selected'''
        popup = SelectPlayersPopup(self)
        popup.open()

    def on_leave(self):
        self.endscreen = self.game.get_screen('screen3')
        self.endscreen.scores_of_players = self.scores_of_players
        self.endscreen.name_of_players = self.name_of_players
        self.active = False

    def unselectAll(self):
        ''' Unselect all the toggle buttons '''
        for button in self.buttons:
            button.state = 'normal'

    def on_enter(self):
        ''' Sets the game '''
        # You can only enter the game from the intro
        self.deck = Deck()
        self.buttons = self.ids.cards_layout.children
        for i in range(12):
            self.buttons[i].bind(on_press=self.checkIfSetOnBoard)
        self.cards = self.deck.drawGuarantee(numberofcards=12)
        for i in range(len(self.scores_of_players)):
            self.scores_of_players[i] = 0
        self.ai = AI()
        self.game.active = True
        self.newRound()
        self.t0 = datetime.datetime.now()

    def newRound(self):
        ''' What should be done at the begining of every round '''
        self.stopRotation()
        self.updateGrid()
        self.setUpHint()
        self.unselectAll()
        self.setUpAI()        

    def checkIfSetOnBoard(self, obj):
        '''Called when a button is pressed, checks if there is a set. If there is one, then refill the display cards'''
        down = self.selected()
        if not len(down) == 3:
            return

        if Deck.checkSet(self.cards[down[0]], self.cards[down[1]], self.cards[down[2]]):
            selectedcards = {self.cards[i] for i in down}
            try:
                newcards = self.deck.drawGuarantee(
                    othercards=set(self.cards) ^ selectedcards, numberofcards=3)
            except ValueError:  # no more collections available
                self.game.current = 'screen3'
                return
            if self.aiPlayed:
                self.aiScore += 1
                self.aiUpdates()
                self.aiPlayed = False                    
            else:
                if self.number_of_players > 1:
                    self.select_player_popup()
                else:
                    self.scores_of_players[0] += 1
            for index, i in enumerate(down):
                self.cards[i] = newcards[index]
            self.newRound()
        else:  # The cards were not a set
            self.unselectAll()

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
                pass
                # Broken? what does selected stand for?
                #self.ai.updateRatingsHuman(
                #    self.cards, selected, timeDifference)

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

    # Functions related to the AIhint ###
    def setUpAI(self):
        Clock.unschedule(self.AIplay)
        if self.aiActivated:
            pass
            # Broken..?
            #(time, self.aiCards) = self.ai.suggestion(self.cards)
            #Clock.schedule_once(self.AIplay, 1)

    def AIplay(self, *arg):
        ''' The AI plays a turn '''
        for index, card in enumerate(self.cards):
            if card in self.aiCards:
                self.buttons[index].state = 'down'
            else:
                self.buttons[index].state = 'normal'
        # Basic AI animation.
        Clock.schedule_once(lambda x: self.checkIfSetOnBoard(None), 1)
        self.aiPlayed = True

    # Functions related to displaying hint ###
    def on_displayHintTimer(self, obj, value):
        self.setUpHint()

    def setUpHint(self):
        ''' unschedule any current hint and loads up the next one if appropriate'''
        # Need to remove any previous call or else it might be activated too
        # quickly    
        Clock.unschedule(self.displayHint)
        Clock.unschedule(self.displayHintSecond)
        # After some time in seconds show a hint
        if self.hintActivated and self.active:
            self.hint = Deck.hint(self.cards)
            Clock.schedule_once(self.displayHint, self.displayHintTimer)

    def on_hintActivated(self, obj, value):
        # If the hint was turned off, unselect the cards
        if value == False:
            self.stopRotation()

    def displayHint(self, *arg):
        ''' Displays the first card in the hint and sets-up the display of the second card in the hint'''
        if self.selected() == []:  # no cards have been selected
            # displays on the first card in a hint
            buttonToRotate = self.buttonFromCard(self.hint[0])
            self.rotator.rotateThisButton(buttonToRotate)
            Clock.schedule_once(self.displayHintSecond, self.displayHintTimer)
        else:  # if the player has a card selected, try calling it again later
            self.setUpHint()

    def displayHintSecond(self, *arg):
        ''' Displays the second of two cards in a hint'''
        selectedcards = self.selected()
        buttonToRotate = self.buttonFromCard(self.hint[1])
        self.rotator.rotateThisButton(buttonToRotate)

    # Functions to handling the game play screen
    def selected(self):
        '''Returns the indices of all the selected ToggleButton'''
        down = []
        for index, button in enumerate(self.buttons):
            if button.state == 'down':
                down.append(index)
        return down            

    def stopClocks(self):
        Clock.unschedule(self.AIplay)
        Clock.unschedule(self.displayHint)
        Clock.unschedule(self.displayHintSecond)    