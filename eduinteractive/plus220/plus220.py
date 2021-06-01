#!/usr/bin/env python3
import sys

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner

class TestApp(App):
    
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

    def build(self):
        wid = Widget()

        self.buttons = []

        main_layout = BoxLayout(orientation='vertical')

        main_layout.add_widget(Label(text='Make a summ!'))

        layout = GridLayout(cols=10, size_hint=(1, 1))

        for j in range(2):
            for i in range(10):
                self.buttons.append(Button(text='', on_press=self.react))
                layout.add_widget(self.buttons[-1]);
        

        main_layout.add_widget(layout)

        main_layout.add_widget(Label(text='Of following numbers:'))

        args = BoxLayout()

        arg1 = Spinner(
                    text='First number',
                    values=('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))
        args.add_widget(arg1)
        args.add_widget(Label(text='+'))
        arg2 = Spinner(
                    text='Second number',
                    values=('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))
        args.add_widget(arg2)

        main_layout.add_widget(args)

        return main_layout

TestApp().run()


class CounterButton():

    def __init__(self, name = '', parent=None):
        QWidget.__init__(self, name, parent)

        self.clicked.connect(self.btn_click)

        self.MODE_RED = 1
        self.MODE_GREEN = 2
        self.MODE_NONE = 0
        self.mode = self.MODE_NONE

        self.setStyleSheet("CounterButton::mode == 1 {background-color: red;}"
                           "CounterButton::mode == 0 {background-color: white;}"
                           "CounterButton::mode == 2 {background-color: green;}"
                           )


    def btn_click(self, pressed):
        target_btn = self.sender()
        print("YEAP: ", target_btn)
        if target_btn.mode == target_btn.MODE_NONE:
            target_btn.mode = target_btn.MODE_RED
        elif target_btn.mode == target_btn.MODE_RED:
            target_btn.mode = target_btn.MODE_GREEN
        else:
            target_btn.mode = target_btn.MODE_NONE
        print("MODE: %d" % target_btn.mode)


#app = QApplication(sys.argv)

#window = QWidget()
#window.setWindowTitle('PyQt5 App')
#window.setGeometry(100, 100, 880, 280)
#window.move(60, 15)
#helloMsg = QLabel('<h1>Hello World!</h1>', parent=window)
#helloMsg.move(60, 15)
#
#btns = []



# The counter table
def init_counter():
    btn_w = 50
    btn_h = 50
    for j in range(2):
        for i in range(10):
            btn = CounterButton('', parent=window)
            btn.resize(btn_w,btn_h)
            btn.move(10 + btn_w * i, 10 + btn_w * j)

            btns.append(btn)

#arg1 = QSpinBox(parent=window)
#arg1.move(20, 140)
#arg2 = QSpinBox(parent=window)
##arg2.move(150, 140)
#
#init_counter()
#
#window.show()
#
#sys.exit(app.exec_())

