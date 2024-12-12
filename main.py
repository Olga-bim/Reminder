import os
import time
import threading
from plyer import notification
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import mainthread
from pystray import Icon, MenuItem, Menu
from PIL import Image

# Global variables to manage the reminder thread
running = False
reminder_thread = None
tray_icon = None

# Path to the icon
ICON_PATH = os.path.join(os.path.dirname(__file__), "assets", "icon.png")


def reminder(title, message, interval):
    """
    Sends reminders at specified intervals.

    :param title: Notification title.
    :param message: Notification message.
    :param interval: Interval in seconds.
    """
    global running
    while running:
        notification.notify(
            title=title,
            message=message,
            timeout=10
        )
        time.sleep(interval)


class ReminderApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.interval = None

    def start_reminder(self, interval):
        """Starts the reminder thread."""
        global running, reminder_thread
        if running:
            self.show_popup("Error", "Reminders are already running!")
            return

        running = True
        reminder_thread = threading.Thread(
            target=reminder,
            args=("Reminder", "Don't forget to take a break!", interval),
            daemon=True
        )
        reminder_thread.start()
        self.show_popup("Success", "Reminders started!")

    def stop_reminder(self):
        """Stops the reminder thread."""
        global running
        if not running:
            self.show_popup("Error", "Reminders are not running!")
            return

        running = False
        self.show_popup("Success", "Reminders stopped!")

    @mainthread
    def show_popup(self, title, message):
        """Displays a popup message."""
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_content.add_widget(Label(text=message))
        close_button = Button(text="OK", size_hint=(1, 0.5))
        popup_content.add_widget(close_button)

        popup = Popup(title=title, content=popup_content, size_hint=(0.7, 0.4))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def build(self):
        """Builds the Kivy UI."""
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        title_label = Label(
            text="Reminder App",
            font_size="24sp",
            size_hint=(1, 0.2),
        )
        layout.add_widget(title_label)

        interval_label = Label(text="Enter interval (in minutes):", font_size="16sp")
        layout.add_widget(interval_label)

        self.interval_input = TextInput(
            hint_text="Enter minutes",
            multiline=False,
            size_hint=(1, 0.3),  # Уменьшено поле
            font_size="20sp",  # Увеличенный шрифт
            background_color=(0.9, 0.9, 0.9, 1),  # Светло-серый фон
            foreground_color=(0.2, 0.2, 0.8, 1),  # Синий текст
            padding=(10, 10),  # Отступы
        )
        layout.add_widget(self.interval_input)

        start_button = Button(
            text="Start Reminder",
            size_hint=(1, 0.4),
            background_color=(0.1, 0.7, 0.2, 1)
        )
        start_button.bind(on_press=self.handle_start)
        layout.add_widget(start_button)

        stop_button = Button(
            text="Stop Reminder",
            size_hint=(1, 0.4),
            background_color=(0.7, 0.2, 0.2, 1)
        )
        stop_button.bind(on_press=self.handle_stop)
        layout.add_widget(stop_button)

        threading.Thread(target=self.setup_tray_icon, daemon=True).start()

        return layout

    def setup_tray_icon(self):
        """Sets up the system tray icon."""
        def quit_app(icon):
            global running
            running = False
            icon.stop()
            self.stop()

        # Load custom icon
        try:
            icon_image = Image.open(ICON_PATH)
        except FileNotFoundError:
            print(f"Error: Icon file not found at {ICON_PATH}.")
            return

        menu = Menu(
            MenuItem("Start Reminder", lambda: self.start_reminder(60)),
            MenuItem("Stop Reminder", self.stop_reminder),
            MenuItem("Quit", quit_app),
        )

        global tray_icon
        tray_icon = Icon("Reminder", icon_image, menu=menu)
        tray_icon.run()

    def handle_start(self, instance):
        """Handles the start button click."""
        try:
            interval_minutes = int(self.interval_input.text)
            if interval_minutes <= 0:
                raise ValueError
            self.start_reminder(interval_minutes * 60)
        except ValueError:
            self.show_popup("Error", "Please enter a valid positive number for the interval.")

    def handle_stop(self, instance):
        """Handles the stop button click."""
        self.stop_reminder()


if __name__ == "__main__":
    ReminderApp().run()
