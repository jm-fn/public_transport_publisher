from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.clock import Clock

from context import scraper


LINES = {
    "Motol": ["Anděl", "Bertramka"],
    "Karlak": ["Anděl", "Karlovo náměstí"],
    "Centrum": ["Anděl", "Arbesovo náměstí"],
}


class MhdApp(App):
    def __init__(self, **kwargs):
        super(MhdApp, self).__init__(**kwargs)
        # Window.fullscreen = 'auto'


class MenuScreen(Screen):
    def btn_callback(self, instance):
        btn_name = instance.text
        pt = scraper.TransportLine(*LINES[btn_name])
        try:
            info = pt.get_times()
            self.manager.info_text = info
            Clock.schedule_once(self.manager.menu_screen_cbk, 60)
            self.manager.current = "_info_"
        except scraper.TransportLineError as err:
            self.manager.info_text = "Error: Showing the wrong screen!"
            self.manager.error_text = str(err)
            Clock.schedule_once(self.manager.menu_screen_cbk, 60)
            self.manager.current = "_error_"


class ErrorScreen(Screen):
    pass


class InfoScreen(Screen):
    pass


class MyScreenManager(ScreenManager):
    info_text = StringProperty("")
    error_text = StringProperty("")

    def build(self):
        sm = MyScreenManager()
        return sm

    def menu_screen_cbk(self, dt, **kwargs):
        self.current = "_menu_"


if __name__ == "__main__":
    MhdApp().run()
