
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.properties import *

class PlayerNameEdit(Popup):
    nameText = StringProperty('')


class PlayerNamePopup(Popup):

    ''' Handles inputing the name of the users in the intro screen '''

    def __init__(self, namesOfPlayers):
        super(PlayerNamePopup, self).__init__()
        self.namesOfPlayers = namesOfPlayers
        # Create the screen which allows to select which user's name to change
        for i, name in enumerate(self.namesOfPlayers):
            button = Button(text=name)
            button.value = i
            button.bind(on_press=self.click)
            self.ids.content.add_widget(button)

    def click(self, button):
        # In here, we create the popup where we request the user's names.
        # On click of the name we want to change, the user can enter a new
        # name.
        playerdit = PlayerNameEdit(nameText = button.text, 
                                   on_dismiss=lambda popup: 
                                            self.set_caption(popup.ids.textinput.text, button))
        playerdit.ids.textinput.select_all()
        playerdit.open()

    def set_caption(self, newName, button):
        # Set the name in the name_of_players array.
        self.namesOfPlayers[button.value] = newName
        button.text = self.namesOfPlayers[button.value]
