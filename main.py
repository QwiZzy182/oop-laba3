import tkinter as tk
from tkinter import ttk, messagebox
import settings
import dictionary_data


class VocabularyTranslator:
    """Класс графического приложения для перевода иностранных слов."""

    def __init__(self, root):
        self.root = root
        self.root.title(settings.WINDOW_TITLE)
        self.root.geometry(settings.WINDOW_GEOMETRY)
        self.root.configure(bg=settings.COLOR_BG)
        self.root.minsize(400, 350)

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        """Создание верхнего меню."""
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Сбросить поле", command=self.clear_fields)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        menubar.add_cascade(label="Программа", menu=file_menu)

        self.root.config(menu=menubar)

    def create_widgets(self):
        """Создание элементов пользовательского интерфейса."""
        main_frame = tk.Frame(self.root, bg=settings.COLOR_BG)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        tk.Label(
            main_frame,
            text="Выберите направление перевода:",
            font=settings.FONT_MAIN,
            bg=settings.COLOR_BG
        ).pack(anchor="w", pady=(0, 5))

        self.direction_combo = ttk.Combobox(
            main_frame,
            values=["Английский -> Русский", "Русский -> Английский"],
            font=settings.FONT_MAIN,
            state="readonly"
        )
        self.direction_combo.current(0)  # По умолчанию выбираем первый вариант
        self.direction_combo.pack(fill=tk.X, pady=(0, 15))

        tk.Label(
            main_frame,
            text="Введите слово для перевода:",
            font=settings.FONT_MAIN,
            bg=settings.COLOR_BG
        ).pack(anchor="w", pady=(0, 5))

        self.word_entry = tk.Entry(main_frame, font=settings.FONT_MAIN)
        self.word_entry.pack(fill=tk.X, pady=(0, 15))
        # Привязка клавиши Enter к запуску перевода
        self.word_entry.bind("<Return>", lambda event: self.translate_word())

        self.translate_btn = tk.Button(
            main_frame,
            text="Перевести",
            font=("Arial", 11, "bold"),
            bg=settings.COLOR_PRIMARY,
            fg="white",
            command=self.translate_word,
            cursor="hand2"
        )
        self.translate_btn.pack(fill=tk.X, pady=(0, 20))

        tk.Label(
            main_frame,
            text="Перевод:",
            font=settings.FONT_MAIN,
            bg=settings.COLOR_BG,
            fg="#7f8c8d"
        ).pack(anchor="w")

        self.result_label = tk.Label(
            main_frame,
            text="",
            font=settings.FONT_RESULT,
            bg=settings.COLOR_BG,
            fg="#2c3e50",
            wraplength=350,
            justify=tk.LEFT
        )
        self.result_label.pack(anchor="w", pady=10)

    def translate_word(self):
        """Логика обработки и перевода введенного слова."""
        search_word = self.word_entry.get().strip().lower()

        if not search_word:
            messagebox.showwarning("Пустой ввод", "Пожалуйста, введите слово.")
            return

        current_direction = self.direction_combo.get()

        if current_direction == "Английский -> Русский":
            dictionary = dictionary_data.EN_TO_RU
        else:
            dictionary = dictionary_data.RU_TO_EN

        translation = dictionary.get(search_word)

        if translation:
            self.result_label.config(text=translation.capitalize(), fg="#27ae60")
        else:
            self.result_label.config(text="Слово не найдено в словаре", fg="#c0392b")

    def clear_fields(self):
        """Очистка поля ввода и результата."""
        self.word_entry.delete(0, tk.END)
        self.result_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyTranslator(root)
    root.mainloop()
