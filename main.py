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

import month_names

import random
import re
import datetime

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
        self.id = app.planet_count
        app.planet_count += 1

        self.__year = random.randint(2030,2149)

        self.__month = random.randint(1,12)

        # Randomly select a day within the parameters of the month.
        if self.__month == 2:
            # Leap years get the leap day as a possibility
            if ((self.__year%400==0) or (self.__year%100!=0) and (self.__year%4==0)):
                self.__day = random.randint(1,29)
            else:
                self.__day = random.randint(1,28)
        elif self.__month == 4 or self.__month == 6 or self.__month == 9 or self.__month == 11:
            self.__day = random.randint(1,30)
        else:
            self.__day = random.randint(1,31)

        self.founding_est_date = datetime.datetime(
                                            self.__year, #YEAR
                                            self.__month, #MONTH
                                            self.__day, #DAY
                                            )

        self.temp_rotation = random.choices( # x00
                                    [0,1,2,3,4,5,6,7,8,9],
                                    weights=[256,16,8,7,6,5,4,3,2,1],
                                    k=1
                                    ) + random.choices( # 0x0
                                    [0,1,2,3,4,5,6,7,8,9],
                                    weights=[6,8,20,5,4,3,2,1,1,1],
                                    k=1
                                    ) + random.choices( # 00x
                                    [1,2,3,4,5,6,7,8,9],
                                    weights=[1,1,1,1,1,1,1,1,1],
                                    k=1
                                    )

        self.rotation_in_hours = int(str(self.temp_rotation[0]) + str(self.temp_rotation[1]) + str(self.temp_rotation[2]))

        self.temp_phase = random.choices( # x00
                                    [0,1,2,3,4,5,6,7,8,9],
                                    weights=[256,16,8,7,6,5,4,3,2,1],
                                    k=1
                                    ) + random.choices( # 0x0
                                    [0,1,2,3,4,5,6,7,8,9],
                                    weights=[4,6,8,20,6,4,3,2,1,1],
                                    k=1
                                    ) + random.choices( # 00x
                                    [1,2,3,4,5,6,7,8,9],
                                    weights=[1,1,1,1,1,1,1,1,1],
                                    k=1
                                    )

        self.phase_in_days = int(str(self.temp_phase[0]) + str(self.temp_phase[1]) + str(self.temp_phase[2]))

        self.temp_orbit = random.choices( # x000
                                [0,1,2,3,4,5,6,7,8,9],
                                weights=[2044,256,128,64,32,16,8,4,2,1],
                                k=1
                                ) + random.choices( # 0x00
                                [0,1,2,3,4,5,6,7,8,9],
                                weights=[2,4,8,10,8,6,4,3,2,1],
                                k=1
                                ) + random.choices( # 00x0
                                [0,1,2,3,4,5,6,7,8,9],
                                weights=[1,1,2,3,4,5,5,5,4,3],
                                k=1
                                ) + random.choices( # 000x
                                [1,2,3,4,5,6,7,8,9],
                                weights=[1,1,1,1,1,1,1,1,1],
                                k=1
                                )

        self.orbit_in_days = int(str(self.temp_orbit[0]) +         str(self.temp_orbit[1]) + str(self.temp_orbit[2]) + str(self.temp_orbit[3]))


        self.__number_of_months = self.orbit_in_days // self.phase_in_days
        self.__lunisolar_leftovers = self.orbit_in_days % self.phase_in_days
        self.__each_month_add = 0

        if self.__number_of_months == 0:
            print('0 months')
        else:
            # Calculate how many days added to each month
            while self.__lunisolar_leftovers >= self.__number_of_months:
                self.__each_month_add += 1
                self.__lunisolar_leftovers -= self.__number_of_months

            # If there are leftovers, figure out how they should be spaced.
            if self.__lunisolar_leftovers > 0:
                self.__month_spacing = round(self.__number_of_months /     self.__lunisolar_leftovers)


        self.months = []
        self.__temp_month_names = month_names.list
        self.__specific_month_add = 0

        for month in range(self.__number_of_months):
            # if month is one of the properly spaced months, add a day to it and remove a leftover day from the list.
            if self.__lunisolar_leftovers > 0 and (month + 1) % self.__month_spacing == 0:
                self.__lunisolar_leftovers -= 1
                self.__specific_month_add = 1
            else:
                self.__specific_month_add = 0

            # Put any remaining leftover days in the last month of the year.
            if (month + 1) == self.__number_of_months and self.__lunisolar_leftovers > 0:
                self.__specific_month_add += self.__lunisolar_leftovers



            self.months.append(
                {
                'name':self.__temp_month_names[month][random.randint(0,len(self.__temp_month_names[month])-1)],
                'days':(self.phase_in_days + self.__each_month_add + self.__specific_month_add)
                }

            )

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

        # Populate the list of planets.
        for i in range(80000):
            self.__temp_len = len(planet_possible_goods) - 1
            self.__selec = random.randint(0,self.__temp_len)
            app.planets.append(Planet(planet_possible_goods[self.__selec]))

    def add_buttons(self, planet):
        app.local_clock = '1234-01-01 00:00:00'

        # Update the Local Planet Time.
        app.sm.children[0].ids.local_planet_time.text = 'Local Planet Time: ' + str(app.local_clock)


        children_count = len(planet.market_goods)
        current_size_x = self.ids.commodity_list.size[0]

        # Update the list size to fill each market button.
        self.ids.commodity_list.size = (current_size_x, (children_count + 1) * 60)

        temp_box_layout = BoxLayout(orientation='horizontal',spacing=20)
        temp_box_layout.add_widget(BuySellLabel(text='Buy 100'))
        temp_box_layout.add_widget(BuySellLabel(text='Buy 10'))
        temp_box_layout.add_widget(BuySellLabel(text='Buy 1'))
        temp_box_layout.add_widget(Label(text='Commodity',color=('4774A2'),font_size=30))
        temp_box_layout.add_widget(BuySellLabel(text='Sell 1'))
        temp_box_layout.add_widget(BuySellLabel(text='Sell 10'))
        temp_box_layout.add_widget(BuySellLabel(text='Sell 100'))


        self.ids.commodity_list.add_widget(temp_box_layout)

        for each in planet.market_goods:
            price = each['market'] * each['labor_value']

            temp_box_layout = BoxLayout(orientation='horizontal',spacing=20)

            temp_box_layout.add_widget(Buy100(text=f'$-{price*100}'))
            temp_box_layout.add_widget(BuyTen(text=f'$-{price*10}'))
            temp_box_layout.add_widget(BuyOne(text=f'$-{price}'))

            temp_box_layout.add_widget(MarketButton(text=each['name']))

            temp_box_layout.add_widget(SellOne(text=f'${price}'))
            temp_box_layout.add_widget(SellTen(text=f'${price*10}'))
            temp_box_layout.add_widget(Sell100(text=f'${price*100}'))

            self.ids.commodity_list.add_widget(temp_box_layout)

        # Create the player cargo panel.
        NewButton().player_cargo_panel_resize('grain')

class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class MyScreenManager(ScreenManager):
    pass

class NewButton(Button):
    def __init__(self,**kwargs):
        super(Button,self).__init__(**kwargs)

    def player_cargo_panel_resize(self,commodity):

        self.__current_commodity = 0

        self.__temp_player_cargo = [i.text.split(':')[0].lower() for i in app.sm.children[0].ids.player_cargo.parent.children]

        if app.player_commodities[commodity.lower()]['count'] > 0:
            try:
                self.__x = self.__temp_player_cargo.index(commodity.lower())

                app.sm.children[0].ids.player_cargo.parent.children[self.__x].text = commodity + ': ' + str(app.player_commodities[commodity.lower()]['count'])
            except:
                app.sm.children[0].ids.player_cargo.parent.add_widget(Label(text= commodity + ': ' + str(app.player_commodities[commodity.lower()]['count'])))
        else:
            try:
                self.__x = self.__temp_player_cargo.index(commodity.lower())

                app.sm.children[0].ids.player_cargo.parent.remove_widget(app.sm.children[0].ids.player_cargo.parent.children[self.__x])
            except:
                print('player_cargo_panel_resize exception')

        anim = Animation(size=(400, (len(app.sm.children[0].ids.player_cargo.parent.children)) * 50),t='out_back',d=0.5)
        anim.start(app.sm.children[0].ids.player_cargo.parent)


    def make_transaction(self, commodity, value, amount):
        # Remove the '$' from the text string and convert it to an integer.
        self.temp_commodity_value = int(re.sub('[$]','',str(value)))

        # Not enough Credits.
        if (app.player_stats['credits'] + self.temp_commodity_value) < 0:
            return

        # Not enough Capacity.
        elif (app.player_stats['cargo_capacity'] - app.player_stats['cargo_used']) < amount:
            return

        # Not enough of commodity in player_commodites.
        elif (app.player_commodities[commodity.lower()]['count'] + amount) < 0:
            return

        # Update player credits stat.
        app.player_stats['credits'] += self.temp_commodity_value

        # Update player commodities by amount purchased/sold
        app.player_commodities[commodity.lower()]['count'] += amount

        # Update the player credits button to match the stat.
        app.sm.children[0].ids.player_credits.text = str(app.player_stats['credits'])

        # Update all the player stats..
        app.update_stats()

        # Update the player_cargo stats.
        app.sm.children[0].ids.player_cargo.text = 'total: ' + str(app.player_stats['cargo_used']) + '/' + str(app.player_stats['cargo_capacity'])

        # Create copy of the current planet's commodities.
        self.__commodities_list = app.planets[0].market_goods

        # Update Cargo panel width.
        self.player_cargo_panel_resize(commodity)

        # Calculate how long the transaction took.
        if amount > 0:
            self.__transaction_time = 60 + ((600 * amount) / app.player_stats['buying_skill'])
        elif amount < 0:
            self.__transaction_time = 60 + ((600 * abs(amount)) / app.player_stats['selling_skill'])


        # Update the clock by the time taken to make the transaction.
        app.advance_time(round(self.__transaction_time))


class MarketButton(NewButton):
    def getMessage(self, obj):
        print('MarketButton Pressed! It was:', obj.text)

class BuyButton(NewButton):
    pass

class Buy100(BuyButton):
    pass

class BuyTen(BuyButton):
    pass

class BuyOne(BuyButton):
    pass

class SellButton(NewButton):
    pass

class Sell100(SellButton):
    pass

class SellTen(SellButton):
    pass

class SellOne(SellButton):
    pass

class BuySellLabel(Label):
    pass

class PlayerStatButton(NewButton):
    def __init__(self,**kwargs):
        super(PlayerStatButton,self).__init__(**kwargs)

    def expand_contract_bar(self):
        if self.pos[0] < self.parent.width / 2: # Collapse
            anim_x = (self.parent.width -
                      self.width -
                      self.parent.spacing)
            new_text = '<'
        elif self.pos[0] > self.parent.width / 2: # Expand
            anim_x = 0
            new_text = '>'
        anim = Animation(x=anim_x,y=0, t='in_out_quart',d=0.5)
        anim.start(app.sm.children[0].children[0].children[1].children[0])
        print(app.sm.children[0].children[0].children[1].children[0].canvas)
        self.text = new_text

    def update(self,new_value):
        self.text = new_value


class InterstellarTransportCoApp(App):
    def build(self):
        app.planets = []
        app.planet_count = 0

        self.player_stats = {
            'credits':100000,
            'cargo_capacity':1000,
            'cargo_used':0,
            'buying_skill':20,
            'selling_skill':1
        }

        self.player_commodities = {
            'grain':{'count':0,'in_cargo_panel':False},
            'water':{'count':0,'in_cargo_panel':False},
            'bread':{'count':0,'in_cargo_panel':False},
            'ore':{'count':0,'in_cargo_panel':False},
            'energy':{'count':0,'in_cargo_panel':False},
            'fuel':{'count':0,'in_cargo_panel':False},
            'drone':{'count':0,'in_cargo_panel':False},
            'droid':{'count':0,'in_cargo_panel':False},
            'synthetic':{'count':0,'in_cargo_panel':False},
        }

        # The game_clock represents Earth Standard Time
        self.earth_clock = datetime.datetime(2150,1,1)
        self.local_clock = '0000-01-01 00:00:00'


        self.sm = ScreenManager(transition=SlideTransition())
        self.sm.add_widget(MarketScreen(name='market'))
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(SettingsScreen(name='settings'))

        return self.sm

    def update_stats(self):
        self.player_stats['cargo_used'] = 0
        for each in self.player_commodities:
            self.player_stats['cargo_used'] += self.player_commodities[each]['count']

    def advance_time(self, ticks):
        self.earth_clock += datetime.timedelta(seconds=ticks)

        app.sm.children[0].ids.earth_standard_time.text = 'Earth Standard Time: ' + str(self.earth_clock)

        self.local_clock = self.local_time_advance(ticks)

        #self.local_clock += datetime.timedelta(seconds=ticks)

        app.sm.children[0].ids.local_planet_time.text = 'Local Planet Time: ' + str(self.local_clock)

    def local_time_advance(self,ticks):
        self.__ticks = ticks
        self.__temp_year = ''
        self.__temp_month = ''
        self.__temp_day = ''
        self.__temp_hour = ''
        self.__temp_minutes = ''
        self.__temp_seconds = ''
        self.__temp_date_counter = 0

        for each in self.local_clock:
            if each == '-' or each == ':' or each == ' ':
                self.__temp_date_counter += 1
            elif self.__temp_date_counter == 0:
                self.__temp_year += each
            elif self.__temp_date_counter == 1:
                self.__temp_month += each
            elif self.__temp_date_counter == 2:
                self.__temp_day += each
            elif self.__temp_date_counter == 3:
                self.__temp_hour += each
            elif self.__temp_date_counter == 4:
                self.__temp_minutes += each
            elif self.__temp_date_counter > 4:
                self.__temp_seconds += each

        # Add to minutes and take from ticks until under 60
        while self.__ticks >= 60:
            self.__temp_minutes = str(int(self.__temp_minutes) + 1)
            self.__ticks -= 60

        # Add remaining ticks to the seconds counter.
        self.__temp_seconds = str(int(self.__temp_seconds) + self.__ticks)

        # Add minutes over 60 to hours.
        while int(self.__temp_minutes) >= 60:
            self.__temp_hour = str(int(self.__temp_hour) + 1)
            self.__temp_minutes = str(int(self.__temp_minutes) - 60)

        # Add hours over the planetary rotation to the days.
        while int(self.__temp_hour) >= app.planets[0].rotation_in_hours:
            self.__temp_day = str(int(self.__temp_day) + 1)
            self.__temp_hour = str(int(self.__temp_hour) - app.planets[0].rotation_in_hours)

        # Add days over the phase length to the month.
        while int(self.__temp_day) >= app.planets[0].phase_in_days:
            self.__temp_month = str(int(self.__temp_month) + 1)
            self.__temp_day = str(int(self.__temp_day) - app.planets[0].phase_in_days)

        # Add months over the orbit length to the year.
        while int(self.__temp_day) >= app.planets[0].orbit_in_days:
            self.__temp_year = str(int(self.__temp_year) + 1)
            self.__temp_day = str(int(self.__temp_day) - app.planets[0].orbit_in_days)





        self.__temp_value = self.__temp_year + '-' + self.__temp_month + '-' + self.__temp_day + ' ' + self.__temp_hour + ':' + self.__temp_minutes + ':' + self.__temp_seconds

        return self.__temp_value


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
