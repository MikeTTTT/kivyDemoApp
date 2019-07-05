import kivy

kivy.require('1.1.3')

from kivy.properties import NumericProperty
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.treeview import TreeView
from kivy.clock import Clock


class Showcase(FloatLayout):
    pass

class StandardWidgets(FloatLayout):
    value = NumericProperty(0)

    def __init__(self, **kwargs):
        super(StandardWidgets, self).__init__(**kwargs)
        Clock.schedule_interval(self.increment_value, 1 / 30.)

    def increment_value(self, dt):
        self.value += dt


class ShowcaseApp(App):

    def on_select_node(self, instance, value):
        # ensure that any keybaord is released
        self.content.get_parent_window().release_keyboard()

        self.content.clear_widgets()
        try:
            w = getattr(self, 'show_%s' %
                        value.text.lower().replace(' ', '_'))()
            self.content.add_widget(w)
        except Exception as e:
            print(e)

    def on_pause(self):
        return True

    def build(self):
        root = BoxLayout(orientation='horizontal', padding=20, spacing=20)
        tree = TreeView(
            size_hint=(None, 1), width=200, hide_root=True, indent_level=0)

        root.add_widget(tree)
        self.content = content = BoxLayout()
        root.add_widget(content)
        sc = Showcase()
        sc.content.add_widget(root)
        self.content.add_widget(StandardWidgets())
        return sc


if __name__ in ('__main__', '__android__'):
    ShowcaseApp().run()
