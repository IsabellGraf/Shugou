from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.properties import StringProperty

class PlayerNameEdit(Popup):
    nameText = StringProperty('')


class PlayerNamePopup(Popup):

    ''' Handles inputing the name of the users in the intro screen '''

    def __init__(self, namesOfPlayers):
        super(PlayerNamePopup, self).__init__()
        self.namesOfPlayers = namesOfPlayers
        # Create the screen which allows to select which users' name to change
        for i, name in enumerate(self.namesOfPlayers):
            button = Button(text=name, on_press=self.click)
            button.value = i
            self.ids.content.add_widget(button)

    def click(self, button):
        # In here, we create the popup where we request the new user's names.
        playerdit = PlayerNameEdit(nameText = button.text, 
                                   on_dismiss = lambda popup: 
                                            self.set_caption(popup.ids.textinput.text, button))
        playerdit.ids.textinput.select_all()
        playerdit.open()

    def set_caption(self, newName, button):
        # Set the name in the name_of_players array.
        self.namesOfPlayers[button.value] = newName[0:10]
        button.text = self.namesOfPlayers[button.value]
