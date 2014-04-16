from __future__ import print_function

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty,StringProperty
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from Deck import Deck
from kivy.clock import Clock

number_of_players = 4
name_of_players = ['John','Sally','Sam','Joey']
# initialize the score of players to 0
player_scores=dict.fromkeys(name_of_players,0)

import sys
from os import environ
from kivy.config import Config
from kivy.logger import Logger

# taken from http://en.wikipedia.org/wiki/List_of_displays_by_pixel_density
devices = {
    # device: (name, width, height, dpi, density)
    'onex': ('HTC One X', 1280, 720, 312, 2),
    's3': ('Galaxy SIII', 1280, 720, 306, 2),
    'droid2': ('Motolora Droid 2', 854, 480, 240, 1.5),
    'xoom': ('Motolora Xoom', 1280, 800, 149, 1),
    'ipad': ('iPad (1 and 2)', 1024, 768, 132, 1),
    'ipad3': ('iPad 3', 2048, 1536, 264, 2),
    'iphone4': ('iPhone 4', 640, 960, 326, 2),
    'iphone5': ('iPhone 5', 640, 1136, 326, 2),
}


def start(win, ctx):
    pass


def stop(win, ctx):
    pass


def apply_device(device, scale, orientation):
    name, width, height, dpi, density = devices[device]
    if orientation == 'portrait':
        width, height = height, width
    Logger.info('Screen: Apply screen settings for {0}'.format(name))
    Logger.info('Screen: size={0}x{1} dpi={2} density={3} '
        'orientation={4}'.format(width, height, dpi, density, orientation))
    environ['KIVY_METRICS_DENSITY'] = str(density)
    environ['KIVY_DPI'] = str(dpi)
    Config.set('graphics', 'width', str(width))
    Config.set('graphics', 'height', str(height))
    Config.set('graphics', 'fullscreen', '0')
    Config.set('graphics', 'show_mousecursor', '1')


def configure(ctx):
    scale = ctx.pop('scale', None)
    orientation = 'landscape'
    ctx.pop('landscape', None)
    if ctx.pop('portrait', None):
        orientation = 'portrait'
    if not ctx:
        return usage(None)
    device = ctx.keys()[0]
    if device not in devices:
        return usage('')
    apply_device(device, scale, orientation)


class MyToggleButton(ToggleButton):
    pass


class GameLayout(FloatLayout):
    score = NumericProperty(0)
    scores = StringProperty('')
    numberofsets = NumericProperty(0)
    def __init__(self, **kwargs):
        self.buttons = [None] * 12
        super(GameLayout, self).__init__(**kwargs)
        playscreen = self.children[0].get_screen('screen2')
        self.deck = Deck()
        self.cards = self.deck.drawGuarantee(numberofcards=12)
        for i in range(12):
            btn_text = 'Button' + str(i + 1)
            self.buttons[i] = MyToggleButton()
            self.buttons[i].bind(
                on_press=self.on_press_callback, state=self.state_callback)
            self.buttons[i].children[0].text = str(self.cards[i])
            playscreen.children[0].add_widget(self.buttons[i])
        self.numberofsets = self.deck.numberOfSets(self.cards)
        self.setUpHint()

        # add a dropdown button for 'Set' call
        if number_of_players > 1:
            self.setbutton = DropDown()
            for index in range(number_of_players):
                btn = Button(text=str(name_of_players[index-1]), size_hint_y=None, height=20)
                btn.bind(on_release=lambda btn: self.setbutton.select(btn.text))
                self.setbutton.add_widget(btn)

            self.mainbutton = Button(text='Set', size_hint=(None, None),size=(100,100))
            self.mainbutton.bind(on_release=self.setbutton.open)
            self.setbutton.bind(on_select=self.on_set_callback) # to verify if there is a set
        else:
            self.mainbutton = Button(text='Set', size_hint=(None, None),size=(100,100))
            self.mainbutton.bind(on_release=self.on_set_callback)
        playscreen.add_widget(self.mainbutton)
        for name in name_of_players:
            self.scores += name + '      '+str(player_scores[name])+ '      '

    def play(self,numPlayers):
        global number_of_players
        number_of_players = numPlayers

    def setUpHint(self):
        self.hint = Deck.hint(self.cards)
        # After 10 second show a hint
        Clock.schedule_once(self.displayHint, 5)

    def displayHint(self,*arg):
        for index, button in enumerate(self.buttons):
            if self.cards[index] in self.hint:
                button.state = 'down'
            else:
                button.state = 'normal'

    def on_press_callback(self, obj):
        pass
        # down = []
        # for index, button in enumerate(self.buttons):
        #     if button.state == 'down':
        #         down.append(index)
        # if len(down) == 3:
        #     if Deck.checkSet(self.cards[down[0]], self.cards[down[1]], self.cards[down[2]]):
        #         selectedcards = {self.cards[i] for i in down}
        #         newcards = self.deck.drawGuarantee(othercards=set(self.cards) ^ selectedcards, numberofcards=3)
        #         self.score += 1
        #         self.numberofsets = self.deck.numberOfSets(self.cards)
        #         for index, i in enumerate(down):
        #             self.buttons[i].children[0].text = str(newcards[index])
        #             self.buttons[i].state = 'normal'
        #             self.cards[i] = newcards[index]
        #     else:
        #         for i in down:
        #             self.buttons[i].state = 'normal'
    def on_set_callback(self, obj,value):
        down = []
        for index, button in enumerate(self.buttons):
            if button.state == 'down':
                down.append(index)
        if len(down) == 3:
            if Deck.checkSet(self.cards[down[0]], self.cards[down[1]], self.cards[down[2]]):
                selectedcards = {self.cards[i] for i in down}
                newcards = self.deck.drawGuarantee(othercards=set(self.cards) ^ selectedcards, numberofcards=3)
                if number_of_players > 1:
                    player_scores[value] += 1
                else:
                    self.score += 1
                self.numberofsets = self.deck.numberOfSets(self.cards)
                for index, i in enumerate(down):
                    self.buttons[i].children[0].text = str(newcards[index])
                    self.buttons[i].state = 'normal'
                    self.cards[i] = newcards[index]
                self.setUpHint()
            else:
                for i in down:
                    self.buttons[i].state = 'normal'
        else:
            for i in down:
                self.buttons[i].state = 'normal'
        if number_of_players > 1:
            self.scores = ''
            for name in name_of_players:
                self.scores += name + '      '+str(player_scores[name])+ '      '


    def state_callback(self, obj, value):
        pass


class ScreenApp(App):

    def build(self):
        apply_device('ipad', None, 'portrait')
        return GameLayout()

if __name__ == '__main__':
    ScreenApp().run()
