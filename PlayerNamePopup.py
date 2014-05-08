
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


class PlayerNamePopup(Popup):

    ''' Handles inputing the name of the users in the intro screen '''

    def __init__(self, namesOfPlayers):
        super(PlayerNamePopup, self).__init__()
        self.namesOfPlayers = namesOfPlayers
        # Create the screen which allows to select which user's name to change
        for i, name in enumerate(self.namesOfPlayers):
            button = Button()
            button.text = name
            button.value = i
            button.bind(on_press=self.click)
            self.ids.content.add_widget(button)

    def click(self, button):
        # In here, we create the popup where we request the user's names.
        # On click of the name we want to change, the user can enter a new
        # name.
        i = button.value
        popup = Popup(title="Enter Name here",
                      size_hint=(0.25, 0.25),
                      on_dismiss=lambda x: self.set_caption(x, i, button))
        box = GridLayout(cols=1)
        box.add_widget(
            TextInput(focus=True, text=button.text, multiline=False))
        box.children[0].select_all()
        box.add_widget(Button(text="Enter Name", on_press=popup.dismiss))
        popup.content = box
        popup.open()

    def set_caption(self, popup, i, button):
        # Set the name in the name_of_players array.
        self.namesOfPlayers[i] = popup.content.children[1].text
        button.text = self.namesOfPlayers[i]
