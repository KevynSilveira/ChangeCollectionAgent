import customtkinter as ctk
from CONSULTA import update_db, query_db
from tkcalendar import Calendar
import datetime


def create_main_frame(): # Cria a interface

    data_hora_atual = datetime.datetime.now() # Obter a data e hora atual

    # Extrair o número do mês e o ano da data atual
    month = data_hora_atual.month
    year = data_hora_atual.year

    # Variaveis NonLocal
    valor = "teste"
    start_date = ""
    final_date = " "

    # Definindo parâmetros do frame main
    frame_main = ctk.CTk()
    frame_main.geometry("310x270")
    frame_main.title("Correção FIDC")
    frame_main.resizable(False, False)

    def select_start_date(): # Cria um frame para selecionar o mês e o dia
        nonlocal start_date

        def back(): # Volta a tela
            frame_select_date.destroy()
        def confirm():
            nonlocal start_date
            selected_date_str = cal.get_date()
            selected_date = datetime.datetime.strptime(selected_date_str, "%m/%d/%y")  # Ajustar o formato aqui
            start_date = selected_date.strftime("%d/%m/%Y")
            entry_start_date.delete(0, "end")
            entry_start_date.insert(0, start_date)
            frame_select_date.destroy()

        frame_select_date = ctk.CTkFrame(master=frame_main, width=290, height=255, corner_radius=8)
        frame_select_date.place(x=10, y=10)

        button_back = ctk.CTkButton(master=frame_select_date, width=100, height=30, corner_radius=8, text="Cancelar", command=back)
        button_back.place(x=45, y=220)

        button_confirm = ctk.CTkButton(master=frame_select_date, width=100, height=30, corner_radius=8, text="Confirmar", command=confirm)
        button_confirm.place(x=155, y=220)

        label_start = ctk.CTkLabel(master=frame_select_date, text="Selecione a data de inicio:")
        label_start.place(x=75, y=0)

        cal = Calendar(frame_select_date, selectmode="day", year=year, month=month)
        cal.place(x=25, y=30)

    def select_final_date(): # Cria um frame para selecionar o mês e o dia
        nonlocal final_date

        def back(): # Volta a tela
            frame_select_date.destroy()
        def confirm():
            nonlocal final_date
            selected_date_str = cal.get_date()
            selected_date = datetime.datetime.strptime(selected_date_str, "%m/%d/%y")  # Ajustar o formato aqui
            final_date = selected_date.strftime("%d/%m/%Y")
            entry_final_date.delete(0, "end")
            entry_final_date.insert(0, final_date)
            frame_select_date.destroy()

        frame_select_date = ctk.CTkFrame(master=frame_main, width=290, height=255, corner_radius=8)
        frame_select_date.place(x=10, y=10)

        button_back = ctk.CTkButton(master=frame_select_date, width=100, height=30, corner_radius=8, text="Cancelar", command=back)
        button_back.place(x=45, y=220)

        button_confirm = ctk.CTkButton(master=frame_select_date, width=100, height=30, corner_radius=8, text="Confirmar", command=confirm)
        button_confirm.place(x=155, y=220)

        label_final = ctk.CTkLabel(master=frame_select_date, text="Selecione a data de fim:")
        label_final.place(x=75, y=0)

        cal = Calendar(frame_select_date, selectmode="day", year=year, month=month)
        cal.place(x=25, y=30)

    def create_confirmation_frame():
        nonlocal valor
        def back(): # Volta a tela
            frame_confirmation.destroy()
        def confirm():
            print("comando executado")

        frame_confirmation = ctk.CTkFrame(master=frame_main, width=290, height=255, corner_radius=8)
        frame_confirmation.place(x=10, y=10)

        label_warning = ctk.CTkLabel(master=frame_confirmation, text=valor)
        label_warning.place(x=50, y=50)

        button_back = ctk.CTkButton(master=frame_confirmation, width=100, height=30, corner_radius=8, text="Cancelar", command=back)
        button_back.place(x=45, y=220)

        button_confirm = ctk.CTkButton(master=frame_confirmation, width=100, height=30, corner_radius=8, text="Confirmar", command=confirm)
        button_confirm.place(x=155, y=220)

    def validate_input(char):
        # Verifica se o caractere é um dígito numérico
        if char.isdigit():
            # Verifica o comprimento atual do texto no Entry
            entry_text = entry_collection_agent.get()
            if len(entry_text) < 4:
                return True
        return False


    button_start_date = ctk.CTkButton(master=frame_main, width=170, height=30, corner_radius=8, text="Selecione a data de inicio", command=select_start_date)
    button_start_date.place(x=10, y=10)

    button_final_date = ctk.CTkButton(master=frame_main, width=170, height=30, corner_radius=8, text="Selecione a data de fim", command=select_final_date)
    button_final_date.place(x=10, y=50)

    entry_start_date = ctk.CTkEntry(master=frame_main, width=100, height=30, corner_radius=8)
    entry_start_date.insert(0, start_date)
    entry_start_date.place(x=200, y=10)

    entry_start_date = ctk.CTkEntry(master=frame_main, width=100, height=30, corner_radius=8)
    entry_start_date.place(x=200, y=10)

    entry_final_date = ctk.CTkEntry(master=frame_main, width=100, height=30, corner_radius=8)
    entry_final_date.place(x=200, y=50)

    label_collection_agent = ctk.CTkLabel(master=frame_main, text="Selecione um agente cobrador:")
    label_collection_agent.place(x=10, y=90)

    entry_collection_agent = ctk.CTkEntry(master=frame_main, width=100, height=30, corner_radius=8)
    entry_collection_agent.place(x=200, y=90)

    vcmd = frame_main.register(validate_input)
    entry_collection_agent.configure(validate="key", validatecommand=(vcmd, "%S"))
    entry_collection_agent.configure(justify="center") # Centraliza o texto no entry

    option_establishment = ["SC", "RS"]  # Opções de estabelecimento
    combobox_establishment = ctk.CTkComboBox(master=frame_main, values=option_establishment, width=290, height=30, state="readonly")
    combobox_establishment.set("---Selecione uma linguagem---") # Indica que precisa escolher um estabelecimento
    combobox_establishment.configure(justify="center") # Centraliza o texto na combobox
    combobox_establishment.place(x=10, y=140)


    button_select = ctk.CTkButton(master=frame_main, width=100, height=30, corner_radius=8, command=create_confirmation_frame, text= "Selecionar")
    button_select.place(x=105, y=235)


    frame_main.mainloop()

create_main_frame()
