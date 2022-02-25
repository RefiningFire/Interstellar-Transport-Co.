from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout


class InterstellarTransportCoGame(BoxLayout):
    pass


class InterstellarTransportCoApp(App):
    def build(self):
        return InterstellarTransportCoGame()


if __name__ == '__main__':
    InterstellarTransportCoApp().run()
