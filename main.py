from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Rectangle
from kivy.graphics import Color
from database import Database


class TaskContainer(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.db = Database()
        # Пример списка
        tasks = self.db.get_tasks()

        # Метод для добавления пунктов
        self.add_task_options(tasks)

    def add_task_options(self, tasks):
        for task in tasks:
            # Создаём новый GridLayout для каждого пункта
            task_layout = GridLayout(cols=3, size_hint_y=None, height=40)

            # Добавляем фон для task_layout с помощью canvas.before
            with task_layout.canvas.before:
                Color(0.25, 0.25, 0.25, 1)  # Серый фон
                task_layout.rect = Rectangle(pos=task_layout.pos, size=task_layout.size)


            # Обновляем позицию и размер фона при изменении task_layout
            task_layout.bind(pos=self.update_rect, size=self.update_rect)

            # Добавляем чекбокс
            checkbox = CheckBox(size_hint_x=0.1)
            task_layout.add_widget(checkbox)

            # Добавляем метку с названием задачи
            label = Label(text=task[1],
                          size_hint_x=0.8)
            task_layout.add_widget(label)
            
            

            # Добавляем кнопку "More"
            button = Button(text='...', size_hint_x=0.1)
            button.bind(on_press=self.callback_function)
            task_layout.add_widget(button)

            # Добавляем этот layout в основной GridLayout
            self.add_widget(task_layout)

    def update_rect(self, instance, value):
    # Обновляем позицию и размер прямоугольника
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size


    def callback_function(self, instance):
        print("More button pressed!")


class Root(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        task_container = TaskContainer()
        self.add_widget(task_container)

class MyApp(App):
    def build(self):
        Window.size = (393, 852)
        
        return Root()


if __name__ == "__main__":
    MyApp().run()
