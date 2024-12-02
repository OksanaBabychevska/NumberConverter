import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from converter.core import (
    convert_to_binary,
    convert_to_octal,
    convert_to_decimal,
    convert_to_hexadecimal,
)
import os

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Конвертер систем числення")
        self.root.geometry("1100x900")  # Початковий розмір вікна
        self.root.minsize(600, 500)  # Мінімальний розмір вікна
        self.root.resizable(True, True)  # Дозволяємо змінювати розміри вікна

        # Стиль для кнопок і чекбоксів
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 18), padding=15, background="#4CAF50", foreground="white")
        self.style.configure("TCheckbutton", font=("Arial", 18), padding=15)
        self.style.map("TButton", background=[('active', '#45a049'), ('pressed', '#387f36')])

        # Стиль для кнопки очищення
        self.style.configure("ClearButton.TButton", font=("Arial", 18), padding=15, background="#FF5733", foreground="white")
        self.style.map("ClearButton.TButton", background=[('active', '#FF7043'), ('pressed', '#D63C29')])

        # Створення меню
        self.create_menu()

        # Контейнер для сторінок
        self.page_frame = ttk.Frame(root, padding=30)
        self.page_frame.pack(fill=tk.BOTH, expand=True)

        # Початкова сторінка (Основна сторінка)
        self.show_main_page()

        # Змінна для збереження шляху до файлу результатів
        self.result_file_path = None

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        page_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Сторінки", menu=page_menu)
        page_menu.add_command(label="Основна сторінка", command=self.show_main_page)
        page_menu.add_command(label="Переведення чисел вручну", command=self.show_manual_conversion_page)
        page_menu.add_command(label="Переведення чисел з файлу", command=self.show_file_conversion_page)

    def show_main_page(self):
        """Показати основну сторінку"""
        # Очищаємо поточний фрейм
        for widget in self.page_frame.winfo_children():
            widget.destroy()

        # Заголовок основної сторінки
        title_label = ttk.Label(self.page_frame, text="Конвертер систем числення", font=("Arial", 24, "bold"))
        title_label.pack(pady=30)

        description_label = ttk.Label(self.page_frame, text="Це додаток для переведення чисел між різними системами числення.\n"
                                                           "Ви можете вибрати одну з двох опцій:\n"
                                                           "1. Переведення чисел вручну\n"
                                                           "2. Переведення чисел з файлів", font=("Arial", 18))
        description_label.pack(pady=20)

        manual_button = ttk.Button(self.page_frame, text="Переведення чисел вручну", command=self.show_manual_conversion_page, style="TButton")
        manual_button.pack(pady=10)

        file_button = ttk.Button(self.page_frame, text="Переведення чисел з файлу", command=self.show_file_conversion_page, style="TButton")
        file_button.pack(pady=10)

    def show_manual_conversion_page(self):
        """Показати сторінку для переведення чисел вручну"""
        # Очищаємо поточний фрейм
        for widget in self.page_frame.winfo_children():
            widget.destroy()

        # Заголовок сторінки
        title_label = ttk.Label(self.page_frame, text="Переведення чисел вручну", font=("Arial", 24, "bold"))
        title_label.pack(pady=30)

        # Поле вводу числа
        input_frame = ttk.Frame(self.page_frame)
        input_frame.pack(fill=tk.X, pady=20)

        input_label = ttk.Label(input_frame, text="Введіть число (десяткове):", font=("Arial", 18))
        input_label.pack(side=tk.LEFT, padx=10)

        self.input_entry = ttk.Entry(input_frame, font=("Arial", 18), width=25)
        self.input_entry.pack(side=tk.LEFT, padx=10, ipadx=10)

        # Чекбокси для вибору систем числення
        self.system_vars = {
            "Двійкова": tk.IntVar(value=0),
            "Вісімкова": tk.IntVar(value=0),
            "Десяткова": tk.IntVar(value=1),
            "Шістнадцяткова": tk.IntVar(value=0),
        }

        checkbox_frame = ttk.Frame(self.page_frame)
        checkbox_frame.pack(fill=tk.X, pady=20)

        ttk.Label(checkbox_frame, text="Виберіть системи числення для переведення:", font=("Arial", 18)).pack(anchor=tk.W, pady=5)

        for system, var in self.system_vars.items():
            ttk.Checkbutton(checkbox_frame, text=system, variable=var, style="TCheckbutton").pack(anchor=tk.W, padx=30, pady=10)

        # Кнопка для переведення
        self.convert_button = ttk.Button(self.page_frame, text="Перевести", command=self.convert, style="TButton")
        self.convert_button.pack(pady=30, side=tk.LEFT, padx=20)

        # Кнопка для очищення результатів
        self.clear_button = ttk.Button(self.page_frame, text="Очистити", command=self.clear_all, style="ClearButton.TButton")
        self.clear_button.pack(pady=30, side=tk.LEFT)

        # Кнопка для збереження результатів у файл
        self.save_button = ttk.Button(self.page_frame, text="Зберегти результати", command=self.save_results, style="TButton")
        self.save_button.pack(pady=10)

        # Поле для результатів
        result_frame = ttk.LabelFrame(self.page_frame, text="Результати", padding=10, labelanchor="n")
        result_frame.pack(fill=tk.BOTH, expand=True)

        self.result_text = tk.Text(result_frame, height=12, font=("Courier New", 16), state=tk.DISABLED, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def show_file_conversion_page(self):
        """Показати сторінку для переведення чисел з файлу"""
        # Очищаємо поточний фрейм
        for widget in self.page_frame.winfo_children():
            widget.destroy()

        # Заголовок сторінки
        title_label = ttk.Label(self.page_frame, text="Переведення чисел з файлу", font=("Arial", 24, "bold"))
        title_label.pack(pady=30)

        # Чекбокси для вибору систем числення
        self.system_vars = {
            "Двійкова": tk.IntVar(value=0),
            "Вісімкова": tk.IntVar(value=0),
            "Десяткова": tk.IntVar(value=1),
            "Шістнадцяткова": tk.IntVar(value=0),
        }

        checkbox_frame = ttk.Frame(self.page_frame)
        checkbox_frame.pack(fill=tk.X, pady=20)

        ttk.Label(checkbox_frame, text="Виберіть системи числення для переведення:", font=("Arial", 18)).pack(anchor=tk.W, pady=5)

        for system, var in self.system_vars.items():
            ttk.Checkbutton(checkbox_frame, text=system, variable=var, style="TCheckbutton").pack(anchor=tk.W, padx=30, pady=10)

        # Кнопка для вибору файлу
        load_button = ttk.Button(self.page_frame, text="Завантажити файл", command=self.load_file, style="TButton")
        load_button.pack(pady=20)

        # Кнопка для очищення результатів
        clear_button = ttk.Button(self.page_frame, text="Очистити результати", command=self.clear_results, style="ClearButton.TButton")
        clear_button.pack(pady=10)

        # Поле для результатів
        result_frame = ttk.LabelFrame(self.page_frame, text="Результати", padding=10, labelanchor="n")
        result_frame.pack(fill=tk.BOTH, expand=True)

        self.result_text = tk.Text(result_frame, height=12, font=("Courier New", 16), state=tk.DISABLED, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def convert(self):
        """Переведення числа вручну"""
        number = self.input_entry.get()

        if not number:
            messagebox.showerror("Помилка", "Будь ласка, введіть число.")
            return

        try:
            decimal_value = int(number)
        except ValueError:
            messagebox.showerror("Помилка", "Введіть коректне десяткове число.")
            return

        results = {}
        if self.system_vars["Двійкова"].get():
            results["Двійкова"] = convert_to_binary(decimal_value)
        if self.system_vars["Вісімкова"].get():
            results["Вісімкова"] = convert_to_octal(decimal_value)
        if self.system_vars["Десяткова"].get():
            results["Десяткова"] = str(decimal_value)
        if self.system_vars["Шістнадцяткова"].get():
            results["Шістнадцяткова"] = convert_to_hexadecimal(decimal_value)

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        if results:
            for system, value in results.items():
                self.result_text.insert(tk.END, f"{system}: {value}\n")
        else:
            self.result_text.insert(tk.END, "Будь ласка, виберіть хоча б одну систему числення.")
        self.result_text.config(state=tk.DISABLED)

    def load_file(self):
        """Завантажити файл та обробити числа"""
        file_path = filedialog.askopenfilename(title="Виберіть файл", filetypes=[("Текстові файли", "*.txt")])
        if not file_path:
            return

        if not any(var.get() for var in self.system_vars.values()):
            messagebox.showerror("Помилка", "Будь ласка, виберіть хоча б одну систему числення.")
            return

        try:
            with open(file_path, "r") as file:
                lines = file.readlines()

            results = {}
            for line in lines:
                numbers = line.strip().split(",")  # Розділяємо числа за комою
                for number_str in numbers:
                    number_str = number_str.strip()  # Очищаємо зайві пробіли
                    if not number_str.isdigit():
                        continue

                    number = int(number_str)
                    result_for_number = {}

                    if self.system_vars["Двійкова"].get():
                        result_for_number["Двійкова"] = convert_to_binary(number)
                    if self.system_vars["Вісімкова"].get():
                        result_for_number["Вісімкова"] = convert_to_octal(number)
                    if self.system_vars["Шістнадцяткова"].get():
                        result_for_number["Шістнадцяткова"] = convert_to_hexadecimal(number)
                    if self.system_vars["Десяткова"].get():
                        result_for_number["Десяткова"] = str(number)

                    results[number] = result_for_number

            # Виведення результатів
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            for number, result in results.items():
                self.result_text.insert(tk.END, f"{number}:\n")
                if isinstance(result, str):
                    self.result_text.insert(tk.END, f"  {result}\n")
                else:
                    for system, value in result.items():
                        self.result_text.insert(tk.END, f"  {system}: {value}\n")
                self.result_text.insert(tk.END, "\n")

            self.result_text.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося обробити файл: {e}")

    def save_results(self):
        """Зберегти результати в файл"""
        if not self.result_text.get(1.0, tk.END).strip():
            messagebox.showerror("Помилка", "Немає результатів для збереження.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Текстові файли", "*.txt")])
        if not save_path:
            return

        try:
            with open(save_path, "w") as file:
                file.write(self.result_text.get(1.0, tk.END))
            self.result_file_path = save_path
            messagebox.showinfo("Успіх", f"Результати збережено в {save_path}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося зберегти файл: {e}")

    def clear_all(self):
        """Очистити введене число та результати"""
        self.input_entry.delete(0, tk.END)
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)

        # Видалення файлу результатів при очищенні
        if self.result_file_path and os.path.exists(self.result_file_path):
            os.remove(self.result_file_path)
            self.result_file_path = None

    def clear_results(self):
        """Очистити результати на сторінці файлу"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)

        # Видалення файлу результатів при очищенні
        if self.result_file_path and os.path.exists(self.result_file_path):
            os.remove(self.result_file_path)
            self.result_file_path = None


if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()
