from __future__ import print_function

import datetime
import pickle

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
from kivy.core.audio import SoundLoader
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen


from Deck import Deck
from AI import AI


number_of_players = 4
name_of_players = ['John', 'Sally', 'Sam', 'Joey']
game = None

'''initialize the score of players to 0'''
player_scores = dict.fromkeys(name_of_players, 0)


class SelectPlayersPopup(Popup):

    '''controls the values shown in the player selection popup'''

    def __init__(self, **kwards):
        super(SelectPlayersPopup, self).__init__()
        test = Builder.load_string('''Button:
    x: 50
    y: 100
    text: "hey"''')
        self.children[0].add_widget(test)

    def get_players_name(self, value):
        return name_of_players[value]

    def update_scores(self, value):
        '''need to other lines to update the score display'''
        player_scores[name_of_players[value]] += 1
        game.print_scores(len(name_of_players))

class PlayerNamePopup(Popup):
    def __init__(self,value):
        super(PlayerNamePopup, self).__init__()
        for i in range(value):
            self.text_input = TextInput(multiline=False, size_hint_y = None, size_hint_x = 0.5, height = '32dp', text = name_of_players[i])
            self.children[0].add_widget(self.text_input)
        self.enter = Button(text = 'Start Game', size_hint_y = None, height = '40dp')
        self.enter.bind(on_press = self.on_press_callback)
        self.children[0].add_widget(self.enter)

    def on_press_callback(self,obj):
        self.dismiss()
        game.children[0].current = 'screen2'
        if game.aiActivated:
            game.setUpAI()

class GamePlayScreen(Screen):
    numberofsets = NumericProperty(0)
    score_display = StringProperty('')
    restart = ObjectProperty()
    _screen_manager = ObjectProperty()
    test = ObjectProperty()
    aiScore = StringProperty(0)

class TutorialScreen(Screen):
    pass

class PlayerSection(Button):
    myvalue = NumericProperty(4)
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
    numberofsets = NumericProperty(0)
    number_of_players = NumericProperty(1)
    score_display = StringProperty('')
    hintActivated = BooleanProperty(False)
    aiActivated = BooleanProperty(False)
    soundActivated = BooleanProperty(False)
    displayHintTimer = NumericProperty(5)
    aiScore = NumericProperty(0)
    # A variable that keeps tracked when an AI has played
    aiPlayed = BooleanProperty(False)
    def goBackToIntro(self,*arg):
        self.children[0].current = 'screen1'
        self.restart()
        
    def __init__(self, **kwargs):
        global game
        game = self
        super(GameLayout, self).__init__(**kwargs)

        self.createGrid()
        self.setupGame()        
        self.ai = AI()
        self.sound = SoundLoader.load('set_song.wav')
        self.loadConfigurations()

    def loadConfigurations(self):
        try:
            with open('config.pkl', 'rb') as config:
                d = pickle.load(config)
        except IOError:  # File has not been created
            d = {'hintActivated': True, 'aiActivated':
                 False, 'soundActivated': False}
        
        self.hintActivated = d['hintActivated']
        self.aiActivated = d['aiActivated']
        self.soundActivated = d['soundActivated']


    def on_hintActivated(self,*arg):
        self.setUpHint()
        self.ids.hint.state = 'down'
        self.saveConfigurations()

    def saveConfigurations(self):
        d = {'hintActivated': self.hintActivated, 'aiActivated': self.aiActivated, 'soundActivated': self.soundActivated}
        pickle.dump(d, open('config.pkl', "wb"))

    def setupGame(self):
        ''' sets up a the deck and draws up some cards'''
        self.deck = Deck()
        self.cards = self.deck.drawGuarantee(numberofcards=12)
        self.updateGrid()

    def createGrid(self):
        ''' Create the grid of the 12 card buttons, should only be called once'''
        playscreen = self.children[0].get_screen('screen2')
        self.buttons = [None] * 12
        for i in range(12):
            self.buttons[i] = MyToggleButton()
            self.buttons[i].bind(on_press=self.checkIfSetOnBoard)
            playscreen.children[0].add_widget(self.buttons[i])

    def loadSound(self,obj):
        ''' Turn the intro song on or off '''
        if obj.state == 'down':
            self.sound.loop = True
            self.sound.play()
        else:
            self.sound.stop()
    
    def updateGrid(self):
        '''Updates the cards being displayed and updates hints/ai/numberofsets'''
        if self.hintActivated:
            # remove any display of a hint since the card have changed
            Clock.unschedule(self.displayHint)
            Clock.unschedule(self.displayHintSecond)
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
        # Need to remove any previous call or else it might be activated too quickly
        Clock.unschedule(self.displayHint)
        self.hint = Deck.hint(self.cards)
        # After some time in seconds show a hint
        Clock.schedule_once(self.displayHint, self.displayHintTimer)

    def setUpAI(self):
        (time, self.aiCards) = self.ai.suggestion(self.cards)
        Clock.schedule_once(self.AIplay, 1)

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

    def selectCards(self,cards):
        ''' selects the given cards if they are in the given cards '''
        for index, button in enumerate(self.buttons):
            if self.cards[index] in cards:
                button.state = 'down'  

    def displayHint(self, *arg):
        ''' Displays the first card in the hint and sets-up the display of the second card in the hint'''
        # in case hint was turned off, after the clock element was launched
        # so we are required to verify if we actually still want to run
        if self.hintActivated:
            if self.selected() == []: # no cards have been selected
                # displays on the first card in a hint
                self.selectCards([self.hint[0]])
                Clock.schedule_once(self.displayHintSecond, 5)
            else: # if the player has a card selected, try calling it again later
                self.setUpHint()

    def displayHintSecond(self,*arg):
        ''' Displays the second of two cards in a hint if the current selected card is the first card of the hint'''
        selectedcards = self.selected()
        # One card is selected and it is a specific card.
        if len(selectedcards) == 1 and self.buttons[selectedcards[0]].card == self.hint[0]:
            self.selectCards([self.hint[1]])

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
                try:
                    newcards = self.deck.drawGuarantee(
                        othercards=set(self.cards) ^ selectedcards, numberofcards=3)
                except ValueError: # no more sets available
                    self.children[0].current = 'screen3'
                    # need to clear the selection
                    self.unselectAll() 
                    self.setupGame()
                    return
                if self.aiPlayed:
                    self.aiScore += 1
                else:
                    if number_of_players > 1:
                        # Load the popup
                        self.select_player_popup()
                    else:
                        self.score += 1
                        self.print_scores(number_of_players)
                for index, i in enumerate(down):
                    self.cards[i] = newcards[index]
                self.aiUpdates()
                self.aiPlayed = False
                self.updateGrid()
            else: # The cards were not a set
                self.unselectAll()
        else:
            self.setUpHint()

    def aiUpdates(self):
        timeDifference = datetime.datetime.now() - self.t0
        if self.aiActivated:
            if self.aiPlayed:
                self.ai.updateRatingsAI(
                    self.cards, self.aiCards, timeDifference)
            else:
                self.ai.updateRatingsHuman(
                    self.cards, selectedcards, timeDifference)

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


    def player_name_popup(self,value):
        '''called after selecting number of players'''
        playername = PlayerNamePopup(value)
        playername.open()

    def restart(self):
        '''reset the scores and everything'''
        global player_scores
        self.score_display = ''
        self.score = 0
        player_scores = dict.fromkeys(name_of_players, 0)
        self.print_scores(len(name_of_players))



# To test the screen size you can use:
# kivy main.py -m screen:ipad3

class ScreenApp(App):

    def build(self):
        return GameLayout()

if __name__ == '__main__':
    ScreenApp().run()
