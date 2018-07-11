from kivy.uix.screenmanager import Screen

import experiment_boxes as exp


class TrainingScreen(Screen):
    """
    Where training sentences are displayed
    """

    def load_experiment(self):
        # self.type is extracted from welcome screen

        experiment_types = {
            "acceptability": "AcceptabilityBox",
            "self-paced": "SelfPacedBox"
        }

        box_name = experiment_types[self.type]

        # a hack to make the kv file load
        load_box = getattr(exp, box_name)()
        load_box.load_attr()
        #
        experiment_box = getattr(exp, box_name)()
        saved = self.children[:]
        self.clear_widgets()
        self.add_widget(experiment_box)
        for widget in saved:
            self.add_widget(widget)
        self.experiment_design = experiment_box.create_design(experiment_part="training")
        instructions_label = getattr(self.ids, "instructions_label")

        training_text = "First, here are some [b]training[/b] sentences " \
                        "for you to get familiar with the experiment. \n\n"
        instructions_label.text = training_text + self.experiment_design.instructions

    def remove_widgets(self, widgets):
        for widget in widgets:
            hideable_widget = getattr(self.ids, widget)
            self.remove_widget(hideable_widget)

    def add_widgets(self, widgets):
        for widget in widgets:
            hideable_widget = getattr(self.ids, widget)
            self.add_widget(hideable_widget)