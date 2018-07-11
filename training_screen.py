from kivy.uix.screenmanager import Screen

import experiment_boxes as exp


class TrainingScreen(Screen):
    """
    Where training sentences are displayed
    """

    def import_acceptability(self):
        # a hack to make the kv file load
        load_box = exp.AcceptabilityBox()
        load_box.load_attr()
        #
        experiment_box = exp.AcceptabilityBox()
        saved = self.children[:]
        self.clear_widgets()
        self.add_widget(experiment_box)
        for widget in saved:
            self.add_widget(widget)
        self.experiment_design = experiment_box.create_design()
        instructions_label = getattr(self.ids, "instructions_label")
        instructions_label.text = self.experiment_design.instructions

    # def import_self_paced(self):
    #     print("hey2")

    # нужна киви-переменная, в которой будем хранить тип эксперимента,
    # который экспериментатор выбирает при загрузке своего файла
    # пока так:

    def load_experiment(self):
        self.experiment_current = "acceptability"

        experiment_types = {
            "acceptability": self.import_acceptability  # ,
            # "self_paced": self.import_self_paced
        }

        experiment_types[self.experiment_current]()

    def remove_widgets(self, widgets):
        for widget in widgets:
            hideable_widget = getattr(self.ids, widget)
            self.remove_widget(hideable_widget)

    def add_widgets(self, widgets):
        for widget in widgets:
            hideable_widget = getattr(self.ids, widget)
            self.add_widget(hideable_widget)