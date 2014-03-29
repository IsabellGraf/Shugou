# Begin Preamble.

import kivy

# To make sure we are all at the same starting point
kivy.require('1.8.0')

from kivy.uix.button import Button
from time import time
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty, ObjectProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen, ScreenManager


# Global variables
num_players = 0


# Naming scheme for files:
# NUMBERCOLOURFILLINGSHAPE.jpg using the numbers above
# So for example, a one empty  blue square should be named
# 16711.jpg
# Notice that the first three digits are each one each and
# the last two are a two digit number.
# Pictures should be stored in a separate folder called 'pictures'
# (without quotes)
# This naming scheme also saves us from storing an extra variable.

# End preamble.


# For example, the person coding the title layout might
# want to use a class like is done in the game layout
# and modify this here and then change the SetApp code.
class TitleLayout(GridLayout):
    pass


# Here is the game layout.
# Currently, we organize everything into 3 columns.

# Code needed:
'''
The way I envision the game running is as follows:
Each player gets a button to push.
when they push the button they get say 10 seconds to select a set
and push okay (or if they select the 3 as time runs out thats okay too)
[10 seconds might be too fast but we'll see]

Then the computer verifies that the set works. If the set does not work
then that player cannot ring in again. If it does, that player
gains a point and then three new cards are dealt.

At any point when no set can be made, the computer must randomly shuffle
the deck and deal again. When no set is possible using the remaining
deck, the game ends.

For one player mode, we need an AI
This AI is based on a timer - say between 10 and 15 seconds 
as chosen randomly - after this amount of time the AI shows the solution
and then he gets a point.

'''

from Deck import NUMCARDS, NUMVISIBLECARDS


class GameLayout(GridLayout):

    def __init__(self, **kwargs):
        kwargs['cols'] = 3
        kwargs['spacing'] = 10
        kwargs['padding'] = [100, 100, 100, 100]
        super(GameLayout, self).__init__(**kwargs)
        # The label below belongs to the class so buttons can modify it.
        self.mainlabel = Label(text="Welcome to Set")
        self.deck = [None] * NUMCARDS
        # I have two null labels below
        self.add_widget(Label())
        self.add_widget(self.mainlabel)
        self.add_widget(Label())
        # Make the array of buttons.
        for i in range(NUMVISIBLECARDS):
            btn = Button(text="Button " + str(i))
            btn.bind(
                on_press=self.on_press_callback, state=self.state_callback)
            self.add_widget(btn)
        # return layout

    def state_callback(self, obj, value):
        self.mainlabel.text = str(obj.text)
        # Print statements print to the command line NOT to the app.
        print obj, value, num_players

    def on_press_callback(self, obj):
        print('press on button', obj)

    # Code needed.
    def checkEndGame(self):
        '''
        Post: When there is less than 21 cards, call this to make sure
        a valid set is present amongst ALL remaining cards.
        When this fails, end game.
        '''


class ScreenButton(Button):
    # Not 100% what this does
    # My interpretation is that this code initializes values and
    # can take in arguments as these parameters.
    screenmanager = ObjectProperty()
    title = ObjectProperty()

    # When this button is pressed, this code gets called.
    # This will change the screen to the specified screen.
    def on_press(self, *args, **kwargs):
        super(ScreenButton, self).on_press(*args)
        self.screenmanager.current = self.title
        # This code sequences allows you to modify the
        # global variable set up in the preamble.
        global num_players
        num_players = 1


# This is the code that will get run first (after main)
# This sets up the screen manager which controls what is on each screen
# Currently, screen 0 is a weak title page with one button
# the second screen is the game layout screen with a little bit
# of layout magic.
class SetApp(App):

    def build(self):
        sm = ScreenManager()

        screen = [None] * 2

        screen[0] = Screen(name='Main Menu')
        # Note: size and position should be relative to screen size
        # I'm just hacking code out so I did not do this.
        screen[0].add_widget(ScreenButton(screenmanager=sm, title='Title 1',
                                          size_hint=(None, None), text='Play Set', size=(200, 200),
                                          pos = (200, 200)))
        sm.add_widget(screen[0])

        screen[1] = Screen(name='Title 1')
        screen[1].add_widget(GameLayout())
        sm.add_widget(screen[1])

        return sm


if __name__ == '__main__':
    SetApp().run()
