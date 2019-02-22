
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivy.graphics.vertex_instructions import (Line, Ellipse, Rectangle)
from kivy.graphics.context_instructions import Color
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import random
from kivy.lang import Builder

Builder.load_string("""

<Button>:
    isX: False
    isO: False
    isavail: True
    
    
<WelcomeScreen>:
    name: 'welcomescreen'
    BoxLayout:
        orientation: 'vertical'
        FloatLayout:
            size_hint: None, None
            size:root.width, 0.4*root.height
            
            canvas:
                Color:
                    rgba: 1,1,1,0.5
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                size_hint: None, None
                text: 'Welcome to TicTacToe'
                center: self.parent.center
                font_size: '50sp'
                size: self.texture_size
        FloatLayout:
            BoxLayout:
                center: self.parent.center
                orientation: 'vertical'
                Button:
                    id: human_button
                    size_hint: None, None
                    size: 0.2*root.width, 0.1*root.height
                    text: '1 vs 1'
                    font_size: '20sp'
                    on_press: app.root.current = 'gamescreen'
                Button:
                    id: ai_button
                    size_hint: None, None
                    size: 0.2*root.width, 0.1*root.height
                    text: '1 vs Bot'
                    font_size: '20sp'
                    on_press: app.root.current = 'gamescreen'
                    on_press: root.aioption = True
<GameScreen>:
    name: 'gamescreen'
    BoxLayout:
        orientation: 'vertical'
        FloatLayout:
            id: myfloat
            size_hint_y: None
            height: 0.2*root.height
            Label:
                id: game_label
                center: self.parent.center
                size_hint_x: None
                width: 0.8*root.width
                color: 0,0,1,0.85
                text: "X's turn"
                font_size: '35sp'
                
        GridLayout:
            id: mygrid
            cols: 3
            rows: 3
            padding: 0.05*root.width
            spacing: 0.02*root.width
            Button:
                id: button1
                background_color: 0,0,0,0
                
                canvas:
                    Color:
                        rgba: 1,1,1,0.8
                    Rectangle:
                        pos: (self.width + self.x), (root.y+0.025*root.width)
                        size: (0.02*root.width), (mygrid.height-0.05*root.width)
                on_press: root.sign(self)
            Button:
                id: button2
                background_color: 0,0,0,0
                
                canvas:
                    Color:
                        rgba: 1,1,1,0.8
                    Rectangle:
                        pos: (self.width + self.x), (root.y+0.025*root.width)
                        size: (0.02*root.width), (mygrid.height-0.05*root.width)
                on_press: root.sign(self)
            Button:
                id: button3
                background_color: 0,0,0,0
                
                on_press: root.sign(self)
                canvas:
                    Color:
                        rgba: 1,0,1,1
            Button:
                id: button4
                background_color: 0,0,0,0
                
                on_press: root.sign(self)
                canvas:
                    Color:
                        rgba: 1,1,1,0.8
                    Rectangle:
                        pos: (root.x + 0.025*root.width) , (self.y + self.height)
                        size: (mygrid.width - 0.05*root.width) , (0.02*root.width)
                    Rectangle:
                        pos: (root.x + 0.025*root.width) , (self.y - 0.02*root.width)
                        size: (mygrid.width - 0.05*root.width) , (0.02*root.width)
            Button:
                id: button5
                background_color: 0,0,0,0
                
                on_press: root.sign(self)
                canvas:
                    Color:
                        rgba: 1,0,0,1
            Button:
                id: button6
                background_color: 0,0,0,0
                
                on_press: root.sign(self)
                canvas:
                    Color:
                        rgba: 1,0,0,1
            Button:
                id: button7 
                background_color: 0,0,0,0
                
                on_press: root.sign(self)
                canvas:
                    Color:
                        rgba: 1,0,0,1
            Button:
                id: button8
                background_color: 0,0,0,0
                
                on_press: root.sign(self)
                canvas:
                    Color:
                        rgba: 1,0,0,1
            Button:
                id: button9
                background_color: 0,0,0,0
                
                on_press: root.sign(self)
                canvas:
                    Color:
                        rgba: 1,0,0,1


	""")
# I set a global variable becasue i dont know how to change another screen/class variable using the first screen

aioption = BooleanProperty(False)

class WelcomeScreen(Screen):
    
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        self.set_aioption()
        
    def set_aioption(self):
        button = self.ids.ai_button
        button.bind(on_press = self.option_true)
        
    def option_true(self, *args):
        global aioption
        aioption = True
        # for debugging porpuses
        print('success in changing global variable')

class WinnerPopup(Popup):
    pass


class GameScreen(Screen):
    #defining all variables we need
    
    global aioption
    turn = 1
    checking_threshold = 0
    isX = BooleanProperty(False)
    isO = BooleanProperty(False)
    result = StringProperty('')
    # this checks if a button is used or not
    isavail = BooleanProperty(True)
    haswon = BooleanProperty(False)
    
    def drawX(self, button):
            # creates the X sign
            with self.canvas.after:
                Color(0,0,0.5,1)
                Line(points = [button.x, button.y, button.x+button.width, button.y+button.height], width = 0.03*button.width)
                Line(points = [button.x+button.width, button.y, button.x, button.y+button.height], width = 0.03*button.width)
                
    def drawO(self, button):
            #draws the O sign
            with self.canvas.after:
                Color(0.5,0,0,1)
                Line(width = 0.03*button.width, circle = (button.center_x, button.center_y, min(button.width, button.height)
                    / 2))
        
    def winning(self, result):
            
        #handles popup at the end
        
        box = BoxLayout(orientation = 'vertical')
        play_btn = Button(text= 'play again', font_size = '20sp')
        exit_btn = Button(text = 'exit', font_size = '20sp')
        winner_label = Label(text= result,
                             font_size= '30sp')
        wp = WinnerPopup(title = 'Winner',
                         id = 'mypopup'
                         , size_hint_y = None, size_hint_x= None
                         , size=(0.5*self.width, 0.5*self.height),
                         auto_dismiss = False)
        
        play_btn.bind(on_press = self.reset_game)
        play_btn.bind(on_press = self.change_welcome)
        play_btn.bind(on_press = wp.dismiss)
        exit_btn.bind(on_press = self.exit_app)
        wp.add_widget(box)
        box.add_widget(winner_label)
        box.add_widget(play_btn)
        box.add_widget(exit_btn)
        
        wp.open()

    def exit_app(self, *args):
        App.get_running_app().stop()
        Window.close()

    def change_welcome(self, *args):
        self.manager.current = 'welcomescreen'

    def check_winner(self):
        b1 = self.ids.button1
        b2 = self.ids.button2
        b3 = self.ids.button3
        b4 = self.ids.button4
        b5 = self.ids.button5
        b6 = self.ids.button6
        b7 = self.ids.button7
        b8 = self.ids.button8
        b9 = self.ids.button9
        
        #checks for winning conditions
        
        if ((b1.isX == True and b2.isX == True and b3.isX == True)
        or (b1.isX == True and b4.isX == True and b7.isX == True)
        or (b1.isX == True and b5.isX == True and b9.isX == True)
        or (b2.isX == True and b5.isX == True and b8.isX == True)
        or (b3.isX == True and b6.isX == True and b9.isX == True)
        or (b4.isX == True and b5.isX == True and b6.isX == True)
        or (b7.isX == True and b8.isX == True and b9.isX == True)
        or (b3.isX == True and b5.isX == True and b7.isX == True)):
            
            self.haswon = True
            self.result = "X's won"
            self.winning(self.result)
        
        elif ((b1.isO == True and b2.isO == True and b3.isO == True)
        or (b1.isO == True and b4.isO == True and b7.isO == True)
        or (b1.isO == True and b5.isO == True and b9.isO == True)
        or (b2.isO == True and b5.isO == True and b8.isO == True)
        or (b3.isO == True and b6.isO == True and b9.isO == True)
        or (b4.isO == True and b5.isO == True and b6.isO == True)
        or (b7.isO == True and b8.isO == True and b9.isO == True)
        or (b3.isO == True and b5.isO == True and b7.isO == True)):
            
            self.haswon = True
            self.result = "O's won"
            self.winning(self.result)
            
        elif self.checking_threshold >= 8:
            
            self.result = 'it is a draw'
            self.winning(self.result)
            
    def reset_game(self, *args):
        self.turn = 1
        self.checking_threshold = 0
        self.result = ''
        self.haswon = False
        global aioption
        aioption = False
        for i in range(1,10):
            self.ids[f'button{i}'].isX = False
            self.ids[f'button{i}'].isO = False
            self.ids[f'button{i}'].isavail = True
            
        self.canvas.after.clear()
        
    def do_nothing(self):
        pass
        
    def ai_engine(self, *args):
        label = self.ids.game_label
        flag = False
        while flag == False and self.turn % 2 == 0:        
            random_int = random.randint(1, 9)
            button = self.ids[f'button{random_int}']
    
            if button.isavail == True:
                button.isO = True
                label.text = "it's X's turn"
                label.color = [0,0,0.5,1]
                self.drawO(button)
                flag = True
                self.turn += 1
                button.isavail = False
                self.checking_threshold += 1

                
    # condition that changes the game mode                
    def sign(self, button):
        if aioption == True:
            label = self.ids.game_label
            #makes sure match cant go on when game is over
            if self.haswon != True:
                if button.isavail == True:
                    if self.turn % 2 != 0:
                        self.drawX(button)
                        label.text = "it's AI's turn"
                        label.color = [0.5,0,0,1]
                        button.isX = True
                        self.turn += 1
                        button.isavail = False
                        self.checking_threshold += 1
                        self.ai_engine()
                        
                    if self.checking_threshold >= 3:
                        self.check_winner()
                    
                    
                    
                else: 
                    print('the button is not available')
        else:
            label = self.ids.game_label
            if self.haswon != True:
                if button.isavail == True:
                    if self.turn % 2 != 0:
                        self.drawX(button)
                        label.text = "it's O's turn"
                        label.color = [0.5,0,0,1]
                        button.isX = True
                    else:
                        button.isO = True
                        label.text = "it's X's turn"
                        label.color = [0,0,0.5,1]
                        self.drawO(button)
                        
                    if self.checking_threshold >= 4:
                        self.check_winner()
                        
                    button.isavail = False
                    self.turn += 1
                    self.checking_threshold += 1
                    
        
                else: 
                    print('the button is not available')
                

class TicTacToe2App(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen())
        sm.add_widget(GameScreen(name = 'gamescreen'))
        return sm
    
if __name__ == '__main__':
    TicTacToe2App().run()
    