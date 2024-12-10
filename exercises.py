# Импортируем необходимые библиотеки и классы
import tkinter as tk
from itertools import cycle
from PIL import Image, ImageTk
from threading import Thread
from tkinter import simpledialog

class Exercise:
    def __init__(self, name, image, duration, repeats=1):
        self.name = name  # Название упражнения
        self.image = image  # Путь к изображению
        self.duration = duration  # Длительность выполнения (в секундах)
        self.repeats = repeats  # Количество повторений

    def __repr__(self):
        return f"{self.name} - {self.duration}s - {self.repeats} times"


import os

# Обновленный список упражнений с корректными путями к изображениям
exercises = [
    Exercise("1. Stretch for 15 seconds", os.path.join("assets", "1.jpg"), 15),
    Exercise("2. Stretch for 15 seconds", os.path.join("assets", "2.jpg"), 15),
    Exercise("3. Stretch to each side for 10 seconds", os.path.join("assets", "3.jpg"), 10, 2),
    Exercise("4. Stretch for 15 seconds", os.path.join("assets", "4.jpg"), 15),
    Exercise("5. Lifting and lowering shoulders x 5", os.path.join("assets", "5.jpg"), 10),
    Exercise("6. Neck stretch for 5 seconds on each side", os.path.join("assets", "6.jpg"), 5, 2),
    Exercise("7. Wrist stretch 10 seconds", os.path.join("assets", "7.jpg"), 10),
    Exercise("8. Turning palms down", os.path.join("assets", "8.jpg"), 10),
    Exercise("9. Stretching arms to each side for 5 seconds", os.path.join("assets", "9.jpg"), 5, 2),
    Exercise("10. Rotation to both sides", os.path.join("assets", "10.jpg"), 5, 2),
    Exercise("11. Shrug back 10 seconds", os.path.join("assets", "11.jpg"), 10),
    Exercise("12. Hand movement 10 seconds", os.path.join("assets", "12.jpg"), 10),
]


# Функция для получения упражнения по индексу
def get_exercise(index):
    """Возвращает упражнение по индексу или None, если индекс некорректен."""
    return exercises[index] if 0 <= index < len(exercises) else None

def main():
    """Запуск приложения с упражнениями."""
    root = tk.Tk()
    app = Exercise(root)
    root.mainloop()

if __name__ == "__main__":
    main()
