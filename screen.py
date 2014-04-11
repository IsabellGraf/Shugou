from __future__ import print_function

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.uix.label import Label
from Deck import Deck

class MyToggleButton(ToggleButton):
    pass

class GameLayout(FloatLayout):

    def __init__(self, **kwargs):
        self.buttons = [None] * 12
        super(GameLayout, self).__init__(**kwargs)
        playscreen = self.children[0].get_screen('screen2')
        self.deck = Deck()
        self.cards = self.deck.drawGuarantee(numberofcards=12)
        for i in range(12):
            btn_text = 'Button' + str(i + 1)
            self.buttons[i] = MyToggleButton()
            self.buttons[i].bind(on_press=self.on_press_callback, state=self.state_callback)
            self.buttons[i].children[0].text =  str(self.cards[i])
            self.buttons[i].children[0].markup = True
            playscreen.children[0].add_widget(self.buttons[i])            

    def play(self):
        pass

    def on_press_callback(self, obj):
        down = []
        for index, button in enumerate(self.buttons):
            if button.state == 'down':
                down.append(index)
        if len(down) == 3:
            if Deck.checkSet(self.cards[down[0]], self.cards[down[1]], self.cards[down[2]]):
                print("That is a set!")
            else:
                print("That is not a set~~")

    def state_callback(self, obj, value):
        pass

class ScreenApp(App):
    def build(self):
        return GameLayout()

if __name__ == '__main__':
    ScreenApp().run()
