import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry

def show_selected_date():
    date = cal.selection_get()
    result_label.config(text="Data selecionada: " + date.strftime("%d/%m/%Y"))

root = tk.Tk()
root.title("Seletor de Data com Tema Escuro")

# Criando o seletor de data com tema escuro
style = ttk.Style(root)
style.theme_use('clam')  # 'clam' é o tema escuro

cal = Calendar(root, selectmode="day", year=2023, month=7)
cal.pack(padx=10, pady=10)

# Label para exibir a data selecionada
result_label = tk.Label(root, text="Nenhuma data selecionada.", font=("Arial", 12))
result_label.pack(pady=10)

# Botão para obter a data selecionada
get_date_button = ttk.Button(root, text="Obter Data Selecionada", command=show_selected_date)
get_date_button.pack(pady=5)

root.mainloop()
