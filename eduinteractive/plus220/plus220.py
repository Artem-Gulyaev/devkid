#!/usr/bin/env python3
import sys

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.config import Config
from kivy.core.window import Window

#Window.size = (1900, 1100)

class TestApp(App):

    def __init__(self):
        App.__init__(self)

        self.font_size = 40
    
    def react(self, a):
        if not hasattr(a, "mode"):
            a.mode = 'white'
        if a.mode == 'green':
            a.background_color = [1, 0, 0, 1]
            a.mode = 'red'
        elif a.mode == 'red':
            a.background_color = [1, 1, 1, 1]
            a.mode = 'white'
        elif a.mode == 'white':
            a.background_color = [0, 1, 0, 1]
            a.mode = 'green'

    def check_answer(self, target):
        a = 0
        b = 0

        try:
            a = int(self.arg1.text)
        except:
            print("Please select the first argument.")
            return
        try:
            b = int(self.arg2.text)
        except:
            print("Please select the second argument.")
            return

        print("Case: %d + %d" % (a, b))

        result = True
        for i in range(20):
            btn = self.buttons[i]
            if not hasattr(btn, 'mode'):
                btn.mode = 'white'

            if i < a:
                if btn.mode != 'red':
                    print("FAILED! At pos: %d. Expected: 'red', actual: '%s'" % (i, btn.mode))
                    btn.text = "X"
                    result = False
                else:
                    btn.text = ""
            elif i < a + b:
                if btn.mode != 'green':
                    print("FAILED! At pos: %d. Expected: 'green', actual: '%s'" % (i, btn.mode))
                    btn.text = "X"
                    result = False
                else:
                    btn.text = ""
            else:
                if btn.mode != 'white':
                    print("FAILED! At pos: %d. Expected: 'white', actual: '%s'" % (i, btn.mode))
                    btn.text = "X"
                    result = False
                else:
                    btn.text = ""

        if (a + b) // 10 == 0:
            if self.answer1.text != "" and self.answer1.text != "0":
                print("FAILED! At first digit of the answer. Expected:"
                      " '0' or empty, actual: '%s'" % (self.answer1.text))
                self.answer1.background_color = [1.0, 0.2, 0.2, 1.0]
                result = False
        else:
            if self.answer1.text != str((a + b) // 10):
                print("FAILED! At first digit of the answer. Expected:"
                      " '%d' , actual: '%s'" % ((a + b) // 10, self.answer1.text))
                self.answer1.background_color = [1.0, 0.2, 0.2, 1.0]
                result = False

        if self.answer2.text != str((a + b) % 10):
            print("FAILED! At second digit of the answer. Expected:"
                  " '%d' , actual: '%s'" % ((a + b) % 10, self.answer2.text))
            self.answer2.background_color = [1.0, 0.2, 0.2, 1.0]
            result = False
        
        if result:
            self.check_button.background_color = [0.3, 0.3, 1.0, 1.0]
        else:
            self.check_button.background_color = [1.0, 0.2, 0.2, 1.0]

        return result


    def build(self):
        wid = Widget()

        self.buttons = []

        main_layout = BoxLayout(orientation='vertical')

        main_layout.add_widget(Label(text='Make a summ!', font_size=self.font_size))

        layout = GridLayout(cols=10, size_hint=(1, 1))

        for j in range(2):
            for i in range(10):
                self.buttons.append(Button(text='', on_press=self.react))
                layout.add_widget(self.buttons[-1]);
        

        main_layout.add_widget(layout)

        main_layout.add_widget(Label(text='Of following numbers:', font_size=self.font_size))

        args = BoxLayout()

        self.arg1 = Spinner(
                    text='First\nnumber',
                    values=('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
                    , font_size=self.font_size
                    , color=[1,0,0,1])
        args.add_widget(self.arg1)
        args.add_widget(Label(text='+', font_size=self.font_size))
        self.arg2 = Spinner(
                    text='Second\nnumber'
                    , values=('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
                    , font_size=self.font_size
                    , color=[0,1,0,1])
        args.add_widget(self.arg2)

        main_layout.add_widget(args)

        main_layout.add_widget(Label(text='=', font_size=self.font_size))

        answer = BoxLayout()

        self.answer1 = Spinner(
                    text=''
                    , values=('', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
                    , font_size=self.font_size)
        answer.add_widget(self.answer1)

        self.answer2 = Spinner(
                    text=''
                    , values=('', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
                    , font_size=self.font_size)
        answer.add_widget(self.answer2)
        answer.size_hint = (0.2, None)
        answer.pos_hint = {'center_x': 0.5}

        main_layout.add_widget(answer)

        self.check_button = Button(text='', on_press=self.check_answer)

        main_layout.add_widget(Label(text='And check the result!'
                                     , font_size=self.font_size, color=[1,0,0,1]))
        main_layout.add_widget(self.check_button)

        main_layout.size_hint = (1.0, 1.0)

        return main_layout

TestApp().run()

