from __future__ import print_function

import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import *
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.popup import Popup

from Deck import Deck
from AI import AI


number_of_players = 4
name_of_players = ['John', 'Sally', 'Sam', 'Joey']


'''initialize the score of players to 0'''
player_scores = dict.fromkeys(name_of_players, 0)


class SelectPlayersPopup(Popup):

    '''controls the values shown in the player selection popup'''

    def get_players_name(self, value):
        return name_of_players[value]

    def update_scores(self, value):
        '''need to other lines to update the score display'''
        player_scores[name_of_players[value]] += 1


class PlayerSection(Button):

    def __init__(self, **kwargs):
        super(PlayerSection, self).__init__(**kwargs)
        self.size = Window.size[0] // 6, Window.size[1] // 6


class MyToggleButton(ToggleButton):
    normalimage = StringProperty('')
    downimage = StringProperty('')
    card = ObjectProperty()

    def on_card(self, instance, value):
        self.card = value
        self.normalimage = self.card.normalimage()
        self.downimage = self.card.downimage()


class GameLayout(FloatLayout):
    score = NumericProperty(0)
    scores = StringProperty('')
    numberofsets = NumericProperty(0)
    number_of_players = NumericProperty(1)
    score_display = StringProperty('')
    hintActivated = BooleanProperty(False)
    aiActivated = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(GameLayout, self).__init__(**kwargs)

        self.deck = Deck()
        self.cards = self.deck.drawGuarantee(numberofcards=12)

        self.ai = AI()

        playscreen = self.children[0].get_screen('screen2')
        self.buttons = [None] * 12
        for i in range(12):
            self.buttons[i] = MyToggleButton()
            self.buttons[i].bind(on_press=self.checkIfSetOnBoard)
            playscreen.children[0].add_widget(self.buttons[i])

        self.updateGrid()

    def updateGrid(self):
        '''Updates the cards being displayed and updates hints/ai/numberofsets'''

        self.numberofsets = self.deck.numberOfSets(self.cards)
        for i, card in enumerate(self.cards):
            self.buttons[i].card = card
            self.buttons[i].state = 'normal'
        self.t0 = datetime.datetime.now()
        if self.hintActivated:
            self.setUpHint()
        if self.aiActivated:
            self.setUpAI()

    def loadHint(self, obj):
        ''' Turns on or off the hint property base on user call'''
        if obj.state == 'down':
            self.hintActivated = True
            self.setUpHint()
        else:
            self.hintActivated = False

    def loadAi(self, obj):
        ''' Turns on or off the hint property base on user call'''
        if obj.state == 'down':
            self.aiActivated = True
            self.setUpAI()
        else:
            self.aiActivated = False

    def setUpHint(self):
        '''Set-up which cards will be part of the hint and a timer for when they will be displayed'''
        self.hint = Deck.hint(self.cards)
        # After some time in seconds show a hint
        Clock.schedule_once(self.displayHint, 5)

    def setUpAI(self):
        (time, self.aiCards) = self.ai.suggestion(self.cards)
        Clock.schedule_once(self.AIplay, 6)

    def AIplay(self, *arg):
        for index, card in enumerate(self.cards):
            if card in self.aiCards:
                self.buttons[index].state = 'down'
            else:
                self.buttons[index].state = 'normal'
        # Basic AI animation.
        Clock.schedule_once(lambda x: self.checkIfSetOnBoard(None), 3)
        self.AIplayed = True

    def displayHint(self, *arg):
        for index, button in enumerate(self.buttons):
            if self.cards[index] in self.hint:
                button.state = 'down'
            else:
                button.state = 'normal'

    def selected(self):
        '''Returns the indices of all the selected ToggleButton'''
        down = []
        for index, button in enumerate(self.buttons):
            if button.state == 'down':
                down.append(index)
        return down

    def unselectAll(self):
        ''' Unselect all the toggle buttons '''
        for button in self.buttons:
            button.state = 'normal'

    def checkIfSetOnBoard(self, obj):
        '''Called when a button is pressed, checks if there is a set. If there is one, then refill the display cards'''
        down = self.selected()

        if len(down) == 3:
            if Deck.checkSet(self.cards[down[0]], self.cards[down[1]], self.cards[down[2]]):
                selectedcards = {self.cards[i] for i in down}
                newcards = self.deck.drawGuarantee(
                    othercards=set(self.cards) ^ selectedcards, numberofcards=3)
                if newcards is False:
                    self.children[0].current = 'screen3'
                else:
                    if number_of_players > 1:
                        # Load the popup
                        self.select_player_popup()
                    else:
                        self.score += 1
                        self.print_scores(number_of_players)
                    for index, i in enumerate(down):
                        self.cards[i] = newcards[index]
                    self.setUpHint()
                timeDifference = datetime.datetime.now() - self.t0

                if self.aiActivated:
                    if self.AIplayed:
                        self.ai.updateRatingsAI(
                            self.cards, self.aiCards, timeDifference)
                    else:
                        self.ai.updateRatingsHuman(
                            self.cards, selectedcards, timeDifference)
                self.updateGrid()
            else:
                self.unselectAll()

    def state_callback(self, obj, value):
        pass

    def select_player_popup(self, *args):
        '''called when three cards are selected'''
        popup = SelectPlayersPopup()
        popup.open()

    def set_players(self, value):
        '''set the number of players according to user's choice on the front page'''
        global number_of_players
        number_of_players = value
        self.print_scores(value)

    def print_scores(self, value):
        '''generate strings for scores display'''
        if value == 1:
            self.score_display = "score " + str(self.score)
        else:
            self.score_display = ''
            for name in name_of_players:
                self.score_display += name + '      ' + \
                    str(player_scores[name]) + '      '


# To test the screen size you can use:
# kivy main.py -m screen:ipad3

class ScreenApp(App):

    def build(self):
        return GameLayout()

if __name__ == '__main__':
    ScreenApp().run()
