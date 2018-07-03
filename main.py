from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, DictProperty, ObservableList
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window

from datetime import datetime
import os

from results_database import db_session, Participant, TrainingResult
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
    choices = dict()
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
        if value and (len(value) > 2 or type(value) == ObservableList):
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
        try:
            exists_name = db_session.query(Participant.id).filter(Participant.name == self.choices["name"]).count()
        except KeyError:
            exists_name = False

        if not errors and not exists_name:
            participant = Participant(
                                      datetime.now(),
                                      self.choices["name"],
                                      self.choices["age"],
                                      self.choices["gender"],
                                      self.choices["education"],
                                      self.choices["work_subject"],
                                      self.choices["birth_city"],
                                      self.choices["now_city"],
                                      " ".join(self.choices["mother_tongue"]),
                                      " ".join(self.choices["other_langs"])
                                      )

            db_session.add(participant)
            db_session.commit()

            self.manager.current = "AttentionScreen"
        else:
            self.errors_text = "[color=ff7400][b][size=25]You filled in the form incorrectly[/size][/b][/color]\n\n"

            if errors:
                human_errors = [self.data[key] for key in errors]
                error_lines = "> " + "\n> ".join(human_errors) + "\n"
                self.errors_text += "[b]Here are the fields you should change:[/b] \n\n" + error_lines
            elif exists_name:
                error_message = "[b]The name you chose already exists[/b]\n" \
                                "[b]Please enter a new name[/b]"
                self.errors_text += error_message

            content = SocioLingPopUp(cancel=self.dismiss_popup, errors_text=self.errors_text)
            self.popup = Popup(title="",
                               separator_height=0,
                               content=content,
                               size_hint=(None, None),
                               size=(400, 400))
            self.popup.open()


class SocioLingPopUp(FloatLayout):
    """
    Displayed if sociolinguistic data input was incorrect
    """
    cancel = ObjectProperty(None)
    errors_text = StringProperty("")


class AttentionScreen(Screen):
    """
    A message to participant to start paying attention"
    """
    pass


class TrainingScreen(Screen):
    """
    Where training sentences are displayed
    """
    instructions = "First, here are some training sentences for you to get familiar with the experiment. \n" \
                   "For each sentence please determine its acceptability on a scale from 1 to 5"

    test_sentences = [
                        {"test": "Who thinks that Paul took the necklace?"},
                        {"test": "What does the detective think that Paul took?"},
                        {"test": "Who wonders whether Paul took the necklace?"}
                     ]

    # предлагаю сначала рандомно отсортировать список, а потом выдавать по порядку
    # (пока рандома нет, сколько тестовых нужно?)

    current_sentence = 1
    sentences_quantity = 3

    scores = DictProperty({})

    def remove_widgets(self, widgets):
        for widget in widgets:
            hideable_widget = getattr(self.ids, widget)
            self.remove_widget(hideable_widget)

    def add_widgets(self, widgets):
        for widget in widgets:
            hideable_widget = getattr(self.ids, widget)
            self.add_widget(hideable_widget)

    def record_active_state(self, state, text):
        sent_key = str(self.current_sentence)
        if state == "down":
            self.scores[sent_key] = int(text)
        else:
            if sent_key in self.scores:
                del self.scores[sent_key]
        print(self.scores)

    def record_result(self):
        sent_key = str(self.current_sentence)
        if sent_key in self.scores:
            if self.current_sentence < self.sentences_quantity:
                box = getattr(self.ids, "sentence_box")
                for child in box.children:
                    try:
                        if child.text == self.test_sentences[self.current_sentence-1]["test"]:
                            box.remove_widget(child)
                    except:
                        try:
                            for btn in child.children:
                                if btn.state == "down":
                                    btn.state = "normal"
                        except:
                            pass

                self.current_sentence += 1
                self.display_sentence()
            else:
                self.save_scores()
                self.manager.current = "ExperimentScreen"

    def save_scores(self):
        name = SocioLingScreen.choices["name"]
        participant = Participant.query.filter(Participant.name == name).first()
        for index in range(len(self.test_sentences)):
            result = TrainingResult(
                                    self.test_sentences[index]["test"],
                                    self.scores[str(index+1)],
                                    participant.id
                                   )
            db_session.add(result)
        db_session.commit()

    def display_sentence(self):
        box = getattr(self.ids, "sentence_box")
        saved = box.children[:]
        saved.reverse()
        box.clear_widgets()
        box.add_widget(saved[0])
        saved = saved[1:]
        sent = Label(text=self.test_sentences[self.current_sentence-1]["test"], font_size="30", color=(0, 0, 0, 1))
        box.add_widget(sent)
        for widget in saved:
            box.add_widget(widget)


class ExperimentScreen(Screen):
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