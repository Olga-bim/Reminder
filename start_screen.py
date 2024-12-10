import tkinter as tk
from PIL import Image, ImageTk  # Импортируем Pillow

class StartScreen:
    def __init__(self, root, on_start):
        self.root = root
        self.on_start = on_start
        
        # Создаем фрейм для стартовой страницы
        self.frame = tk.Frame(root, bg="#2e2e2e")
        self.frame.pack(fill="both", expand=True)

        # Заголовок
        self.title_label = tk.Label(self.frame, text="Time for exercise", font=("Arial", 24, "bold"), bg="#2e2e2e", fg="#ffffff")
        self.title_label.pack(pady=20)

        # Загружаем изображение с помощью Pillow
        try:
            img_path = "assets/desk.jpg"  # Путь к изображению
            image = Image.open(img_path)  # Открываем изображение с помощью Pillow
            image = image.resize((500, 300))  # Пропорционально изменяем размер изображения
            self.start_image = ImageTk.PhotoImage(image)  # Конвертируем изображение для Tkinter

            self.image_label = tk.Label(self.frame, image=self.start_image, bg="#2e2e2e")
            self.image_label.image = self.start_image  # Это нужно для того, чтобы изображение не исчезало
            self.image_label.pack(pady=20)
        except Exception as e:
            print(f"Ошибка при загрузке изображения: {e}")

        # Кнопка "Начать упражнения"
        self.start_button = tk.Button(self.frame, text="Start exercising", font=("Arial", 16), fg="white", bg="#4CAF50", 
                                      command=self.on_start, relief="flat", bd=0, activebackground="#45a049", activeforeground="white")
        self.start_button.pack(pady=20)

    def destroy(self):
        """Удаляет стартовый экран"""
        self.frame.destroy()
