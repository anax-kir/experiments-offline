from kivy.uix.label import Label

from datetime import datetime

from results_database import db_session, Participant, AcceptabilityTraining, AcceptabilityExperiment
from socioling_screen import SocioLingScreen
from custom_widgets import CircularProgressBar


class AcceptabilityDesign:

    def __init__(self, main_box, progress_layout, experiment_part):
        self.main_box = main_box
        self.progress_layout = progress_layout
        self.experiment_part = experiment_part  # test or actual experiment

    scores = dict()

    instructions = "For each sentence please determine its acceptability\non a scale from [b]1[/b] to [b]5[/b]"

    test_sentences = [
        {"test": "Who thinks that Paul took the necklace?"},
        {"test": "What does the detective think that Paul took?"},
        {"test": "Who wonders whether Paul took the necklace?"}
    ]

    current_sentence = 1
    sentences_quantity = 3

    def record_active_state(self, state, text):
        sent_key = str(self.current_sentence)
        if state == "down":
            self.scores[sent_key] = [int(text)]
        else:
            if sent_key in self.scores:
                del self.scores[sent_key]

    def record_result(self, *args):
        sent_key = str(self.current_sentence)
        if sent_key in self.scores:
            # stop timing
            self.time_end = datetime.now()
            delta = str(self.time_end - self.time_start)
            self.scores[sent_key].append(delta)
            print(self.scores)

            if self.current_sentence < self.sentences_quantity:
                for child in self.main_box.children:
                    text = getattr(child, "text", "")
                    if text == self.test_sentences[self.current_sentence - 1]["test"]:
                        self.main_box.remove_widget(child)

                    for btn in child.children:
                        state = getattr(btn, "state", "")
                        if state == "down":
                            btn.state = "normal"

                self.current_sentence += 1
                self.display_sentence()
            else:
                self.save_scores()

    def save_scores(self):
        name = SocioLingScreen.choices["name"]
        self.participant = Participant.query.filter(Participant.name == name).first()
        if self.experiment_part == "training":
            self.save_scores_training()
            self.main_box.parent.manager.current = "ExperimentScreen"
        elif self.experiment_part == "experiment":
            self.save_scores_experiment()
            self.main_box.parent.manager.current = "EndScreen"

    def save_scores_training(self):
        for index in range(len(self.test_sentences)):
            rating, time = self.scores[str(index+1)]
            result = AcceptabilityTraining(
                                    self.test_sentences[index]["test"],
                                    rating,
                                    time,
                                    self.participant.id
                                    )
            db_session.add(result)
        db_session.commit()

    def save_scores_experiment(self):
        for index in range(len(self.test_sentences)):
            rating, time = self.scores[str(index+1)]
            result = AcceptabilityExperiment(
                                    self.test_sentences[index]["test"],
                                    rating,
                                    time,
                                    self.participant.id
                                    )
            db_session.add(result)
        db_session.commit()

    def display_sentence(self, *args):
        pb = CircularProgressBar()
        pb.set_value((100 * (self.current_sentence-1)) / len(self.test_sentences))
        saved = self.main_box.children[:]
        saved.remove(self.progress_layout)
        saved.reverse()
        self.main_box.clear_widgets()
        self.main_box.add_widget(saved[0])

        self.progress_layout.add_widget(pb)
        pb.draw()
        self.main_box.add_widget(self.progress_layout)

        saved = saved[1:]
        sent = Label(text=self.test_sentences[self.current_sentence-1]["test"], font_size="30", color=(0, 0, 0, 1))
        self.main_box.add_widget(sent)
        for widget in saved:
            self.main_box.add_widget(widget)
        # all widgets displayed:
        self.time_start = datetime.now()
