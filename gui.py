import tkinter as tk
from start_screen import StartScreen  # Импортируем класс для стартового экрана
from main import ExerciseApp  # Импортируем класс с основной логикой упражнений

def start_gui():
    # Создаем окно приложения
    window = tk.Tk()
    window.title("Exercise Reminder")

    # Создаем экземпляр StartScreen, передавая нажатие кнопки в метод
    start_screen = StartScreen(window, on_start=lambda: start_exercises(window, start_screen))

    # Запуск главного цикла приложения
    window.mainloop()

def start_exercises(window, start_screen):
    # Удаляем стартовую страницу
    start_screen.destroy()

    # Создаем экземпляр приложения упражнений
    app = ExerciseApp(window)

# Для тестирования
if __name__ == "__main__":
    start_gui()
