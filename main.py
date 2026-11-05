import tkinter as tk
from tkinter import ttk, messagebox
import settings
import dictionary_data


import tkinter as tk
from tkinter import ttk, messagebox
import threading
import settings

# Автоматически проверяем наличие библиотеки при старте
try:
    import translators as ts
except ImportError:
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "translators"])
    import translators as ts


class UltimateTranslator:
    """Полноценный графический онлайн-переводчик."""

    def __init__(self, root):
        self.root = root
        self.root.title(settings.WINDOW_TITLE)
        self.root.geometry(settings.WINDOW_GEOMETRY)
        self.root.configure(bg=settings.COLOR_BG)
        self.root.minsize(450, 420)

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        """Создание верхнего меню приложения."""
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Очистить всё", command=self.clear_fields)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        menubar.add_cascade(label="Программа", menu=file_menu)
        self.root.config(menu=menubar)

    def create_widgets(self):
        """Создание элементов интерфейса."""
        main_frame = tk.Frame(self.root, bg=settings.COLOR_BG)
        main_frame.pack(padx=20, pady=15, fill=tk.BOTH, expand=True)

        # Выбор языков
        lang_frame = tk.Frame(main_frame, bg=settings.COLOR_BG)
        lang_frame.pack(fill=tk.X, pady=(0, 15))

        lang_src_subframe = tk.Frame(lang_frame, bg=settings.COLOR_BG)
        lang_src_subframe.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(lang_src_subframe, text="Из какого языка:", font=settings.FONT_MAIN, bg=settings.COLOR_BG).pack(
            anchor="w")

        self.combo_src = ttk.Combobox(lang_src_subframe, values=list(settings.LANGUAGES.keys()),
                                      font=settings.FONT_MAIN, state="readonly")
        self.combo_src.current(0)
        self.combo_src.pack(fill=tk.X, pady=(5, 0), padx=(0, 10))

        lang_dest_subframe = tk.Frame(lang_frame, bg=settings.COLOR_BG)
        lang_dest_subframe.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(lang_dest_subframe, text="На какой язык:", font=settings.FONT_MAIN, bg=settings.COLOR_BG).pack(
            anchor="w")

        self.combo_dest = ttk.Combobox(lang_dest_subframe, values=list(settings.LANGUAGES.keys())[1:],
                                       font=settings.FONT_MAIN, state="readonly")
        self.combo_dest.current(0)
        self.combo_dest.pack(fill=tk.X, pady=(5, 0))

        # Поле ввода текста
        tk.Label(main_frame, text="Введите текст для перевода:", font=settings.FONT_MAIN, bg=settings.COLOR_BG).pack(
            anchor="w", pady=(0, 5))
        self.text_input = tk.Text(main_frame, height=5, font=settings.FONT_MAIN, wrap=tk.WORD, bd=1, relief=tk.SOLID)
        self.text_input.pack(fill=tk.X, pady=(0, 15))

        # Кнопка перевода
        self.translate_btn = tk.Button(
            main_frame,
            text="Перевести онлайн",
            font=("Arial", 11, "bold"),
            bg=settings.COLOR_PRIMARY,
            fg="white",
            command=self.start_translation_thread,
            cursor="hand2",
            bd=0,
            pady=8
        )
        self.translate_btn.pack(fill=tk.X, pady=(0, 15))

        # Поле вывода результата
        tk.Label(main_frame, text="Результат перевода:", font=settings.FONT_MAIN, bg=settings.COLOR_BG,
                 fg="#7f8c8d").pack(anchor="w")
        self.text_output = tk.Text(main_frame, height=5, font=settings.FONT_RESULT, wrap=tk.WORD, bg="#ffffff", bd=1,
                                   relief=tk.SOLID, state=tk.DISABLED)
        self.text_output.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

    def start_translation_thread(self):
        """Запуск задачи в отдельном потоке."""
        text_to_translate = self.text_input.get("1.0", tk.END).strip()
        if not text_to_translate:
            messagebox.showwarning("Пустой ввод", "Пожалуйста, введите текст для перевода.")
            return

        self.translate_btn.config(text="Перевод идет...", state=tk.DISABLED)

        thread = threading.Thread(target=self.perform_translation, args=(text_to_translate,))
        thread.daemon = True
        thread.start()

    def perform_translation(self, text):
        """Запрос к серверам перевода через библиотеку translators."""
        src_lang_name = self.combo_src.get()
        dest_lang_name = self.combo_dest.get()

        src_code = settings.LANGUAGES[src_lang_name]
        dest_code = settings.LANGUAGES[dest_lang_name]

        try:
            # Основной сервер перевода (Bing) — работает быстро и стабильно
            translated_text = ts.translate_text(
                query_text=text,
                from_language=src_code,
                to_language=dest_code,
                translator='bing'
            )
            self.root.after(0, self.update_output_success, translated_text)
        except Exception:
            try:
                # Резервный сервер (Google) на случай сбоя первого
                translated_text = ts.translate_text(
                    query_text=text,
                    from_language=src_code,
                    to_language=dest_code,
                    translator='google'
                )
                self.root.after(0, self.update_output_success, translated_text)
            except Exception:
                self.root.after(0, self.update_output_error, "Ошибка соединения. Серверы временно недоступны.")
        finally:
            self.root.after(0, lambda: self.translate_btn.config(text="Перевести онлайн", state=tk.NORMAL))

    def update_output_success(self, text):
        self.text_output.config(state=tk.NORMAL)
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert("1.0", text)
        self.text_output.config(state=tk.DISABLED, fg="#2c3e50")

    def update_output_error(self, error_message):
        self.text_output.config(state=tk.NORMAL)
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert("1.0", error_message)
        self.text_output.config(state=tk.DISABLED, fg="#c0392b")

    def clear_fields(self):
        self.text_input.delete("1.0", tk.END)
        self.text_output.config(state=tk.NORMAL)
        self.text_output.delete()
        self.text_output.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateTranslator(root)
    root.mainloop()