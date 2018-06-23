from kivy.uix.label import Label
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.factory import Factory
from kivy.lang import Builder

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
            
<ComboEdit>:
    size_hint: .5, .5
    pos_hint: {'center':(.5, .5)}
    options: [Button(text = str(x), size_hint_y = None, height = 50) for x in range(3)]
    
<MultiSelectOption@ToggleButton>:
    size_hint: 1, None
    height: '48dp'
""")


class ColoredLabel(Label):
    """
    Widget that adds color to Labels
    source: http://robertour.com/2015/07/15/kivy-label-or-widget-with-background-color-property/
    """
    background_color = ListProperty([1,1,1,1])


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

    def __init__(self, **kwargs):
        self.bind(drop_down=self.update_drop_down)
        self.bind(values=self.update_drop_down)
        super(MultiSelectSpinner, self).__init__(**kwargs)
        self.bind(on_release=self.toggle_drop_down)

    def toggle_drop_down(self, *args):
        if self.drop_down.parent:
            self.drop_down.dismiss()
        else:
            self.drop_down.open(self)

    def update_drop_down(self, *args):
        if not self.drop_down:
            self.drop_down = DropDown()
        values = self.values
        if values:
            if self.drop_down.children:
                self.drop_down.clear_widgets()
            for value in values:
                b = Factory.MultiSelectOption(text=value)
                b.bind(state=self.select_value)
                self.drop_down.add_widget(b)

    def select_value(self, instance, value):
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
            self.text = "choose 1 or more"


Factory.register('CustomKivy', module='ColoredLabel') # default: light-gray
Factory.register('CustomKivy', module='ComboEdit')
Factory.register('CustomKivy', module='MultiSelectSpinner')