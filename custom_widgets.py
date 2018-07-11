from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ListProperty, ObjectProperty, StringProperty
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.progressbar import ProgressBar
from kivy.core.text import Label as CoreLabel
from kivy.graphics import Color, Ellipse, Rectangle

from socioling_screen import SocioLingScreen

Builder.load_string("""
#:import Button kivy.uix.button.Button

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

<GrayListLabel>:
    background_color: 0.95, 0.95, 0.95, 1
    color: 0, 0, 0, 1
    size_hint_x: None
    width: 400

<WhiteListLabel>:
    background_color: 1, 1, 1, 1
    color: 0, 0, 0, 1
    size_hint_x: None
    width: 400
         
<ComboEdit>:
    font_size: 20
    multiline: False
    background_color: 0.608, 0.608, 0.627, 0.1
    foreground_color: 0.608, 0.608, 0.627, 1
    text: "start typing to see suggestions"
    options: ""
    size_hint: .5, .5
    pos_hint: {'center':(.5, .5)}
    
<MultiSelectOption@ToggleButton>:
    size_hint: 1, None
    height: '48dp'
    
<MultiSelectSpinner>:
    color: 0, 0, 0, 1
    font_size: 20
    background_color: 0.608, 0.608, 0.627, 0.2
    text: "choose 1 or more"

<RatingButton>:
    background_color: 0.608, 0.608, 0.627, 0.5
    font_size: 20
    group: "score"
    
<CircularProgressBar>:
    size_hint: (None, None)
    height: 70
    width: 70
    max: 100
""")


class ColoredLabel(Label):
    """
    Widget that adds color to Labels
    source: http://robertour.com/2015/07/15/kivy-label-or-widget-with-background-color-property/
    """
    background_color = ListProperty([1,1,1,1])


class GrayListLabel(ColoredLabel):
    pass


class WhiteListLabel(ColoredLabel):
    pass


class RatingButton(ToggleButton):
    pass


class ComboEdit(TextInput):
    """
    Widget combining TextInput and DropDown with Buttons
    source: https://github.com/kivy/kivy/wiki/Editable-ComboBox
    """
    options = ListProperty(('', ))

    def __init__(self, **kw):
        ddn = self.drop_down = DropDown()
        ddn.bind(on_select=self.on_select)
        super(ComboEdit, self).__init__(**kw)

    def on_options(self, instance, value):
        ddn = self.drop_down
        ddn.clear_widgets()
        for widg in value:
            widg.bind(on_release=lambda btn: ddn.select(btn.text))
            ddn.add_widget(widg)

    def on_select(self, *args):
        self.text = args[1]

    def on_touch_up(self, touch):
        """
        checks if TextInput was "touched"
        """
        if touch.grab_current == self:
            self.options = ""
            if self.text == "start typing to see suggestions":
                self.text = ""
            self.foreground_color = 0, 0, 0, 1
            self.drop_down.open(self)
        else:
            if not self.text:
                self.text = "start typing to see suggestions"
                self.foreground_color = 0.608, 0.608, 0.627, 1

        return super(ComboEdit, self).on_touch_up(touch)


class MultiSelectSpinner(Button):
    """
    Widget allowing to select multiple text options
    source: https://stackoverflow.com/questions/36609017/kivy-spinner-widget-with-multiple-selection
    """

    drop_down = ObjectProperty(None)
    values = ListProperty([])
    selected_values = ListProperty([])
    check_type = StringProperty()
    saved_values = []

    def __init__(self, **kwargs):
        self.bind(drop_down=self.update_drop_down)
        self.bind(values=self.update_drop_down)
        super(MultiSelectSpinner, self).__init__(**kwargs)
        self.bind(on_release=self.toggle_drop_down)

    def toggle_drop_down(self, *args):
        if self.drop_down.parent:
            self.drop_down.dismiss()
        else:
            if self.saved_values:
                self.values = self.saved_values

            if self.check_type in SocioLingScreen.choices:
                self.saved_values = self.values[:]
                for value in self.saved_values:
                    if value in SocioLingScreen.choices[self.check_type]:
                        self.values.remove(value)
            self.create_buttons()
            self.drop_down.open(self)

    def create_buttons(self):
        if self.drop_down.children:
            self.drop_down.clear_widgets()
        for value in self.values:
            b = Factory.MultiSelectOption(text=value)
            if value in self.selected_values:
                b.state = "down"
            b.bind(state=self.select_value)
            self.drop_down.add_widget(b)

    def update_drop_down(self, *args):
        if not self.drop_down:
            self.drop_down = DropDown()
        values = self.values
        if values:
            self.create_buttons()

    def select_value(self, instance, value):
        choices = {'5': 15,
                   '6': 15,
                   '7': 13,
                   '8': 12,
                   '9': 11}

        if len(self.selected_values) > 4:
            self.font_size = choices.get(str(len(self.selected_values)), 10)
        else:
            self.font_size = 20

        if value == "down":
            if instance.text not in self.selected_values:
                self.selected_values.append(instance.text)
        else:
            if instance.text in self.selected_values:
                self.selected_values.remove(instance.text)

    def on_selected_values(self, instance, value):
        if value:
            self.text = ", ".join(value)
        else:
            self.font_size = 20
            self.text = "choose 1 or more"


class CircularProgressBar(ProgressBar):
    """
    source: https://stackoverflow.com/questions/50543028/how-to-make-circular-progress-bar-in-kivy
    """

    def __init__(self, **kwargs):
        super(CircularProgressBar, self).__init__(**kwargs)
        self.thickness = 25
        self.label = CoreLabel(text="0%", font_size=self.thickness-5)
        self.texture_size = None
        self.refresh_text()

    def draw(self):
        with self.canvas:
            self.canvas.clear()
            Color(0.608, 0.608, 0.627, 1)
            # label = self.parent.children[1]
            # y = label.pos[1] + label.height + 15
            # self.pos = [100, 100]
            # print(self.pos)
            # print(self.size)
            # print(self.parent.pos)
            Ellipse(pos=self.pos, size=self.size)
            Color(1, 0.49, 0.25, 1)
            Ellipse(pos=self.pos, size=self.size,
                    angle_end=(0.001 if self.value_normalized == 0 else self.value_normalized*360))
            Color(1, 1, 1)
            Ellipse(pos=(self.pos[0] + self.thickness / 2, self.pos[1] + self.thickness / 2),
                    size=(self.size[0] - self.thickness, self.size[1] - self.thickness))
            Color(0, 0, 0, 1)
            Rectangle(texture=self.label.texture, size=self.texture_size,
                      pos=(self.size[0]/2 - self.texture_size[0]/2, self.size[1]/2 - self.texture_size[1]/2))

    def refresh_text(self):
        self.label.refresh()
        self.texture_size = list(self.label.texture.size)

    def set_value(self, value):
        self.value = value
        self.label.text = str(int(self.value_normalized*100)) + "%"
        self.refresh_text()

