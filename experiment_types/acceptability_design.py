from kivy.uix.label import Label

from datetime import datetime

from results_database import db_session, Participant, TrainingResult
from socioling_screen import SocioLingScreen
import custom_widgets


class AcceptabilityDesign:

    def __init__(self, main_box, progress_layout):
        self.main_box = main_box
        self.progress_layout = progress_layout

    scores = dict()

    instructions = "First, here are some [b]training[/b] sentences for you to get familiar with the experiment. \n\n" \
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
                self.main_box.parent.manager.current = "ExperimentScreen"

    def save_scores(self):
        name = SocioLingScreen.choices["name"]
        participant = Participant.query.filter(Participant.name == name).first()
        for index in range(len(self.test_sentences)):
            rating, time = self.scores[str(index+1)]
            result = TrainingResult(
                                    self.test_sentences[index]["test"],
                                    rating,
                                    time,
                                    participant.id
                                    )
            db_session.add(result)
        db_session.commit()

    def display_sentence(self, *args):
        pb = custom_widgets.CircularProgressBar()
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
