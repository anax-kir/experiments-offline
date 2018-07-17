from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

import os
import _thread
import time
import pandas as pd


class WelcomeScreen(Screen):
    """
    Welcome screen contents
    """
    loadfile = ObjectProperty(None)
    type = StringProperty('')
    type_chosen = False

    def record_choice(self, state, value):
        if state == "down":
            self.type_chosen = True
            self.type = value
        else:
            self.type_chosen = False

    def upload(self):
        if self.type_chosen:
            self.show_load()

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        self.content = LoadDialog(load=self.load,
                             cancel=self.dismiss_popup)
        self._popup = Popup(title="Upload experiment file",
                            content=self.content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
        _thread.start_new_thread(self.track_changes_dir, ())

    def track_changes_dir(self):
        path_to_watch = "."
        before = os.listdir(path_to_watch)
        filechooser = getattr(self.content.ids, "filechooser")
        counter = 0
        while counter < 15:
            time.sleep(5)
            after = os.listdir(path_to_watch)
            if before != after:
                filechooser._update_files()
                print("updated")
                before = after
            else:
                counter += 1

    def load(self, path, filename):
        try:
            self.all_sentences = pd.read_csv(os.path.join(path, filename[0]), sep=";",
                                        header="infer",
                                        names=["type", "group", "number_within_group", "sentence"],
                                        skip_blank_lines=True, encoding="utf8")
            self.exit = True
            data_screen = getattr(self.manager.ids, "data_screen")
            data_screen.extract_sentences(self.all_sentences)
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
        return os.path.abspath(__file__ + "/../../")

    def is_csv(self, *args):
        filename = args[1]
        return "csv" in filename
