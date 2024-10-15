from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle, Color
from database import Database


class SettingsBar(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TaskContainer(GridLayout):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.checkboxes = {}
        self.update_task_list()

    def update_task_list(self):
        """Обновляет список задач."""
        self.clear_widgets()
        for task in self.db.get_tasks():
            self.add_task_widget(task)

    def add_task_widget(self, task):
        """Добавляет виджет задачи в контейнер."""
        task_layout = GridLayout(cols=3, size_hint_y=None, height=40)
        with task_layout.canvas.before:
            Color(0.25, 0.25, 0.25, 1)
            task_layout.rect = Rectangle(pos=task_layout.pos, size=task_layout.size)

        task_layout.bind(pos=self.update_rect, size=self.update_rect)

        checkbox = CheckBox(size_hint_x=0.1)
        checkbox.bind(active=lambda checkbox, value, task_id=task[0]: self.on_checkbox_active(task_id, value))
        task_layout.add_widget(checkbox)
        self.checkboxes[task[0]] = checkbox

        label = Label(text=task[1], size_hint_x=0.8)
        task_layout.add_widget(label)

        button = Button(text='...', size_hint_x=0.1)
        button.bind(on_press=self.callback_function)
        task_layout.add_widget(button)

        self.add_widget(task_layout)

    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def on_checkbox_active(self, task_id, value):
        if value:
            self.remove_task(task_id)

    def remove_task(self, task_id):
        self.db.delete_task(task_id)
        self.update_task_list()  # Обновляем отображение задач

    def callback_function(self, instance):
        print("More button pressed!")


class Root(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.settings_bar = SettingsBar()
        self.task_container = TaskContainer(self.db)
        
        self.add_widget(self.task_container)

    def add_task(self):
        title = self.ids.input_field.text
        if title:
            self.db.add_task(title, 'placeholder description')
            self.ids.input_field.text = ''
            self.task_container.update_task_list()

    def display_settings(func):
        def wrapper(self, is_show):
            if is_show and self.settings_bar not in self.children:
                self.add_widget(self.settings_bar)
            elif not is_show and self.settings_bar in self.children:
                self.remove_widget(self.settings_bar)
            return func(self, is_show)  # Вызов оригинальной функции
        return wrapper


    @display_settings
    def toggle_settings(self, is_show):
        """Переключает отображение панели настроек."""
        pass  # Логика для других действий при переключении


class MyApp(App):
    def build(self):
        Window.size = (393, 852)
        return Root()


if __name__ == "__main__":
    MyApp().run()
