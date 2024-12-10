import time
import threading
import tkinter as tk
from itertools import cycle
from plyer import notification
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageTk
from tkinter import simpledialog
import os
import webbrowser

import exercises
from start_screen import StartScreen

# Global variable to manage the reminder thread
running = True

# Путь к иконке
ICON_PATH = os.path.join(os.path.dirname(__file__), "assets", "icon.png")

def load_icon_image():
    """Загружает изображение иконки."""
    try:
        return Image.open(ICON_PATH)
    except FileNotFoundError:
        raise FileNotFoundError(f"Icon file '{ICON_PATH}' not found!")

def open_exercises(app):
    """Показывает стартовую страницу приложения."""
    start_screen = StartScreen(app.root, app.start_exercises)

def reminder(title, message, interval):
    """
    Sends reminders at specified intervals.

    :param title: Notification title.
    :param message: Notification message.
    :param interval: Interval in seconds.
    """
    while running:
        notification.notify(
            title=title,
            message=message,
            timeout=10
        )
        time.sleep(interval)

def start_reminder(icon, interval):
    """Starts the reminder thread."""
    global running
    running = True
    thread = threading.Thread(target=reminder, args=("Reminder", "Don't forget to take a break!", interval), daemon=True)
    thread.start()

def stop_reminder(icon):
    """Stops the reminder thread."""
    global running
    running = False

def quit_program(icon):
    """Exits the program."""
    global running
    running = False
    icon.stop()

class ExerciseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exercise Reminder")
        
        # Получаем размеры экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Устанавливаем размер окна
        window_size = f"{screen_width // 2}x{int(screen_height * 0.8)}"
        self.root.geometry(window_size)
        self.root.configure(bg="#2e2e2e")  # Темный фон
        
        # Переменные состояния
        self.is_paused = False
        self.current_exercise = None
        self.exercise_cycle = None
        self.countdown = 0
        self.time_left = 0
        self.timer_running = False
        self.repeat_count = 0
        self.reminder_timer = None  # Таймер для напоминания позже

        # Создаем стартовый экран
        self.start_screen = StartScreen(root, self.start_exercises)

    def start_exercises(self):
        """Запуск упражнений"""
        # Удаляем стартовый экран
        self.start_screen.destroy()

        # Виджеты для упражнений
        self.exercise_label = tk.Label(self.root, text="", font=("Helvetica", 14), bg="#2e2e2e", fg="#ffffff")
        self.exercise_label.pack(pady=10)

        self.timer_label = tk.Label(self.root, text="", font=("Helvetica", 14), bg="#2e2e2e", fg="#ffffff")
        self.timer_label.pack(pady=10)

        self.image_label = tk.Label(self.root, bg="#2e2e2e")
        self.image_label.pack(pady=10)

        # Кнопки управления
        self.pause_button = tk.Button(self.root, text="Pause", font=("Arial", 16), fg="white", bg="#FF6347", command=self.pause_exercises, relief="flat", bd=0)
        self.pause_button.pack(side="left", padx=20, pady=10)

        self.resume_button = tk.Button(self.root, text="Continue", font=("Arial", 16), fg="white", bg="#4CAF50", command=self.resume_exercises, relief="flat", bd=0)
        self.resume_button.pack(side="left", padx=20, pady=10)

        self.remind_button = tk.Button(self.root, text="Remind me later", font=("Arial", 16), fg="white", bg="#FFD700", command=self.remind_later, relief="flat", bd=0)
        self.remind_button.pack(side="left", padx=20, pady=10)

        # Цикл упражнений
        self.exercise_cycle = cycle(exercises)
        self.show_next_exercise()

    def show_next_exercise(self):
        """Показываем следующее упражнение"""
        if self.is_paused:
            return

        exercise = next(self.exercise_cycle)
        self.current_exercise = exercise
        self.repeat_count = exercise.repeats

        self.exercise_label.config(text=f"{exercise.name}\nDuration: {exercise.duration}s\nrepeat for the other side: {self.repeat_count} раз")
        
        # Отображение изображения
        img = exercise.image
        try:
            image = Image.open(img)
            image.thumbnail((300, 300))
            self.start_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.start_image)
            self.image_label.image = self.start_image
        except Exception as e:
            print(f"Error loading image: {e}")
        
        # Запуск таймера
        self.start_timer(exercise)

    def start_timer(self, exercise):
        """Запускает таймер для упражнения"""
        self.time_left = exercise.duration
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        """Обновляет таймер"""
        if self.timer_running:
            self.timer_label.config(text=f"There is time left: {self.time_left}s")
            if self.time_left > 0:
                self.time_left -= 1
                self.root.after(1000, self.update_timer)
            else:
                self.finish_exercise()

    def finish_exercise(self):
        """Обработка завершения упражнения"""
        self.repeat_count -= 1
        if self.repeat_count > 0:
            self.start_timer(self.current_exercise)
        else:
            self.show_next_exercise()

    def pause_exercises(self):
        """Ставит упражнения на паузу"""
        self.is_paused = True
        self.timer_running = False
        self.pause_button.config(state="disabled")
        self.resume_button.config(state="normal")

    def resume_exercises(self):
        """Возобновляет упражнения"""
        self.is_paused = False
        self.timer_running = True
        self.pause_button.config(state="normal")
        self.resume_button.config(state="disabled")
        self.update_timer()

    def remind_later(self):
        """Напоминает позже"""
        # Можно добавить логику для напоминания через определенное время
        pass

def main():
    try:
        user_interval = int(input("Enter reminder interval (in minutes): "))
        reminder_interval = user_interval * 60
    except ValueError:
        print("Invalid input. Using default interval (1 minute).")
        reminder_interval = 60

    try:
        icon_image = load_icon_image()
    except FileNotFoundError as e:
        print(e)
        exit(1)

    tray_icon = Icon(
        "Reminder",
        icon_image,
        menu=Menu(
            MenuItem("Start Reminders", lambda icon: start_reminder(icon, reminder_interval)),
            MenuItem("Stop Reminders", stop_reminder),
            MenuItem("Open Exercises", lambda icon: open_exercises(app)),  # Передаем объект app
            MenuItem("Quit", quit_program)
        )
    )

    thread = threading.Thread(target=tray_icon.run, daemon=True)
    thread.start()

    root = tk.Tk()
    app = ExerciseApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
