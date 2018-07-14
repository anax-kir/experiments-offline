from kivy.app import App
from kivy.properties import StringProperty, ListProperty
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.lang.builder import Builder

import os
import sys
import _locale

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])
PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PATH + '/screen_classes')

import custom_widgets
from welcome_screen import WelcomeScreen, LoadDialog
from agreement_screen import AgreementScreen
from socioling_screen import SocioLingScreen, SocioLingPopUp
from training_screen import TrainingScreen
from experiment_screen import ExperimentScreen


class DataScreen(Screen):
    """
    Data Screen: show file contents so user can check that file was parsed correctly
    """
    text = StringProperty('')

    test_sentences = ListProperty([
        {"test": "Who thinks that Paul took the necklace?"},
        {"test": "What does the detective think that Paul took?"},
        {"test": "Who wonders whether Paul took the necklace?"}
    ])

    exp_sentences = ListProperty([
        {"test": "Who thinks that Paul took the necklace?"},
        {"test": "What does the detective think that Paul took?"},
        {"test": "Who wonders whether Paul took the necklace?"}
    ])


class StartScreen(Screen):
    """
    Press "start" to begin actual experiment
    """
    pass


class EndScreen(Screen):
    """
    Experiment ends here
    """
    pass


class ExperimentApp(App):
    """
    Main Application Class
    """
    def build(self):
        with open("screen_classes/socioling.kv", encoding="utf8") as socioling_file:
            stream = socioling_file.read()
        representation = Builder.load_string(stream, filename="screen_classes/socioling.kv")
        self.title = "Experiments: Layer 0"
        Window.clearcolor = (1, 1, 1, 1)
        return representation


if __name__ == '__main__':
    ExperimentApp().run()