from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, DictProperty, ObservableList
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
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
    data = {
            "name": "Name",
            "age": "Age",
            "education": "Level of education",
            "work_subject": "Work / Study subject",
            "birth_city": "City you were born in",
            "now_city": "City you currently live in",
            "mother_tongue": "Native language",
            "other_langs": "Other languages you speak"
            }

    from cities import parse_cities
    cities_list = parse_cities("cities.txt")

    languages = ["russian", "ukrainian", "english"]

    def add_choice(self, key, value):
        if value and (len(value) > 1 or type(value) == ObservableList):
            self.choices[key] = value
            print(self.choices)
        else:
            if key in self.choices:
                del self.choices[key]
                print(self.choices)

    def add_city(self, key, value):
        if value == "" or value in self.cities_list:
            self.add_choice(key, value)

    def checkbox_choice(self, key, value, state):
        if state == "down":
            self.add_choice(key, value)
        else:
            self.add_choice(key, "")

    def suggest_cities(self, widget):
        if widget.text:
            cities = [city for city in self.cities_list if city[0:len(widget.text)] == widget.text.capitalize()]
            widget.options = [Button(text=city, size_hint_y=None, height=50) for city in cities]

    def dismiss_popup(self):
        self.popup.dismiss()

    def save_info(self):
        errors = [key for key in self.data.keys() if key not in self.choices.keys()]
        if not errors:
            self.manager.current = "TrainingScreen"
        else:
            human_errors = [self.data[key] for key in errors]
            error_lines = "> " + "\n> ".join(human_errors) + "\n"
            self.errors_text = "[color=ff3333][b][size=25]You filled in the form incorrectly[/size][/b][/color]\n\n" \
                               "[b]Here are the fields you should change:[/b] \n\n" + error_lines
            content = SocioLingPopUp(cancel=self.dismiss_popup, errors_text=self.errors_text)
            self.popup = Popup(title="",
                               separator_height=0,
                               content=content,
                               size_hint=(None, None),
                               size=(400, 400))
            self.popup.open()


class SocioLingPopUp(FloatLayout):
    cancel = ObjectProperty(None)
    errors_text = StringProperty("")


class TrainingScreen(Screen):
    """
    Where training sentenses are displayed
    """
    pass


class ExperimentApp(App):
    """
    Main Application Class
    """
    def build(self):
        self.title = "Experiments: Layer 0"
        Window.clearcolor = (1, 1, 1, 1)


if __name__ == '__main__':
    ExperimentApp().run()