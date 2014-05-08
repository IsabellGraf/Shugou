from __future__ import print_function

import datetime
import pickle

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import *
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from jsonConfig import settingsjson

from gameplay import GamePlayScreen
game = None

class PlayerNamePopup(Popup):

    def __init__(self, value, game):
        super(PlayerNamePopup, self).__init__()
        self.game = game
        self.game.number_of_players = value
        self.game.name_of_players = ['John', 'Sally', 'Sam', 'Joey']
        #Create the screen which allows a user to change names.
        for i in range(self.game.number_of_players):
            button = Button()
            button.text = self.game.name_of_players[i]
            button.value = i
            button.bind(on_press=self.click)
            self.ids.content.add_widget(button)
        
        self.ids.enter.bind(on_press=self.on_press_callback)

    def click(self,button):
        #In here, we create the popup where we request the user's names.
        #On click of the name we want to change, the user can enter a new name.
        i = button.value
        popup = Popup(title="Enter Name here",
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
        self.game.name_of_players[i] = popup.content.children[1].text
        button.text = self.game.name_of_players[i]
        
    def on_press_callback(self, obj):
        self.dismiss()
        self.game.children[0].current = 'screen2'


class TutorialScreen(Screen):
    active = BooleanProperty(False)

class EndGameScreen(Screen):
    name_of_players = ListProperty(['','','',''])
    scores_of_players = ListProperty([0, 0, 0, 0])
    screenManager = ObjectProperty()
    number_of_players = NumericProperty(1)
    game = ObjectProperty()

    def on_enter(self,*args):
        self.name_of_players = [x for y,x in sorted(zip(self.game.scores_of_players,self.game.name_of_players))][::-1]
        self.scores_of_players = sorted(self.game.scores_of_players)[::-1]

class PlayerSection(Button):
    myvalue = NumericProperty(4)

    def __init__(self, **kwargs):
        super(PlayerSection, self).__init__(**kwargs)
        self.size = Window.size[0] // 6, Window.size[1] // 6

class GameLayout(FloatLayout):
    ''' This class manages the movements between the various screen and the sound '''
    
    name_of_players = ListProperty(['Collections found', '', '', ''])
    number_of_players = NumericProperty(1)
    scores_of_players = ListProperty([0, 0, 0, 0])

    # True if there is a game going on
    active = BooleanProperty(False)
    soundActivated = BooleanProperty(False)
    def __init__(self, **kwargs):
        super(GameLayout, self).__init__(**kwargs)
        self.screens = self.ids.screenManager
        self.playscreen = self.screens.get_screen('screen2')
        self.sound = SoundLoader.load('set_song.wav')
        
    # screen play navigation
    def goToIntro(self, *arg):
        self.screens.current = 'screen1'

    def goToGameScreen(self):
        self.screens.current = 'screen2'

    # Dealing with Sound
    def on_soundActivated(self, obj, value):
        ''' Turn the intro song on or off '''
        if value:
            self.sound.loop = True
            self.sound.play()
        else:
            self.sound.stop()

    def player_name_popup(self, numPlayers):
        '''called after selecting number of players'''
        playername = PlayerNamePopup(numPlayers, self)
        playername.open()

    def restart(self):
        '''reset the scores and everything'''
        self.scores_of_players = [0,0,0,0]
        self.aiScore = 0

    def quit(self):
        ''' You are quiting the current game '''
        self.playscreen.unselectAll()
        self.setupGame()
        self.restart()
        self.goToIntro()
        self.playscreen.stopRotation()
        self.active = False

    def goToTutorial(self):
        self.screens.current = 'tutorialFlow'

    def stopClocks(self):
        Clock.unschedule(self.playscreen.AIplay)
        Clock.unschedule(self.playscreen.displayHint)
        Clock.unschedule(self.playscreen.displayHintSecond)

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
        self.gamelayout.playscreen.hintActivated = boolFromJS(
            self.config.get('settings', 'hint'))
        speedSettings = {'slow':10, 'normal':5, 'fast':1}
        self.gamelayout.playscreen.displayHintTimer = speedSettings[
            self.config.get('settings', 'hintspeed')]
        self.gamelayout.soundActivated = boolFromJS(
            self.config.get('settings', 'sound'))
        self.gamelayout.playscreen.aiActivated = boolFromJS(
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
        self.gamelayout.playscreen.setUpHint()
        self.gamelayout.playscreen.setUpAI()

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
