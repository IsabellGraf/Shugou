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
from kivy.uix.gridlayout import GridLayout
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.boxlayout import BoxLayout

from Deck import Deck
from AI import AI
from jsonConfig import settingsjson

game = None

'''initialize the score of players to 0'''

class SelectPlayersPopup(Popup):

    '''controls the values shown in the player selection popup'''

    def __init__(self, **kwards):
        super(SelectPlayersPopup, self).__init__()
        # More UI that I can't quite put in the kv file
        self.content = GridLayout(cols=2, spacing='10dp')
        self.buttons = [None] * number_of_players
        for i in range(number_of_players):
            self.buttons[i] = Button()
            self.buttons[i].text = game.name_of_players[i]
            self.buttons[i].value = i
            self.buttons[i].bind(on_press=self.click)
            self.content.add_widget(self.buttons[i])

    def click(self,button):
        self.update_scores(button.value)
        self.dismiss()

    def get_players_name(self, value):
        return name_of_players[value]

    def update_scores(self, value):
        '''need to other lines to update the score display'''
        print(value)
        game.scores_of_players[int(value)] += 1

class PlayerNamePopup(Popup):

    def __init__(self, value):
        super(PlayerNamePopup, self).__init__()
        self.text_inputs = [0]*value
        self.number_of_players = value
        game.number_of_players = value
        game.name_of_players = ['John', 'Sally', 'Sam', 'Joey']

        #Create the screen which allows a user to change names.
        self.content = GridLayout(cols=2, spacing='10dp')
        self.buttons = [None] * number_of_players
        for i in range(number_of_players):
            self.buttons[i] = Button()
            self.buttons[i].text = game.name_of_players[i]
            self.buttons[i].value = i
            self.buttons[i].bind(on_press=self.click)
            self.content.add_widget(self.buttons[i])
            
        self.enter = Button(text='Start Game', size_hint_y=None, height='40dp')

        self.enter.bind(on_press=self.on_press_callback)
        self.children[0].add_widget(self.enter)

    def click(self,button):
        #In here, we create the popup where we request the user's names.
        #On click of the name we want to change, the user can enter a new name.
        i = button.value
        popup = Popup(title="Enter text here",
              size_hint=(0.25, 0.25),
              on_dismiss=lambda x: self.set_caption(x,i,button))
        box = GridLayout(cols=1)
        box.add_widget(TextInput(focus=True,text=button.text))
        box.children[0].select_all()
        box.add_widget(Button(text="Enter Name",on_press = popup.dismiss) )
        popup.content = box
        popup.open()


    def set_caption(self, popup,i,button):
        #Set the name in the name_of_players array.
        game.name_of_players[i] = popup.content.children[1].text
        button.text = game.name_of_players[i]
        

    def on_press_callback(self, obj):
        self.dismiss()
        game.children[0].current = 'screen2'

class GamePlayScreen(Screen):
    numberofsets = NumericProperty(0)
    score_display = StringProperty('')
    restart = ObjectProperty()
    screenManager = ObjectProperty()
    aiScore = StringProperty(0)
    
    number_of_players = NumericProperty(1)
    name_of_players = ListProperty(['','','',''])
    scores_of_players = ListProperty([0, 0, 0, 0])

    def on_enter(self):
        game.active = True
        game.setUpHint()
        game.setUpAI()

class TutorialScreen(Screen):
    active = BooleanProperty(False)
    pass

class EndGameScreen(Screen):
    name_of_players = ListProperty(['','','',''])
    scores_of_players = ListProperty([0, 0, 0, 0])
    screenManager = ObjectProperty()
    number_of_players = NumericProperty(1)

    def on_enter(self,*args):
        print('gameover')
        self.name_of_players = [x for y,x in sorted(zip(game.scores_of_players,game.name_of_players))][::-1]
        self.scores_of_players = sorted(game.scores_of_players)[::-1]


class Scores(Label):
    pass

class PlayerSection(Button):
    myvalue = NumericProperty(4)

    def __init__(self, **kwargs):
        super(PlayerSection, self).__init__(**kwargs)
        self.size = Window.size[0] // 6, Window.size[1] // 6


global current_angle
current_angle = 0

class Rotator(object):
    ''' A class that handles the rotation of buttons '''
    def __init__(self):
        self.angle = 0
        self.buttons = []

    def rotateThisButton(self, button):
        ''' Starts rotating the given button '''

        self.buttons.append(button)
        # It is already rotating
        if len(self.buttons) > 1:
            self.buttons[-1].angle = self.angle
        else:
            Clock.schedule_interval(self.rotateLeft,0.05)

    def rotateLeft(self, dt):
        if self.angle < 8:
            self.angle += 0.5
        for button in self.buttons:
            button.angle = self.angle
        if self.angle == 8:
            Clock.unschedule(self.rotateLeft)
            Clock.schedule_interval(self.rotateRight,0.05)

    def rotateRight(self, dt):
        if self.angle > -8:
            self.angle -= 0.5
        for button in self.buttons:
            button.angle = self.angle
        if self.angle == -8:
            Clock.unschedule(self.rotateRight)
            Clock.schedule_interval(self.rotateLeft,0.05)

    def endRotate(self):
        Clock.unschedule(self.rotateRight)
        Clock.unschedule(self.rotateLeft)
        for button in self.buttons:
            # The bizarre way to get the angles back to 0
            while button.angle != 0:
                if button.angle > 0:
                    button.angle -= 0.5
                else:
                    button.angle += 0.5
        self.buttons = []

class CardToggle(ToggleButton):
    card = ObjectProperty()
    angle = NumericProperty(0)

class GameLayout(FloatLayout):
    score = NumericProperty(0)
    number_of_players = NumericProperty(1)
    score_display = StringProperty('')
    playersScores = ListProperty([0,0,0,0])
    soundActivated = BooleanProperty(False)

    hintActivated = BooleanProperty(False)
    displayHintTimer = NumericProperty(5)
    
    # A variable that keeps tracked when an AI has played or not
    aiPlayed = BooleanProperty(False)
    aiActivated = BooleanProperty(False)
    aiScore = NumericProperty(0)

    deck = ObjectProperty()
    cards = ListProperty([])

    name_of_players = ListProperty(['Collections found', '', '', ''])
    number_of_players = NumericProperty(1)
    scores_of_players = ListProperty([0, 0, 0, 0])

    # True if there is a game going on
    active = BooleanProperty(False)
    def __init__(self, **kwargs):
        super(GameLayout, self).__init__(**kwargs)
        global game
        game = self

        self.screens = self.ids.screenManager
        # The UI element we were not able to add to collections.kv
        self.createGrid()
        self.setupGame()
        self.sound = SoundLoader.load('set_song.wav')
        self.rotator = Rotator()

    # screen play navigation
    def goToIntro(self, *arg):
        self.screens.current = 'screen1'

    def goToGameScreen(self):
        self.screens.current = 'screen2'

    def setupGame(self):
        ''' sets up a the deck and draws up some cards'''
        self.deck = Deck()
        self.cards = self.deck.drawGuarantee(numberofcards=12)
        self.updateGrid()
        self.ai = AI()

    def createGrid(self):
        ''' Create the grid of the 12 card buttons, should only be called once'''
        playscreen = self.screens.get_screen('screen2')
        self.buttons = playscreen.ids.cards_layout.children
        # couldn't pass this on_press to the kv file.. no idea why
        for i in range(12):
            self.buttons[i].bind(on_press=self.checkIfSetOnBoard)

    def updateGrid(self):
        '''Updates the cards being displayed and updates hints/ai/numberofsets'''
        for i, card in enumerate(self.cards):
            self.buttons[i].card = card
            self.buttons[i].state = 'normal'
        self.setUpHint()
        self.t0 = datetime.datetime.now()
        if self.aiActivated:
            self.setUpAI()

    # Dealing with Sound
    def on_soundActivated(self, obj, value):
        ''' Turn the intro song on or off '''
        if value:
            self.sound.loop = True
            self.sound.play()
        else:
            self.sound.stop()

    # Functions related to the AIhint ###
    def setUpAI(self):
        Clock.unschedule(self.AIplay)
        if self.aiActivated and self.screens.current == 'screen2':
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

    def aiUpdates(self):
        timeDifference = datetime.datetime.now() - self.t0
        if self.aiActivated:
            if self.aiPlayed:
                self.ai.updateRatingsAI(
                    self.cards, self.aiCards, timeDifference)
            else:
                self.ai.updateRatingsHuman(
                    self.cards, selectedcards, timeDifference)

    # Functions related to displaying hint ###
    def on_displayHintTimer(self, obj, value):
        if self.screens.current == 'screen2':
            self.setUpHint()

    def setUpHint(self):
        ''' unschedule any current hint and loads up the next one if appropriate'''
        # Need to remove any previous call or else it might be activated too
        # quickly
        Clock.unschedule(self.displayHint)
        Clock.unschedule(self.displayHintSecond)
        # After some time in seconds show a hint
        if self.hintActivated and self.screens.current == 'screen2':
            self.hint = Deck.hint(self.cards)
            Clock.schedule_once(self.displayHint, self.displayHintTimer)

    def displayHint(self, *arg):
        ''' Displays the first card in the hint and sets-up the display of the second card in the hint'''
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

    # Functions to handling the game play screen
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

    def unselectAll(self):
        ''' Unselect all the toggle buttons '''
        for button in self.buttons:
            button.state = 'normal'

    def selectCards(self, cards):
        ''' selects the given cards if they are in the given cards '''
        for index, button in enumerate(self.buttons):
            if self.cards[index] in cards:
                button.state = 'down'

    def rotateCards(self, cards):
        ''' selects the given cards if they are in the given cards '''
        for index, button in enumerate(self.buttons):
            if self.cards[index] in cards:
                button.rotate()

    def stopRotation(self):
        self.rotator.endRotate()

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
                    if number_of_players > 1:
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

    # Dealing with multiplayer ###
    def select_player_popup(self, *args):
        '''called when three cards are selected'''
        popup = SelectPlayersPopup()
        popup.open()

    def set_players(self, value):
        '''set the number of players according to user's choice on the front page'''
        global number_of_players
        number_of_players = value

    def player_name_popup(self, numPlayers):
        '''called after selecting number of players'''
        playername = PlayerNamePopup(numPlayers)
        playername.open()

    def restart(self):
        '''reset the scores and everything'''
        global player_scores
        self.score_display = ''
        self.score = 0
        self.scores_of_players = [0,0,0,0]
        self.aiScore = 0

    def quit(self):
        ''' You are quiting the current game '''
        self.unselectAll()
        self.setupGame()
        self.restart()
        self.goToIntro()
        self.stopRotation()
        self.active = False

    def goToTutorial(self):
        self.screens.current = 'tutorialFlow'

    def stopClocks(self):
        Clock.unschedule(self.AIplay)
        Clock.unschedule(self.displayHint)
        Clock.unschedule(self.displayHintSecond)

def boolFromJS(value):
    ''' JSON config returns '1' and '0' for True and False'''
    return True if value == '1' else False


class CollectionApp(App):
    active = BooleanProperty(False)

    def build(self):
        Clock.max_iteration = 50
        # The following line will be uncommented in the beta
        # For now, it gives us access to various kivy settings we can play with
        self.use_kivy_settings = False
        self.gamelayout = GameLayout()
        self.settings_cls = SettingsWithSidebar
        self.loadSettings()
        self.gamelayout.bind(active=self.changeActive)
        return self.gamelayout

    def changeActive(self,instance,value):
        # This doesn't work.. crashes if the build_settings wasn't launched first
        #self.quitButton.disabled = not self.gamelayout.active
        pass


    def loadSettings(self):
        # Load the values already stored into the file
        self.gamelayout.hintActivated = boolFromJS(
            self.config.get('settings', 'hint'))
        speedSettings = {'slow':10, 'normal':5, 'fast':1}
        self.gamelayout.displayHintTimer = speedSettings[
            self.config.get('settings', 'hintspeed')]
        self.gamelayout.soundActivated = boolFromJS(
            self.config.get('settings', 'sound'))
        self.gamelayout.aiActivated = boolFromJS(
            self.config.get('settings', 'ai'))

    def build_config(self, config):
        config.setdefaults('settings', {'hint': True, 
                                        'sound': False,
                                        'ai': False, 
                                        'hintspeed': 'fast'})

    def build_settings(self, settings):
        print(settings)
        self.settings = settings
        settings.add_json_panel('Settings', self.config, data=settingsjson)
        settingsCloseButton = settings.interface.ids.menu.ids.button
        self.settingsCloseButton = settingsCloseButton
        settingsCloseButton.on_press = self.leaveSettingsPanel
        settings.interface.ids.menu.add_widget(Button(text="Tutorial",
                                                      size_hint = (None, None),
                                                      x= settingsCloseButton.x,
                                                      y = settingsCloseButton.top + 10,
                                                      size = settingsCloseButton.size, 
                                                      on_press= self.moveToTutorial))

        self.quitButton = Button(text="Quit Current Game",
                              background_color = [1,0,0,1],
                              size_hint = (None, None),
                              x= settingsCloseButton.x,
                              y = settingsCloseButton.top + settingsCloseButton.height + 20,
                              size = settingsCloseButton.size,
                              disabled = False,
                              on_press= self.quit)   

        settings.interface.ids.menu.add_widget(self.quitButton)
        settings.on_close = self.quit

    def quit(self, *arg):
        self.gamelayout.quit()
        self.settingsCloseButton.trigger_action()

    def moveToTutorial(self, buttonInstance):
        self.gamelayout.goToTutorial()
        self.settingsCloseButton.trigger_action()

    def leaveSettingsPanel(self, *arg):       
        ''' activated when you exit the setting panels'''
        self.gamelayout.setUpHint()
        self.gamelayout.setUpAI()

    def on_config_change(self, config, section, key, value):
        if key == 'hint':
            self.gamelayout.hintActivated = boolFromJS(value)
        if key == 'sound':
            self.gamelayout.soundActivated = boolFromJS(value)
        if key == 'hintspeed':
            speedSettings = {'slow':10, 'normal':5, 'fast':1}
            self.gamelayout.displayHintTimer = speedSettings[value]
        if key == 'ai':
            self.gamelayout.aiActivated = boolFromJS(value)

# To test the screen size you can use:
# kivy main.py -m screen:ipad3

if __name__ == '__main__':
    CollectionApp().run()
