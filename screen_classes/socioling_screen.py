from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, ObservableList, StringProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

from datetime import datetime
import os

from cities import parse_cities
from results_database import (db_session, Base, engine, Participant,
                              AcceptabilityTraining, AcceptabilityExperiment,
                              SelfPacedTrainingSentences, SelfPacedTrainingQuestions,
                              SelfPacedExperimentSentences, SelfPacedExperimentQuestions)


class SocioLingScreen(Screen):
    """
    Sociolinguistic data Screen: ask informants to fill in info about themselves
    """
    database_created = os.path.isfile(os.path.abspath(__file__) + "/../../" + "results.db")
    choices = dict()
    email = ObjectProperty(None)

    data = {
            "name": "Name",
            "age": "Age",
            "education": "Level of education",
            "degree_subject": "Your degree subject / specialty",
            "occupation": "Your current occupation",
            "childhood_city": "City where you spent your childhood",
            "longest_time_city": "City where you lived most of your life",
            "now_city": "City you currently live in",
            "native_languages": "Native language / languages",
            "other_languages": "Other languages you speak"
            }

    cities_list = parse_cities("media_data/cities.txt")

    native_languages = ["russian", "ukrainian", "belarus",
                        "kazakh", "tatar", "chechen",
                        "bashkir", "chuvash", "armenian"]
    native_languages.sort()

    other_languages = ["english", "german",
                       "spanish","french", "italian",
                       "chinese", "japanese", "finnish",
                       "hebrew"]

    all_languages = native_languages + other_languages
    all_languages.sort()

    def add_choice(self, key, value):
        if value and (len(value) > 2 or type(value) == ObservableList):
            self.choices[key] = value
        else:
            if key in self.choices:
                del self.choices[key]

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

    def create_database(self):

        db_tables = {
            "acceptability": [Participant.__table__, AcceptabilityTraining.__table__,
                              AcceptabilityExperiment.__table__],
            "self-paced": [Participant.__table__, SelfPacedTrainingSentences.__table__,
                           SelfPacedTrainingQuestions.__table__,
                           SelfPacedExperimentSentences.__table__,
                           SelfPacedExperimentQuestions.__table__]
        }
        Base.metadata.create_all(bind=engine, tables=db_tables[self.type])
        self.database_created = True

    def save_info(self):
        if not self.database_created:
            self.create_database()

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
                                      self.choices["degree_subject"],
                                      self.choices["occupation"],
                                      self.choices["childhood_city"],
                                      self.choices["longest_time_city"],
                                      self.choices["now_city"],
                                      ", ".join(self.choices["native_languages"]),
                                      ", ".join(self.choices["other_languages"]),
                                      self.email
                                      )

            db_session.add(participant)
            db_session.commit()

            self.manager.current = "TrainingScreen"
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