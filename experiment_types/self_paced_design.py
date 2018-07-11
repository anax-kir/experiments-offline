from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

from datetime import datetime

from results_database import db_session, Participant, SelfPacedTrainingSentences, \
                             SelfPacedTrainingQuestions,SelfPacedExperimentSentences, \
                             SelfPacedExperimentQuestions

from socioling_screen import SocioLingScreen
from custom_widgets import CircularProgressBar


class SelfPacedDesign:

    def __init__(self, main_box, progress_layout, experiment_part):
        self.main_box = main_box
        self.progress_layout = progress_layout
        self.experiment_part = experiment_part  # test or actual experiment

    instructions = "Press [b]ENTER[/b] or [b]SPACE[/b] to see each word in the sentence one by one. \n\n" \
                   "Your task is to read the sentence as quickly as possible, " \
                   "while understanding it, as checked by a simple question on the following screen."

    test_sentences = [
        {"test": "Who thinks that Paul took the necklace?"},
        {"test": "What does the detective think that Paul took?"},
        {"test": "Who wonders whether Paul took the necklace?"}
    ]

    # 1 or 0 - is the answer yes or no
    questions = [
        {"quest": ["Did Jim take something?", 0]},
        {"quest": ["Is Paul a suspect?", 1]},
        {"quest": ["Is Paul guilty?", 0]}
    ]

    current_sentence = 1
    sentences_quantity = 3
    time_codes = []

    def save_quest_results(self, is_correct, time):
        if self.experiment_part == "training":
            result = self.save_quest_training(is_correct, time)
        else:
            result = self.save_quest_experiment(is_correct, time)
        db_session.add(result)
        db_session.commit()

    def save_quest_training(self, is_correct, time):
        result = SelfPacedTrainingQuestions(
            self.sentence_id,
            self.quest_text,
            self.answer,
            is_correct,
            str(time),
            self.participant.id
        )
        return result

    def save_quest_experiment(self, is_correct, time):
        result = SelfPacedExperimentQuestions(
            self.sentence_id,
            self.quest_text,
            self.answer,
            is_correct,
            str(time),
            self.participant.id
        )
        return result

    def remove_question_on_ok(self, widget):
        self.main_box.remove_widget(widget)
        self.remove_question()

    def remove_question(self):
        if self.current_sentence < self.sentences_quantity:
            self.main_box.remove_widget(self.question)
            self.current_sentence += 1
            self.top_label.text = self.old_text
            self.display_sentence()
        else:
            if self.experiment_part == "training":
                self.main_box.parent.manager.current = "ExperimentScreen"
            else:
                self.main_box.parent.manager.current = "EndScreen"

    def record_answer(self, widget):
        self.quest_time_end = datetime.now()
        delta = str(self.quest_time_end - self.quest_time_start)
        self.main_box.remove_widget(self.grid)

        self.answer = widget.text
        is_correct = self.questions[self.current_sentence - 1]["quest"][1]
        answer_correct = is_correct and self.answer == "Yes" or not is_correct and self.answer == "No"
        self.save_quest_results(int(answer_correct), delta)

        if not answer_correct:
            self.question.text = "[b]Not true! Please read quickly, but carefully[/b]"
            ok_button = Button(text="OK", background_color=(0, 1, 0, 1), font_size=25,
                               size_hint=(0.5, None), pos_hint={'center_x': 0.5}, height=50)
            ok_button.bind(on_press=self.remove_question_on_ok)
            self.main_box.add_widget(ok_button, 1)
        else:
            self.remove_question()

    def display_question(self):
        self.top_label = getattr(self.main_box.ids, "top_text")
        self.old_text = self.top_label.text
        self.top_label.text = "Please answer a question about the sentence you just read"
        self.quest_text = self.questions[self.current_sentence-1]["quest"][0]
        self.question = Label(text=self.quest_text, font_size="30", color=(0, 0, 0, 1), markup=True)
        self.main_box.add_widget(self.question, 1)
        self.grid = GridLayout(cols=2, row_force_default=True, row_default_height=40)
        yes_button = Button(text="Yes", background_color=(0, 1, 0, 1), font_size=25)
        no_button = Button(text="No", background_color=(1, 0, 0, 1), font_size=25)
        yes_button.bind(on_press=self.record_answer)
        no_button.bind(on_press=self.record_answer)
        self.grid.add_widget(yes_button)
        self.grid.add_widget(no_button)
        self.main_box.add_widget(self.grid, 1)
        self.quest_time_start = datetime.now()

    def display_sentence(self, *args):
        Window.on_key_down = self.key_reaction

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
        text = self.test_sentences[self.current_sentence-1]["test"]
        self.sent_text = text
        self.full_text = text.split()
        self.pos = 0
        for char in self.sent_text:
            if char not in [" ", ",", ".", "?", "!"]:
                self.sent_text = self.sent_text.replace(char, "_")

        self.sent = Label(text=self.sent_text, font_size="30", color=(0, 0, 0, 1))
        self.main_box.add_widget(self.sent)
        for widget in saved:
            self.main_box.add_widget(widget)
        self.time_start = 0
        self.time_codes = []

    def key_reaction(self, *args):
        if args[0] == 32 or args[0] == 13:
            if self.time_start:
                self.time_end = datetime.now()
                delta = str(self.time_end - self.time_start)
                self.time_codes.append(delta)
            if self.pos == len(self.full_text):
                self.main_box.remove_widget(self.sent)
                self.save_sent_results()
                self.display_question()

            current_text = self.sent_text.split()

            for index in range(len(current_text)):
                if index == self.pos:
                    current_text[index] = self.full_text[index]
                elif self.pos > 0 and index == self.pos - 1:
                    current_text[index] = "".join(["_" for letter in current_text[index]])

            self.sent.text = " ".join(current_text)
            self.time_start = datetime.now()
            self.pos += 1

    def save_sent_results(self):
        name = SocioLingScreen.choices["name"]
        self.participant = Participant.query.filter(Participant.name == name).first()
        self.sentence_id = self.current_sentence
        if self.experiment_part == "training":
            self.save_sent_training()
        elif self.experiment_part == "experiment":
            self.save_sent_experiment()

    def save_sent_training(self):
        for word, time_code in zip(self.full_text, self.time_codes):
            result = SelfPacedTrainingSentences(
                self.sentence_id,
                word,
                time_code,
                self.participant.id
                )
            db_session.add(result)
        db_session.commit()

    def save_sent_experiment(self):
        for word, time_code in zip(self.full_text, self.time_codes):
            result = SelfPacedExperimentSentences(
                self.sentence_id,
                word,
                time_code,
                self.participant.id
                )
            db_session.add(result)
        db_session.commit()

    def save_sent_results(self):
        name = SocioLingScreen.choices["name"]
        participant = Participant.query.filter(Participant.name == name).first()
        sentence_id = self.current_sentence
        for word, time_code in zip(self.full_text, self.time_codes):
            result = SelfPacedTrainingSentences(
                sentence_id,
                word,
                time_code,
                participant.id
                )
            db_session.add(result)
        db_session.commit()
