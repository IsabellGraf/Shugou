from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.properties import StringProperty, ObjectProperty


class PlayerNameEdit(Popup):
    nameText = StringProperty('')
    textBox = ObjectProperty()


class PlayerNamePopup(Popup):

    ''' Handles inputing the name of the users in the intro screen '''

    def __init__(self, namesOfPlayers, numPlayers):
        super(PlayerNamePopup, self).__init__()
        self.namesOfPlayers = namesOfPlayers
        # Create the screen which allows to select which users' name to change
        for i, name in enumerate(self.namesOfPlayers[0:numPlayers]):
            button = Button(text=name, on_press=self.click)
            button.value = i
            self.ids.content.add_widget(button)

    def click(self, button):
        # In here, we create the popup where we request the new user's names.

        playerEdit = PlayerNameEdit(nameText=button.text,
                                    on_dismiss=lambda popup:
                                       self.set_caption(popup.textBox.text, button))
        playerEdit.textBox.select_all()
        playerEdit.open()

    def set_caption(self, newName, button):
        # Set the truncated name in the name_of_players array.
        self.namesOfPlayers[button.value] = newName[0:10]
        button.text = newName[0:10]