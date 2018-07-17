from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.properties import ObjectProperty


class DataScreen(Screen):
    """
    Data Screen: show file contents so user can check that file was parsed correctly
    """
    test_sentences = ObjectProperty(None, force_dispatch=True)
    exp_sentences = ObjectProperty(None, force_dispatch=True)
    text_to_check = ""

    # test_sentences = ListProperty([
    #     {"test": "Who thinks that Paul took the necklace?"},
    #     {"test": "What does the detective think that Paul took?"},
    #     {"test": "Who wonders whether Paul took the necklace?"}
    # ])
    #
    # exp_sentences = ListProperty([
    #     {"test": "Who thinks that Paul took the necklace?"},
    #     {"test": "What does the detective think that Paul took?"},
    #     {"test": "Who wonders whether Paul took the necklace?"}
    # ])

    def extract_sentences(self, all_sentences):
        """
        Latin square and randomization here
        """
        practice = all_sentences["type"] == "practice"
        experiment = (all_sentences["type"] == "test") | (all_sentences["type"] == "filler")

        # пока тут из датафрейма только сами предложения для примера, нужны еще номера предложений
        # NB: для self paced нужно еще как-то вопросы допилить — тип эксперимента можно взять в welcome_screen.type

        self.test_sentences = all_sentences[practice]["sentence"].values
        self.exp_sentences = all_sentences[experiment]["sentence"].values


        # текст, который выводится на экран, пока просто сами предложения

        self.text_to_check = all_sentences["sentence"].values[1:]
        scroll_layout = getattr(self.ids, "scroll_layout")
        scroll_layout.clear_widgets()

        for sentence in self.text_to_check:

            height = 90 if len(sentence) > 90 else 70

            label = Label(text=sentence, font_size=20,
                          color=(0, 0, 0, 1), size_hint_y=None, height=height, halign="left"
                          )
            
            label.text_size = label.width + 550, None

            scroll_layout.add_widget(label)
