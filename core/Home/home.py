from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty, DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivymd.uix.picker import MDDatePicker
from kivymd.theming import ThemableBehavior

from database import SQLite3
from datetime import datetime
import locale
locale.setlocale(locale.LC_ALL, '')
import os

_path = os.path.dirname(__file__)
Builder.load_file(os.path.join(_path, "home.kv"))


class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

    def on_pre_enter(self, *args):
        self.load()

    def load(self):
        self.ids["salesList"].clear_widgets()
        for timestamp, rowid in SQLite3.getDate()[::-1]:
            date = datetime.fromtimestamp(timestamp)
            self.ids["salesList"].add_widget(
                SalesListItem(text=date.strftime("%B %d %Y"),
                              rowid=rowid,
                              on_release=lambda x: MDCustomBottomSheet(screen=ContentCustomSheet(rowid=x.rowid)).open())
            )

    def switch(self, screen):
        self.ids["screen_manager"].current = screen

    def process(self, sale: int, date):
        SQLite3.insertData(sale, date)
        self.switch(self.ids["screen_manager"].previous())
        self.ids["backdrop"].open()
        self.ids["insertSales"].text = ""

    def show_time_picker(self):
        time_dialog = MDDatePicker(min_year=2020, max_year=2030, primary_color="darkmagenta")
        time_dialog.bind(on_save=self.on_save)
        time_dialog.open()

    def on_save(self, instance, value, date_range):
        self.ids["dateBtn"].text = value

    def set_error_message(self):
        self.ids["insertSales"].error = True

    def checkTrue(self, obj):
        if obj.text == "":
            self.ids["insertSales"].error = True
        else:
            self.ids["insertSales"].error = False


#########################################################################################


class SalesListItem(OneLineListItem):
    rowid = NumericProperty()


class ContentCustomSheet(BoxLayout, ThemableBehavior):
    rowid = NumericProperty()
    dialog = None
    obj = ObjectProperty()

    def __init__(self, **kwargs):
        super(ContentCustomSheet, self).__init__(**kwargs)

    def closeBottomSheet(self, app):
        app.show_alert(self)


class ComputeSales(BoxLayout, ThemableBehavior):
    dialog = None

    def compute(self, first: int, second: int):
        Total = int(first) + int(second)
        Mayann = locale.currency((float(.40) * float(Total)) + 1250, grouping=True)
        Revan = locale.currency((.60 * float(Total)) - 1250, grouping=True)
        earl = locale.currency(float(.20) * ((float(.60) * float(Total)) - 1250), grouping=True)
        lei = locale.currency(float(.10) * ((float(.60) * float(Total)) - 1250), grouping=True)
        revan = locale.currency(float(.70) * ((float(.60) * float(Total)) - 1250), grouping=True)
        info = {
            "revan": revan,
            "mayann": Mayann,
            "earl": earl,
            "lei": lei,
            "nobe": Revan,
            "total": Total
        }
        if not self.dialog:
            self.dialog = MDDialog(
                type="custom",
                content_cls=ContentCompute(info=info),
                buttons=[
                    MDRaisedButton(
                        text="OK", md_bg_color=self.theme_cls.primary_color, on_release=self.close
                    ),
                ],
                auto_dismiss=False
            )
        self.dialog.open()

    def close(self, *args):
        self.dialog.dismiss(force=True)
        self.ids["sale1"].text = ""
        self.ids["sale2"].text = ""

    def error_text(self, sale1, sale2):
        sale1.error = True
        sale2.error = True


class ContentCompute(BoxLayout):
    info = DictProperty()
