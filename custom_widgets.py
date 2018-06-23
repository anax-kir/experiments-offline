from kivy.uix.label import Label
from kivy.properties import ListProperty

from kivy.factory import Factory
from kivy.lang import Builder

Builder.load_string("""
<ColoredLabel>:
    background_color: 0.608, 0.608, 0.627, 1
    size_hint_y: None
    height: 40
    font_size: 20
    canvas.before:
        Color:
            rgba: self.background_color
        Rectangle:
            pos: self.pos
            size: self.size
""")


class ColoredLabel(Label):
    background_color = ListProperty([1,1,1,1])


Factory.register('ColoredKivy', module='ColoredLabel') # default: light-gray