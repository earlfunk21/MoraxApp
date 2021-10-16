from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, WipeTransition
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.utils import get_color_from_hex
from core.Home.home import HomeScreen
from database import SQLite3
import os

_path = os.path.dirname(os.path.join(__file__, "KV"))


class MyApp(MDApp):
    dialog = None
    sm = ScreenManager(transition=WipeTransition())

    def build(self):
        self.sm.add_widget(HomeScreen(name="home"))
        return self.sm

    def show_alert(self, obj):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Are you Sure?",
                text="You want to remove?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color, on_press=self.close
                    ),
                    MDRaisedButton(
                        text="OK", md_bg_color=get_color_from_hex("#008000"), on_press=lambda x: self.delete(obj.rowid)
                    ),
                ],
                auto_dismiss=False
            )
        self.dialog.open()

    def close(self, *args):
        self.dialog.dismiss(force=True)

    def delete(self, rowid):
        SQLite3.removeData(rowid)
        self.close()
        self.sm.get_screen("home").ids["backdrop"].open()
