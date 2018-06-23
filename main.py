from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty, DictProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window

import os

import custom_widgets


class LoadDialog(FloatLayout):
    """
    Load dialog and display current directory contents
    """
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def get_path(self):
        return os.path.dirname(os.path.abspath(__file__))


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


class DataScreen(Screen):
    """
    Data Screen: show file contents so user can check that file was parsed correctly
    """
    label_text = StringProperty('')


class StartScreen(Screen):
    """
    Press "start" to begin actual experiment
    """
    pass


class SocioLingScreen(Screen):
    """
    Sociolinguistic data Screen: ask informants to fill in info about themselves
    """
    choices = DictProperty({})

    def add_choice(self):
        print(self.choices)
        # self.choices[key] = value



class ExperimentApp(App):
    """
    Main Application Class
    """
    def build(self):
        self.title = 'Experiments: Layer 0'
        Window.clearcolor = (1, 1, 1, 1)


if __name__ == '__main__':
    ExperimentApp().run()