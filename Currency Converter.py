import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
from datetime import datetime

# Настройки API (замените на ваш ключ)
API_KEY = "YOUR_API_KEY"  # Получите на exchangerate-api.com
BASE_URL = "https://api.exchangerate-api.com/v4/latest/"

# Файл для сохранения истории
HISTORY_FILE = "currency_history.json"


# Инициализация окна
root = tk.Tk()
root.title("Currency Converter")
root.geometry("600x500")

# Настройка весов для адаптивности
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# --- ФУНКЦИИ ---
def get_exchange_rate(from_currency, to_currency):
    try:
        response = requests.get(f"{BASE_URL}{from_currency}")
        data = response.json()

        if 'rates' in data and to_currency in data['rates']:
            return data['rates'][to_currency]
        else:
            messagebox.showerror("Ошибка", "Не удалось получить курс валюты")
            return None
    except Exception as e:
        messagebox.showerror("Ошибка сети", f"Не удалось подключиться к API:\n{str(e)}")
        return None

def convert_currency():
    # Получаем данные из полей
    try:
        amount = float(amount_entry.get())
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Сумма должна быть положительным числом")
        return

    from_curr = from_currency.get()
    to_curr = to_currency.get()

    if from_curr == to_curr:
        result = amount
    else:
        rate = get_exchange_rate(from_curr, to_curr)
        if rate is None:
            return
        result = amount * rate

    # Отображаем результат
    result_label.config(text=f"{amount:.2f} {from_curr} = {result:.2f} {to_curr}")

    # Сохраняем в историю
    save_to_history(amount, from_curr, result, to_curr, rate)

def save_to_history(amount, from_curr, result, to_curr, rate):
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "amount": amount,
        "from_currency": from_curr,
        "result": result,
        "to_currency": to_curr,
        "rate": rate
    }

    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)

    history.append(entry)

    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

    # Обновляем таблицу
    update_history_table()

def update_history_table():
    # Очищаем таблицу
    for item in history_tree.get_children():
        history_tree.delete(item)

    # Загружаем историю
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
            for entry in history:
                history_tree.insert('', 'end', values=(
                    entry['timestamp'],
            f"{entry['amount']:.2f} {entry['from_currency']}",
            f"{entry['result']:.2f} {entry['to_currency']}",
            f"{entry['rate']:.4f}"
        ))

# --- ИНТЕРФЕЙС ---
# Основной фрейм
main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(2, weight=1)

# Верхняя часть — конвертер
converter_frame = tk.LabelFrame(main_frame, text="Конвертер валют")
converter_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
converter_frame.columnconfigure(1, weight=1)

# Поле ввода суммы
tk.Label(converter_frame, text="Сумма:").grid(row=0, column=0, sticky="w", pady=5)
amount_entry = tk.Entry(converter_frame)
amount_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)

# Выбор валюты «из»
tk.Label(converter_frame, text="Из:").grid(row=1, column=0, sticky="w", pady=5)
from_currency = ttk.Combobox(converter_frame, values=["USD", "EUR", "GBP", "JPY", "RUB", "CNY"])
from_currency.set("USD")
from_currency.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=5)

# Выбор валюты «в»
tk.Label(converter_frame, text="В:").grid(row=2, column=0, sticky="w", pady=5)
to_currency = ttk.Combobox(converter_frame, values=["USD", "EUR", "GBP", "JPY", "RUB", "CNY"])
to_currency.set("EUR")
to_currency.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=5)

# Кнопка конвертации
convert_button = tk.Button(converter_frame, text="Конвертировать", command=convert_currency)
convert_button.grid(row=3, column=0, columnspan=2, pady=10)


# Результат
result_label = tk.Label(converter_frame, text="", font=("Arial", 12, "bold"))
result_label.grid(row=4, column=0, columnspan=2, pady=5)

# Таблица истории
history_frame = tk.LabelFrame(main_frame, text="История конвертаций")
history_frame.grid(row=1, column=0, sticky="nsew")
history_frame.columnconfigure(0, weight=1)
history_frame.rowconfigure(0, weight=1)


columns = ("Время", "Из", "В", "Курс")
history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=8)

for col in columns:
    history_tree.heading(col, text=col)
    history_tree.column(col, width=120)


history_tree.pack(fill="both", expand=True)


# --- ЗАПУСК ---
# Загружаем историю при старте
update_history_table()
root.mainloop()














