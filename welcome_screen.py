from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

import os


class WelcomeScreen(Screen):
    """
    Welcome screen contents
    """
    loadfile = ObjectProperty(None)
    text = StringProperty('')

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        print('"Upload" was pressed')
        content = LoadDialog(load=self.load,
                             cancel=self.dismiss_popup)
        self._popup = Popup(title="Upload experiment file",
                            content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        try:
            with open(os.path.join(path, filename[0])) as stream:
                self.text = stream.read()
                self.manager.current = "DataScreen"

            self.dismiss_popup()
        except IndexError:
            pass


class LoadDialog(FloatLayout):
    """
    Load dialog and display current directory contents
    """
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def get_path(self):
        return os.path.dirname(os.path.abspath(__file__))