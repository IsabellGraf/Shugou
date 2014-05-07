from kivy.properties import *
from kivy.uix.screenmanager import Screen

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
        self.game.active = True
        self.game.setUpHint()
        self.game.setUpAI()
