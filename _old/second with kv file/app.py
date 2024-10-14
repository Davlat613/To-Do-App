from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

class MyGrid(Widget):
    name = ObjectProperty(None)
    email = ObjectProperty(None)

    def btn(self):
        print(f"Name: {self.name.text}, Email: {self.email.text}")
        self.name.text = ""
        self.email.text = ""

class MyApp(App):
    def build(self):
        return MyGrid()
    

if __name__ == "__main__":
    MyApp().run()