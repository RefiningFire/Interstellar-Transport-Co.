from kivy.app import App

from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.relativelayout import RelativeLayout

from kivy.animation import Animation

from kivy.core.window import Window

import random
import re

Window.maximize()


# This is a list of the goods that each planet type can support, in descending order of commonality at start.
planet_possible_goods = [
                            [# Name, labor_value
                                {
                                'name':'Grain',
                                'labor_value':1
                                },{
                                'name':'Water',
                                'labor_value':2
                                },{
                                'name':'Bread',
                                'labor_value':3
                                },
                            ],
                            [
                                {
                                'name':'Ore',
                                'labor_value':1
                                },{
                                'name':'Energy',
                                'labor_value':2
                                },{
                                'name':'Fuel',
                                'labor_value':3
                                },
                            ],
                            [
                                {
                                'name':'Drone',
                                'labor_value':1
                                },{
                                'name':'Droid',
                                'labor_value':2
                                },{
                                'name':'Synthetic',
                                'labor_value':3
                                },
                            ]
                        ]

class Planet():
    def __init__(self,planet_possible_goods):
        self.__currently_populating = True
        self.__pop_pass = 0
        self.__pop_adjust = 0
        self.population = 0

        while self.__currently_populating:
            self.__temp = random.choices([0,1],
                                          weights=[80,20],
                                          k=1)

            # On an average of every 1 in 5 times, the population is increased.
            if self.__temp[0] > 0 and self.__pop_pass < 12:
                self.__temp_adjust_choice = random.choices(
                    [-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6],
                    weights=[1,2,4,8,16,32,64,32,16,8,4,2,1],
                    k=1)

                self.__temp_adjust = self.__temp_adjust_choice[0]

                self.__temp_adjust_counter = 0

                # Adjust the pop so that 7, 49, 343, etc are adusted up and down in an curve.
                for i in range(self.__pop_pass + 1):
                    self.__pop_adjust += self.__temp_adjust * (7 ** self.__temp_adjust_counter)
                    self.__temp_adjust_counter += 1

                self.__pop_pass += 1
            else:
                if self.__pop_pass == 0:
                    self.population == 0
                else:
                    self.population = 7 ** self.__pop_pass + self.__pop_adjust
                    if self.population < 0:
                        self.population = 0

                self.__currently_populating = False


        # The later a good occurs the less likely it will be produced.
        self.goods_types = planet_possible_goods

        self.producers = []
        self.__potential_producers = self.population

        for i in range(len(self.goods_types)):
            self.__temp_producers = random.randint(0,self.__potential_producers)

            self.producers.append(self.__temp_producers)

            # Decrease potential producers by the producers taken previous pass.
            self.__potential_producers -= self.__temp_producers

        self.market_goods = []

        for i in range(len(self.goods_types)):
            self.market_goods.append(
            {
            'name':self.goods_types[i]['name'],
            'labor_value':self.goods_types[i]['labor_value'],
            'production':self.producers[i],
            'consumption':0,
            'market':100,
            'reserve':14
            }
            )

        # Calculate and add consumption for each good in the market.
        for i in range(len(self.market_goods)):
            self.__temp_consumption = 0

            # Grain consumption on a planet = its bread production.
            if self.market_goods[i]['name'] == 'Grain':
                for x in range(len(self.market_goods)):
                    if self.market_goods[x]['name'] == 'Bread':
                        self.__temp_consumption = self.market_goods[x]['production']

            # Water consumption is 1:1 for population. Each person consumes 1.
            elif self.market_goods[i]['name'] == 'Water':
                self.__temp_consumption = self.population

            # Bread consumption is 1:1, w/modifier. Wealther people eat more.
            elif self.market_goods[i]['name'] == 'Bread':
                self.__temp_consumption = self.population


            self.market_goods[i]['consumption'] = self.__temp_consumption

        self.unemployment_calculation()

    def unemployment_calculation(self):
        self.unemployment = self.population

        # Remove each goods producers from the unemployment stat.
        for i in range(len(self.market_goods)):
            self.unemployment -= self.market_goods[i]['production']


class MarketScreen(Screen):
    children_count = 0
    def __init__(self,**kwargs):
        super(MarketScreen,self).__init__(**kwargs)

        # Create the list of planets.
        self.planets = []

        # Populate the list of planets.
        for i in range(80000):
            self.__temp_len = len(planet_possible_goods) - 1
            self.__selec = random.randint(0,self.__temp_len)
            self.planets.append(Planet(planet_possible_goods[self.__selec]))

    def add_buttons(self, commodities_list):
        children_count = len(commodities_list)
        current_size_x = self.ids.commodity_list.size[0]

        # Update the list size to fill each market button.
        self.ids.commodity_list.size = (current_size_x, (children_count + 1) * 60)

        temp_box_layout = BoxLayout(orientation='horizontal',spacing=20)
        temp_box_layout.add_widget(PlusMinusLabel(text='Buy 100'))
        temp_box_layout.add_widget(PlusMinusLabel(text='Buy 10'))
        temp_box_layout.add_widget(PlusMinusLabel(text='Buy 1'))
        temp_box_layout.add_widget(Label(text='Commodity',color=('4774A2'),font_size=30))
        temp_box_layout.add_widget(PlusMinusLabel(text='Sell 1'))
        temp_box_layout.add_widget(PlusMinusLabel(text='Sell 10'))
        temp_box_layout.add_widget(PlusMinusLabel(text='Sell 100'))


        self.ids.commodity_list.add_widget(temp_box_layout)

        for each in commodities_list:
            price = each['market'] * each['labor_value']

            temp_box_layout = BoxLayout(orientation='horizontal',spacing=20)

            temp_box_layout.add_widget(PlusButton(text=f'$-{price*100}'))
            temp_box_layout.add_widget(PlusButton(text=f'$-{price*10}'))
            temp_box_layout.add_widget(PlusButton(text=f'$-{price}'))

            temp_box_layout.add_widget(MarketButton(text=each['name']))

            temp_box_layout.add_widget(MinusButton(text=f'${price}'))
            temp_box_layout.add_widget(MinusButton(text=f'${price*10}'))
            temp_box_layout.add_widget(MinusButton(text=f'${price*100}'))

            self.ids.commodity_list.add_widget(temp_box_layout)

class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class MyScreenManager(ScreenManager):
    pass

class NewButton(Button):
    def __init__(self,**kwargs):
        super(Button,self).__init__(**kwargs)

    def make_transaction(self, commodity, value):
        # Remove the '$' from the text string and convert it to an integer.
        self.temp_commodity_value = int(re.sub('[$]','',str(value)))

        # Update player credits stat.
        app.player_stats['credits'] += self.temp_commodity_value

        # Update player commodities by amount purchased/sold
        app.player_commodities[commodity.lower()] += self.temp_commodity_value

        # Update the player credits button to match the stat.
        app.sm.children[0].ids.player_credits.text = str(app.player_stats['credits'])



        # Create copy of the current planet's commodities.
        self.__commodities_list = app.sm.children[0].planets[0].market_goods

        #self.__market_list = app.sm.children[0].ids.commodity_list.children

        self.__counter = 0

        for each in self.__commodities_list:
            self.__commodity_price = each['market'] * each['labor_value']

            #for child in app.sm.children[0].ids.commodity_list.children:
            print(app.sm.children[0].ids.commodity_list.children[self.__counter].children[0].text)
            print(app.sm.children[0].ids.commodity_list.children[self.__counter].children[1].text)
            print(app.sm.children[0].ids.commodity_list.children[self.__counter].children[2].text)
            print(app.sm.children[0].ids.commodity_list.children[self.__counter].children[3].text)
            print(app.sm.children[0].ids.commodity_list.children[self.__counter].children[4].text)
            print(app.sm.children[0].ids.commodity_list.children[self.__counter].children[5].text)
            print(app.sm.children[0].ids.commodity_list.children[self.__counter].children[6].text)
            print()
            print()
            print()

            app.sm.children[0].ids.commodity_list.children[self.__counter].children[0].text = f'$-{self.__commodity_price*100}'
            app.sm.children[0].ids.commodity_list.children[self.__counter].children[1].text = f'$-{self.__commodity_price*10}'
            app.sm.children[0].ids.commodity_list.children[self.__counter].children[2].text = f'$-{self.__commodity_price}'
            #app.sm.children[0].ids.commodity_list.children[self.__counter].children[3].text
            app.sm.children[0].ids.commodity_list.children[self.__counter].children[4].text = f'${self.__commodity_price}'
            app.sm.children[0].ids.commodity_list.children[self.__counter].children[5].text = f'${self.__commodity_price*10}'
            app.sm.children[0].ids.commodity_list.children[self.__counter].children[6].text = f'${self.__commodity_price*100}'
            print()
            print()
            print()


            print(app.sm.children[0].ids.commodity_list.children[self.__counter].children[0].text)
            print(app.sm.children[0].ids.commodity_list.children[self.__counter].children[1].text)
            print(app.sm.children[0].ids.commodity_list.children[self.__counter].children[2].text)
            print(app.sm.children[0].ids.commodity_list.children[self.__counter].children[3].text)
            print(app.sm.children[0].ids.commodity_list.children[self.__counter].children[4].text)
            print(app.sm.children[0].ids.commodity_list.children[self.__counter].children[5].text)
            print(app.sm.children[0].ids.commodity_list.children[self.__counter].children[6].text)
            print()

            self.__counter += 1

            print()

class MarketButton(NewButton):
    def getMessage(self, obj):
        print('MarketButton Pressed! It was:', obj.text)

class PlusButton(NewButton):
    pass

class MinusButton(NewButton):
    pass

class PlusMinusLabel(Label):
    pass

class PlayerStatButton(NewButton):
    def __init__(self,**kwargs):
        super(PlayerStatButton,self).__init__(**kwargs)

    def expand_contract(self):
        if self.pos[0] < self.parent.width / 2: # Collapse
            anim_x = (self.parent.width -
                      self.width -
                      self.parent.spacing)
            new_text = '<'
        elif self.pos[0] > self.parent.width / 2: # Expand
            anim_x = 0
            new_text = '>'
        anim = Animation(x=anim_x,y=0, t='in_out_quart',d=0.5)
        anim.start(self.parent)
        self.text = new_text

    def update(self,new_value):
        self.text = new_value


class InterstellarTransportCoApp(App):
    def build(self):

        self.player_stats = {
            'credits':100000,
            'cargo_capacity':100,
            'cargo_used':0
        }

        self.player_commodities = {
            'grain':0,
            'water':0,
            'bread':0,
            'ore':0,
            'energy':0,
            'fuel':0,
            'drone':0,
            'droid':0,
            'synthetic':0
        }

        self.sm = ScreenManager(transition=SlideTransition())
        self.sm.add_widget(MarketScreen(name='market'))
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(SettingsScreen(name='settings'))

        return self.sm

if __name__ == '__main__':
    app = InterstellarTransportCoApp()
    app.run()


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
