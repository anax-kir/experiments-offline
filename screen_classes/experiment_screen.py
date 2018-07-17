from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

import experiment_boxes as exp


class ExperimentScreen(Screen):
    """
    Where actual experiment takes place
    """
    exp_sentences = ObjectProperty()

    def load_experiment(self):

        experiment_types = {
            "acceptability": "AcceptabilityBox",
            "self-paced": "SelfPacedBox"
        }

        box_name = experiment_types[self.type]
        experiment_box = getattr(exp, box_name)(self.exp_sentences)
        saved = self.children[:]
        self.clear_widgets()
        self.add_widget(experiment_box)
        for widget in saved:
            self.add_widget(widget)
        self.experiment_design = experiment_box.create_design(experiment_part="experiment")
        instructions_label = getattr(self.ids, "exp_instructions_label")
        instructions_label.text = self.experiment_design.instructions

    def remove_widgets(self, widgets):
        for widget in widgets:
            hideable_widget = getattr(self.ids, widget)
            self.remove_widget(hideable_widget)

    def add_widgets(self, widgets):
        for widget in widgets:
            hideable_widget = getattr(self.ids, widget)
            self.add_widget(hideable_widget)