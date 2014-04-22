from __future__ import print_function

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty, StringProperty
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from Deck import Deck
from kivy.clock import Clock
from kivy.core.window import Window

number_of_players = 4
name_of_players = ['John', 'Sally', 'Sam', 'Joey']
# initialize the score of players to 0
player_scores = dict.fromkeys(name_of_players, 0)

import sys
from os import environ
from kivy.config import Config
from kivy.logger import Logger

from AI import AI

class PlayerSection(Button):
    def __init__(self,**kwargs):
        super(PlayerSection, self).__init__(**kwargs)
        self.size = Window.size[0]//6, Window.size[1]//6


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
    scores = StringProperty('')
    numberofsets = NumericProperty(0)
    number_of_players = NumericProperty(1)

    def __init__(self, **kwargs):
        self.buttons = [None] * 12
        super(GameLayout, self).__init__(**kwargs)
        playscreen = self.children[0].get_screen('screen2')
        self.deck = Deck()
        self.cards = self.deck.drawGuarantee(numberofcards=12)
        if AI_on:
            pass

        self.ai = AI()
        for i in range(12):
            self.buttons[i] = MyToggleButton()
            self.buttons[i].bind(on_press=self.checkIfSetOnBoard)
            playscreen.children[0].add_widget(self.buttons[i])
        self.numberofsets = self.deck.numberOfSets(self.cards)
        self.setUpHint()
        self.setUpAI()
        self.updateGrid()

        # add a dropdown button for 'Set' call
        if number_of_players > 1:
            self.setbutton = DropDown()
            for index in range(number_of_players):
                btn = Button(
                    text=str(name_of_players[index - 1]), size_hint_y=None, height=20)
                btn.bind(
                    on_release=lambda btn: self.setbutton.select(btn.text))
                self.setbutton.add_widget(btn)

            self.mainbutton = Button(
                text='Set', size_hint=(None, None), size=(100, 100))
            self.mainbutton.bind(on_release=self.setbutton.open)
            # to verify if there is a set
            self.setbutton.bind(on_select=self.on_set_callback)
        else:
            self.mainbutton = Button(
                text='Set', size_hint=(None, None), size=(100, 100))
            self.mainbutton.bind(on_release=self.on_set_callback)
        playscreen.add_widget(self.mainbutton)
        for name in name_of_players:
            self.scores += name + '      ' + \
                str(player_scores[name]) + '      '

    def updateGrid(self):
        '''Updates the cards being displayed'''
        for i, card in enumerate(self.cards):
            self.buttons[i].card = card
            self.buttons[i].state = 'normal'

    def setUpHint(self):
        '''Set-up which cards will be part of the hint'''
        self.hint = Deck.hint(self.cards)
        # After 10 second show a hint
        Clock.schedule_once(self.displayHint, 5)

    def setUpAI(self):
        (time, self.aiCards) = ai.suggestion(self.cards)
        Clock.schedule_once(self.AIplay, 2)

    def AIplay(self):
        print(self.aiCards)

    def displayHint(self, *arg):
        for index, button in enumerate(self.buttons):
            if self.cards[index] in self.hint:
                button.state = 'down'
            else:
                button.state = 'normal'

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
        if len(down) != 3:
            return
        if Deck.checkSet(self.cards[down[0]], self.cards[down[1]], self.cards[down[2]]):
            selectedcards = {self.cards[i] for i in down}
            newcards = self.deck.drawGuarantee(othercards=set(self.cards) ^ selectedcards, numberofcards=3)
            self.numberofsets = self.deck.numberOfSets(self.cards)
            for index, i in enumerate(down):
                self.cards[i] = newcards[index]
            self.updateGrid()
        else:
            self.unselectAll()

    def on_set_callback(self, obj, value):
        '''Called when the player button is pressed'''
        down = []
        for index, button in enumerate(self.buttons):
            if button.state == 'down':
                down.append(index)
        if len(down) == 3:
            if Deck.checkSet(self.cards[down[0]], self.cards[down[1]], self.cards[down[2]]):
                selectedcards = {self.cards[i] for i in down}
                newcards = self.deck.drawGuarantee(
                    othercards=set(self.cards) ^ selectedcards, numberofcards=3)
                if newcards is False:
                    self.children[0].current = 'screen3'
                else:
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

# To test the screen size you can use:
# kivy main.py -m screen:ipad3

class ScreenApp(App):
    def build(self):
        return GameLayout()

if __name__ == '__main__':
    ScreenApp().run()
