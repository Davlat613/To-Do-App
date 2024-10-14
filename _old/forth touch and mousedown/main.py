from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics import Color


class TouchInput(Widget):
    def __init__(self, **kwargs):
        super(TouchInput, self).__init__(**kwargs)

        with self.canvas:
            self.rect = Rectangle(pos=(0, 0), size=(50, 50))

    def on_touch_down(self, touch):
        print("Mouse down", touch)
        return super().on_touch_down(touch)
    
    def on_touch_move(self, touch):
        print("Mouse move", touch)
    
    def on_touch_up(self, touch):
        print("Mouse up", touch)

class MyApp(App):
    def build(self):
        return TouchInput()
    

if __name__ == "__main__":
    MyApp().run()