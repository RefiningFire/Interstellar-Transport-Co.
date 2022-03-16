from kivy.app import App

from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.relativelayout import RelativeLayout

from kivy.animation import Animation

from kivy.core.window import Window

Window.maximize()



class MarketScreen(Screen):
        children_count = 0
        def __init__(self,**kwargs):
            super(MarketScreen,self).__init__(**kwargs)

        def add_buttons(self, commodities_list):
            children_count = len(commodities_list) * 60
            current_size_x = self.ids.commodity_list.size[0]

            # Update the list size to fill each market button.
            self.ids.commodity_list.size = (current_size_x, children_count)

            for each in commodities_list:
                temp_box_layout = BoxLayout(orientation='horizontal',spacing=20)

                temp_box_layout.add_widget(PlusButton(text='+100'))
                temp_box_layout.add_widget(PlusButton(text='+10'))
                temp_box_layout.add_widget(PlusButton(text='+1'))

                temp_box_layout.add_widget(MarketButton(text=each))

                temp_box_layout.add_widget(MinusButton(text='-1'))
                temp_box_layout.add_widget(MinusButton(text='-10'))
                temp_box_layout.add_widget(MinusButton(text='-100'))

                self.ids.commodity_list.add_widget(temp_box_layout)

class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class MyScreenManager(ScreenManager):
    pass

class MarketButton(Button):
    def getMessage(self, obj):
        print('MarketButton Pressed! It was:', obj.text)

class PlusButton(Button):
    pass

class MinusButton(Button):
    pass

class PlayerStats(RelativeLayout):
    pass

class PlayerStatButton(Button):
    def __init__(self,**kwargs):
        super(PlayerStatButton,self).__init__(**kwargs)

    def expand_contract(self):
        if self.pos[0] < self.parent.width / 2:
            anim_x = (self.parent.width -
                      self.width -
                      self.parent.spacing)
            new_text = '<'
        elif self.pos[0] > self.parent.width / 2:
            anim_x = 0
            new_text = '>'
        anim = Animation(x=anim_x,y=0, t='in_out_quart',d=0.5)
        anim.start(self.parent)
        self.text = new_text


class InterstellarTransportCoApp(App):
    def build(self):
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(MarketScreen(name='market'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))

        return sm

if __name__ == '__main__':
    InterstellarTransportCoApp().run()


'''
<MenuScreen>:
    BoxLayout:
        Button:
            text: 'Goto settings'
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1.5
                root.manager.current = 'settings'
        Button:
            text: 'Quit'

<SettingsScreen>:
    BoxLayout:
        Button:
            text: 'My settings button'
        Button:
            text: 'Back to menu'
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.transition.duration = 0.7
                root.manager.current = 'menu'
'''
