from kivy.app import App
from kivy.properties import *
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.settings import SettingsWithSidebar
from kivy.metrics import dp
from jsonConfig import settingsjson
import datetime
import pickle

from gameplay import GamePlayScreen
from PlayerNamePopup import PlayerNamePopup

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

class GameLayout(ScreenManager):
    ''' This class manages the movements between the various screen and the sound '''
    
    name_of_players = ListProperty(['Collections found', '', '', ''])
    number_of_players = NumericProperty(1)
    scores_of_players = ListProperty([0, 0, 0, 0])

    # True if there is a game going on
    active = BooleanProperty(False)
    soundActivated = BooleanProperty(False)
    def __init__(self, **kwargs):
        super(GameLayout, self).__init__(**kwargs)
        self.playscreen = self.get_screen('screen2')
        self.sound = SoundLoader.load('set_song.wav')
        
    # screen play navigation
    def goToIntro(self, *arg):
        self.current = 'screen1'

    def goToGameScreen(self, *arg):
        self.current = 'screen2'

    # Dealing with Sound
    def on_soundActivated(self, obj, value):
        ''' Turn the intro song on or off '''
        if value:
            self.sound.loop = True
            self.sound.play()
        else:
            self.sound.stop()

    def on_name_of_players(self,value, obj):
        pickle.dump(list(self.name_of_players), open("name_of_players.pkl", "wb"))
        
    def player_name_popup(self, numPlayers):
        '''called after selecting number of players'''
        self.number_of_players = numPlayers
        if False: # iOS is not happy with pickling..??
            try:
                names = pickle.load(open("name_of_players.pkl", "rb"))
                if len(names) < numPlayers:
                    names = names +  ['John', 'Sally', 'Sam', 'Joey'][::-1][numPlayers - len(names)]
                self.name_of_players = names[:numPlayers]
            except:
                self.name_of_players = ['John', 'Sally', 'Sam', 'Joey'][0:numPlayers]
        else:
            self.name_of_players = ['John', 'Sally', 'Sam', 'Joey'][0:numPlayers]
        playername = PlayerNamePopup(self.name_of_players)
        playername.open()
        playername.bind(on_dismiss = self.goToGameScreen)

    def quit(self):
        ''' You are quiting the current game '''
        if self.active:
            self.playscreen.scores_of_players = [0,0,0,0]
            self.playscreen.aiScore = 0
            self.goToIntro()
            self.playscreen.stopRotation()
            self.active = False

    def goToTutorial(self):
        self.current = 'tutorialFlow'


def boolFromJS(value):
    ''' JSON config returns '1' and '0' for True and False'''
    return True if value == '1' else False


class CollectionApp(App):
    active = BooleanProperty(False)

    def build(self):
        Clock.max_iteration = 50
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
        self.settings = settings
        self.settings.interface.menu.width = dp(100)
        settings.add_json_panel('Settings', self.config, data=settingsjson)
        settingsCloseButton = settings.interface.ids.menu.ids.button
        self.settingsCloseButton = settingsCloseButton
        self.settingsCloseButton.text = "Return"
        settingsCloseButton.on_press = self.leaveSettingsPanel
        settings.interface.ids.menu.add_widget(Button(text="Tutorial",
                                                      size_hint = (None, None),
                                                      x= settingsCloseButton.x,
                                                      y = settingsCloseButton.top + 10,
                                                      size = settingsCloseButton.size, 
                                                      on_press= self.moveToTutorial))

        self.quitButton = Button(text="Quit",
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
            self.gamelayout.playscreen.hintActivated = boolFromJS(value)
        if key == 'sound':
            self.gamelayout.soundActivated = boolFromJS(value)
        if key == 'hintspeed':
            speedSettings = {'slow':10, 'normal':5, 'fast':1}
            self.gamelayout.playscreen.displayHintTimer = speedSettings[value]
            print()
        if key == 'ai':
            self.gamelayout.playscreen.aiActivated = boolFromJS(value)

# To test the screen size you can use:
# kivy main.py -m screen:ipad3

if __name__ == '__main__':
    CollectionApp().run()
