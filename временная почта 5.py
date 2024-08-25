import requests
import tkinter as tk
from tkinter import font
import pyperclip

# URL для генерации временной почты
CREATE_EMAIL_URL = "https://www.1secmail.com/api/v1/?action=genRandomMailbox"
# URL для получения сообщений
CHECK_EMAIL_URL = "https://www.1secmail.com/api/v1/"

def create_temp_email():
    response = requests.get(CREATE_EMAIL_URL)
    if response.status_code == 200:
        email = response.json()[0]
        email_var.set(email)
    else:
        email_var.set("Ошибка при создании почты")

def check_emails():
    email = email_var.get()
    if not email:
        email_var.set("Сначала создайте временную почту")
        return

    username, domain = email.split('@')
    params = {
        'action': 'getMessages',
        'login': username,
        'domain': domain
    }
    response = requests.get(CHECK_EMAIL_URL, params=params)
    if response.status_code == 200:
        emails = response.json()
        if emails:
            emails_text.delete(1.0, tk.END)
            for email in emails:
                msg_id = email.get('id')
                msg_response = requests.get(f"{CHECK_EMAIL_URL}?action=readMessage&login={username}&domain={domain}&id={msg_id}")
                if msg_response.status_code == 200:
                    msg_data = msg_response.json()
                    emails_text.insert(tk.END, f"От: {msg_data.get('from')}\nТема: {msg_data.get('subject')}\nТекст: {msg_data.get('textBody')}\n\n")
                    btn = tk.Button(frame, text="Копировать сообщение", command=lambda m=msg_data.get('textBody'): copy_message(m), font=("Helvetica", 12), bg="#87CEEB", fg="#FFFFFF")
                    btn.grid(row=3 + len(emails), column=0, columnspan=4, pady=5)
                else:
                    emails_text.insert(tk.END, f"Ошибка при получении письма с ID {msg_id}\n")
        else:
            emails_text.insert(tk.END, "Нет новых писем\n")
    else:
        emails_text.insert(tk.END, "Не удалось проверить почту\n")

def copy_email():
    email = email_var.get()
    if email:
        pyperclip.copy(email)
    else:
        email_var.set("Сначала создайте временную почту")

def copy_message(message):
    pyperclip.copy(message)

# Создание главного окна
root = tk.Tk()
root.title("Временная почта")
root.configure(bg="#87CEEB")

# Переменная для хранения email
email_var = tk.StringVar()

# Создание и размещение элементов интерфейса
frame = tk.Frame(root, bg="#87CEEB")
frame.pack(padx=10, pady=10)

email_label = tk.Label(frame, text="Временная почта:", fg="#000000", bg="#87CEEB", font=("Helvetica", 14))
email_label.grid(row=0, column=0, sticky="w")

email_entry = tk.Entry(frame, textvariable=email_var, width=30, font=("Helvetica", 14), bg="#ADD8E6", fg="#000000")
email_entry.grid(row=0, column=1, padx=5)

create_button = tk.Button(frame, text="Создать почту", command=create_temp_email, font=("Helvetica", 14), bg="#ADD8E6", fg="#000000")
create_button.grid(row=0, column=2, padx=5)

copy_button = tk.Button(frame, text="Копировать почту", command=copy_email, font=("Helvetica", 14), bg="#ADD8E6", fg="#000000")
copy_button.grid(row=0, column=3, padx=5)

check_button = tk.Button(frame, text="Проверить почту", command=check_emails, font=("Helvetica", 14), bg="#ADD8E6", fg="#000000")
check_button.grid(row=1, column=0, columnspan=4, pady=10)

emails_text = tk.Text(frame, width=50, height=10, font=("Helvetica", 14), bg="#ADD8E6", fg="#000000")
emails_text.grid(row=2, column=0, columnspan=4, pady=5)

# Запуск главного цикла
root.mainloop()