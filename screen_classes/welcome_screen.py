from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

import os
import _thread
import time


class WelcomeScreen(Screen):
    """
    Welcome screen contents
    """
    loadfile = ObjectProperty(None)
    text = StringProperty('')
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
        content = LoadDialog(load=self.load,
                             cancel=self.dismiss_popup)
        self._popup = Popup(title="Upload experiment file",
                            content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
        _thread.start_new_thread(self.track_changes_dir, ())

    def track_changes_dir(self):
        path_to_watch = "."
        before = dict([(item, None) for item in os.listdir(path_to_watch)])
        while True:
            if self.manager.current != "WelcomeScreen":
                break
            time.sleep(10)
            after = dict([(item, None) for item in os.listdir(path_to_watch)])
            added = [item for item in after if item not in before]
            removed = [item for item in before if item not in after]
            if added:
                print("Added: ", ", ".join(added))
            if removed:
                print("Removed: ", ", ".join(removed))
            if before != after:
                self.dismiss_popup()
                self.show_load()

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
        return os.path.abspath(__file__ + "/../../")