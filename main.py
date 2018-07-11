from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window

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
        self.title = "Experiments: Layer 0"
        Window.clearcolor = (1, 1, 1, 1)


if __name__ == '__main__':
    ExperimentApp().run()