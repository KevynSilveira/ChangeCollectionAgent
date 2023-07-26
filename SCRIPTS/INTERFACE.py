import customtkinter as ctk
from CONSULTA import update_db, query_db
from tkcalendar import Calendar
import datetime


def create_main_frame(): # Cria a interface

    # Obter a data e hora atual
    data_hora_atual = datetime.datetime.now()

    # Extrair o número do mês e o ano da data atual
    month = data_hora_atual.month
    year = data_hora_atual.year

    # Variaveis NonLocal
    valor = "teste"
    start_date = ""
    final_date = ""

    # Definindo parâmetros do frame main
    frame_main = ctk.CTk()
    frame_main.geometry("500x300")
    frame_main.title("Correção FIDC")
    frame_main.resizable(False, False)

    def select_start_date():
        nonlocal start_date

        def back(): # Volta a tela
            frame_select_date.destroy()
        def confirm():
            print("comando executado")

        frame_select_date = ctk.CTkFrame(master=frame_main, width=480, height=280, corner_radius=8)
        frame_select_date.place(x=10, y=10)

        button_back = ctk.CTkButton(master=frame_select_date, width=100, height=30, corner_radius=8, text="Cancelar", command=back)
        button_back.place(x=145, y=240)

        button_confirm = ctk.CTkButton(master=frame_select_date, width=100, height=30, corner_radius=8, text="Confirmar", command=confirm)
        button_confirm.place(x=255, y=240)

        label_warning = ctk.CTkLabel(master=frame_select_date, text="Selecione a data de inicio:")
        label_warning.place(x=175, y=10)

        cal = Calendar(frame_select_date, selectmode="day", year=year, month=month)
        cal.place(x=125, y=40)

    button_confirm = ctk.CTkButton(master=frame_main, width=100, height=30, corner_radius=8, text="Selecione a data de inicio", command=select_start_date)
    button_confirm.place(x=50, y=50)



    def create_confirmation_frame():
        nonlocal valor
        def back(): # Volta a tela
            frame_confirmation.destroy()
        def confirm():
            print("comando executado")

        frame_confirmation = ctk.CTkFrame(master=frame_main, width=480, height=280, corner_radius=8)
        frame_confirmation.place(x=10, y=10)

        label_warning = ctk.CTkLabel(master=frame_confirmation, text=valor)
        label_warning.place(x=50, y=50)

        button_back = ctk.CTkButton(master=frame_confirmation, width=100, height=30, corner_radius=8, text= "Cancelar", command=back)
        button_back.place(x=145, y=240)

        button_confirm = ctk.CTkButton(master=frame_confirmation, width=100, height=30, corner_radius=8, text= "Confirmar", command=confirm)
        button_confirm.place(x=255, y=240)


    button_select = ctk.CTkButton(master=frame_main, width=100, height=30, corner_radius=8, command=create_confirmation_frame, text= "Selecionar")
    button_select.place(x=200, y=260)


    frame_main.mainloop()

create_main_frame()
