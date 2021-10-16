from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.lang import Builder
import random
from kivy.clock import Clock
from kivy.core.window import Window
Window.size = (300, 630)

Builder.load_string("""
#:import Clock kivy.clock.Clock
<Home>:
    orientation: "vertical"
    MDLabel:
        text: "Rate my handsome face"
        pos_hint: {"center_y":.8}
        font_style: "H3"
        halign: "center"
    MDLabel:
        id: Rates
        text: "100%"
        halign: "center"
        font_style: "H6"
    MDRaisedButton:
        text: "Rate"
        on_release: root.call_back()
        pos_hint: {"center_x": .5, "center_y": .2}
    MDLabel:
        id: Face
        text: ""
        pos_hint: {"center_y":.1}
        halign: "center"
        font_style: "H6"
""")


class Home(Screen):

    def call_back(self):
        self.event = Clock.schedule_interval(self.my_callback, 0)
        Clock.schedule_once(self.cancel, 3)

    def my_callback(self, *args):
        self.ids["Rates"].text = f"{str(random.randrange(1, 100))}%"

    def cancel(self, *args):
        Clock.unschedule(self.event.cancel())
        if 80 > int(self.ids["Rates"].text[:-1]) > 50:
            self.ids["Face"].text = "Ugly"
        elif int(self.ids["Rates"].text[:-1]) < 50:
            self.ids["Face"].text = "Super Ugly"
        else:
            self.ids["Face"].text = "Handsome"

class MyApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Home(name="home"))
        return sm

MyApp().run()
