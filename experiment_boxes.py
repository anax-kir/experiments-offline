from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

import os
import sys

PATH = os.path.dirname(os.path.abspath(__file__))
KIVY_PATH = PATH + "/experiment_boxes/"
sys.path.append(PATH + '/experiment_types')

from acceptability_design import AcceptabilityDesign
from self_paced_design import SelfPacedDesign


class AcceptabilityBox(BoxLayout):

    def create_design(self, *args):
        progress_layout = getattr(self.ids, "progress_bar")
        self.experiment_design = AcceptabilityDesign(self, progress_layout)
        return self.experiment_design

    def load_attr(self, *args):
        Builder.load_file(KIVY_PATH + "acceptability_box.kv")


class SelfPacedBox(BoxLayout):

    def create_design(self, *args):
        progress_layout = getattr(self.ids, "progress_bar")
        self.experiment_design = SelfPacedDesign(self, progress_layout)
        return self.experiment_design

    def load_attr(self, *args):
        Builder.load_file(KIVY_PATH + "self_paced_box.kv")