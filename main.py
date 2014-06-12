from kivy.app import App
from kivy.properties import *
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import (Screen,
                                    ScreenManager,
                                    FadeTransition,
                                    SlideTransition,
                                    NoTransition)
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy import platform
from kivy.clock import Clock
from jsonConfig import settingsjson
import pickle

from gameplay import GamePlayScreen
from PlayerNamePopup import PlayerNamePopup


class TutorialScreen(Popup):
    pass


class BoxLayoutim(BoxLayout):
    image1 = StringProperty('')
    image2 = StringProperty('')
    image3 = StringProperty('')


class EndGameScreen(Screen):
    name_of_players = ListProperty(['', '', '', ''])
    scores_of_players = ListProperty()
    screenManager = ObjectProperty()
    number_of_players = NumericProperty()
    game = ObjectProperty()
    aiActivated = BooleanProperty()
    aiScore = NumericProperty()

    def nthname(self, n):
        try:
            return [x for y, x in sorted(zip(
                self.scores_of_players + [self.aiScore],
                self.name_of_players + ['AI']*self.aiActivated))][::-1][n]
        except IndexError:
            return ''

    def nthscore(self, n):
        try:
            return sorted(self.scores_of_players +
                          [self.aiScore]*self.aiActivated)[::-1][n]
        except IndexError:
            return ''

    def on_enter(self, *args, **kwargs):
        if self.aiActivated:
            self.number_of_players += 1

    def on_leave(self, *args, **kwargs):
        if self.aiActivated:
            self.number_of_players -= 1


class PlayerSection(Button):
    myvalue = NumericProperty(4)

    def __init__(self, **kwargs):
        super(PlayerSection, self).__init__(**kwargs)
        self.size = Window.size[0] // 6, Window.size[1] // 6


class Music(Widget):
    soundActivated = BooleanProperty(False)
    currentSong = StringProperty('set_song')
    sound = ObjectProperty()

    def on_currentSong(self, obj, value):
        self.playMusic()

    def on_soundActivated(self, obj, value):
        self.playMusic()

    def playMusic(self):
        if self.sound:
            self.sound.stop()
        self.sound = SoundLoader.load("music/" + self.currentSong + ".wav")
        if self.soundActivated:
            self.sound.loop = True
            self.sound.play()
        else:
            self.sound.stop()


class GameLayout(ScreenManager):
    ''' This class manages the movements
    between the various screen and the sound '''

    name_of_players = ListProperty(['Score', '', '', ''])
    number_of_players = NumericProperty(1)
    scores_of_players = ListProperty([0, 0, 0, 0])
    aiActivated = BooleanProperty()
    aiScore = NumericProperty()

    # True if there is a game going on
    active = BooleanProperty(False)

    directory = StringProperty()

    def __init__(self, **kwargs):
        super(GameLayout, self).__init__(**kwargs)
        # on_enter of intro screen is not called, set the song here
        App.get_running_app().music.currentSong = 'shugou_song_main'
        self.playscreen = self.get_screen('game')
        self.transition = FadeTransition()

    # screen play navigation
    def goToIntro(self, *arg):
        self.transition = NoTransition()
        self.current = 'intro'

    def goToGameScreen(self, *arg):
        self.transition = FadeTransition()
        self.current = 'game'

    def pickleFile(self):
        return self.directory + "name_of_players.pkl"

    def on_name_of_players(self, value, obj):
        if platform == 'macosx' or platform == 'ios':
            with open(self.pickleFile(), "wb") as playersNamePickle:
                pickle.dump(list(self.name_of_players), playersNamePickle)

    def player_name_popup(self, numPlayers):
        '''called after selecting number of players'''
        self.number_of_players = numPlayers
        tempNames = ['John', 'Sally', 'Sam', 'Joey']

        if self.number_of_players == 1 or platform == 'android':
            self.name_of_players = tempNames
            self.goToGameScreen()
            return
        if platform == 'macosx' or platform == 'ios':
            try:
                names = pickle.load(open(self.pickleFile(), "rb"))
                for index, name in enumerate(names):
                    tempNames[index] = name
            except Exception as exception:
                print("Loading from Pickling went wrong, using default names")

        self.name_of_players = tempNames
        playername = PlayerNamePopup(self.name_of_players, numPlayers)
        playername.goto_game = self.goToGameScreen
        playername.open()

    def quit(self):
        ''' You are quiting the current game '''
        if self.active:
            self.goToIntro()
            self.active = False


def boolFromJS(value):
    ''' JSON config returns '1' and '0' for True and False'''
    return True if value == '1' else False


class ShugouApp(App):
    active = BooleanProperty(False)

    def build(self):
        self.music = Music()
        Clock.max_iteration = 50
        self.use_kivy_settings = False
        self.gamelayout = GameLayout()
        self.settings_cls = SettingsWithSidebar
        self.loadSettings()
        self.gamelayout.bind(active=self.changeActive)
        self.gamelayout.directory = self.whereToSave()
        return self.gamelayout

    def whereToSave(self):
        # Returns in which directory you can store files
        return self.get_application_config().rstrip("shugou.ini")

    def changeActive(self, instance, value):
        # This doesn't work..
        # crashes if the build_settings wasn't launched first
        # self.quitButton.disabled = not self.gamelayout.active
        pass

    def loadSettings(self):
        # Load the values already stored into the file
        self.speedSettings = {u'slow': 60, u'normal': 30, u'fast': 1, u'off': 0}
        self.music.soundActivated = boolFromJS(
            self.config.get('settings', 'sound'))
        speed = self.speedSettings[self.config.get('settings', 'hint')]
        if speed != 0:
            self.gamelayout.playscreen.displayHintTimer = speed
            self.gamelayout.playscreen.hintActivated = True
        else:
            self.gamelayout.playscreen.hintActivated = False
        self.gamelayout.playscreen.aiActivated = boolFromJS(
            self.config.get('settings', 'ai'))

    def build_config(self, config):
        config.setdefaults('settings', {'sound': False,
                                        'ai': False,
                                        'hint': 'off'})

    def build_settings(self, settings):
        Clock.unschedule(self.gamelayout.playscreen.AIplay)
        Clock.unschedule(self.gamelayout.playscreen.aiMoves)

        self.settings = settings
        self.settings.interface.menu.width = dp(100)
        settings.add_json_panel('Settings', self.config, data=settingsjson)
        settingsCloseButton = settings.interface.ids.menu.ids.button
        self.settingsCloseButton = settingsCloseButton
        self.settingsCloseButton.text = "Return"
        settingsCloseButton.on_press = self.leaveSettingsPanel
        settings.interface.ids.menu.add_widget(
            Button(text="Tutorial",
                   size_hint=(None, None),
                   x=settingsCloseButton.x,
                   y=settingsCloseButton.top + 10,
                   size=settingsCloseButton.size,
                   on_press=self.moveToTutorial))

        self.quitButton = Button(text="Quit",
                                 background_color=[1, 0, 0, 1],
                                 size_hint=(None, None),
                                 x=settingsCloseButton.x,
                                 y=settingsCloseButton.top
                                 + settingsCloseButton.height + 20,
                                 size=settingsCloseButton.size,
                                 disabled=False,
                                 on_press=self.quit)

        settings.interface.ids.menu.add_widget(self.quitButton)
        settings.on_close = self.quit

    def quit(self, *arg):
        self.gamelayout.quit()
        self.settingsCloseButton.trigger_action()

    def moveToTutorial(self, buttonInstance):
        tutorial = TutorialScreen(title="Tutorial")
        tutorial.open()

    def leaveSettingsPanel(self, *arg):
        ''' activated when you exit the setting panels'''
        self.gamelayout.playscreen.setUpHint()
        self.gamelayout.playscreen.setUpAI()

    def on_config_change(self, config, section, key, value):
        if key == 'sound':
            self.music.soundActivated = boolFromJS(value)
        elif key == 'hint':
            speed = self.speedSettings[value]
            if speed != 0:
                self.gamelayout.playscreen.displayHintTimer = speed
                self.gamelayout.playscreen.hintActivated = True
            else:
                self.gamelayout.playscreen.hintActivated = False
        elif key == 'ai':
            self.gamelayout.playscreen.aiActivated = boolFromJS(value)

# To test the screen size you can use:
# kivy main.py -m screen:ipad3

if __name__ == '__main__':
    ShugouApp().run()
