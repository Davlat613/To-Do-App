# database.py
import sqlite3

class Database:
    def __init__(self, db_name='tasks.db'):
        # Подключение к базе данных (если файла не существует, он будет создан)
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()  # Создание таблицы при инициализации

    def create_table(self):
        # Создание таблицы задач, если она не существует
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                is_do BOOLEAN NOT NULL DEFAULT 0,
                description TEXT,
                completed BOOLEAN NOT NULL DEFAULT 0,
                due_date DATE
            )
        ''')
        self.connection.commit()  # Применение изменений к базе данных

    def add_task(self, is_do, title, description, due_date=None):
        # Метод для добавления новой задачи в базу данных
        self.cursor.execute('''
            INSERT INTO tasks (title, is_do, description, due_date)
            VALUES (?, ?, ?, ?)
        ''', (title, is_do, description, due_date))
        self.connection.commit()  # Применение изменений

    def get_tasks(self):
        # Метод для получения всех задач из базы данных
        self.cursor.execute('SELECT * FROM tasks')
        return self.cursor.fetchall()  # Возвращаем все найденные задачи

    def update_task(self, task_id, completed):
        # Метод для обновления статуса задачи (выполнена или нет)
        self.cursor.execute('''
            UPDATE tasks SET completed = ? WHERE id = ?
        ''', (completed, task_id))
        self.connection.commit()  # Применение изменений

    def delete_task(self, task_id):
        """Удаляет задачу из базы данных по заданному идентификатору."""
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            self.connection.commit()


    def close(self):
        # Метод для закрытия соединения с базой данных
        self.connection.close()
