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

class MyToggleButton(ToggleButton):
    pass

class GameLayout(FloatLayout):

    def __init__(self, **kwargs):
        self.btns = [None] * 12
        super(GameLayout, self).__init__(**kwargs)
        playscreen = self.children[0].get_screen('screen2')
        for i in range(12):
            btn_text = 'Button' + str(i + 1)
            self.btns[i] = MyToggleButton()
            self.btns[i].bind(on_press=self.on_press_callback, state=self.state_callback)
            self.btns[i].children[0].text =  "[color=ff3333]Button[/color][color=3333ff]" + str(i) + "[/color]"
            self.btns[i].children[0].markup = True
            playscreen.children[0].add_widget(self.btns[i])            

    def play(self):
        pass

    def on_press_callback(self, obj):
        total = 0
        for btn in self.btns:
            if btn.state == 'down':
                total += 1

    def state_callback(self, obj, value):
        pass

class ScreenApp(App):
    def build(self):
        return GameLayout()

if __name__ == '__main__':
    ScreenApp().run()
