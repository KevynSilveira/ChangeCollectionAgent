import customtkinter as ctk
from CONSULTA import update_db, query_db, access_db
from tkcalendar import Calendar
import datetime
from tkinter import messagebox


def create_main_frame(): # Cria a interface grafica

    data_hora_atual = datetime.datetime.now() # Obtem a data e hora atual

    # Variaveis NonLocal
    establishment = ""
    start_date = ""
    final_date = ""
    collection_agent = ""
    result = ""
    query_cont_result = 0
    start_date = ""
    final_date = ""
    client = ""

    month = data_hora_atual.month # Obtem o mês atual
    year = data_hora_atual.year # Obtem o dia atual
    text = f"Foi selecionado {result}!"

    # Definindo parâmetros do frame main
    frame_main = ctk.CTk()
    frame_main.geometry("310x310") # Definindo o tamanho do frame
    frame_main.title("CORREÇÃO FIDC") # Definindo o titulo do frame
    frame_main.resizable(False, False) # Tirando o botão de maximizar

    def select_start_date(): # Cria um frame para selecionar a data de fim de vencimento
        def back(): # Volta a tela
            frame_select_date.destroy()
        def confirm(): # Confirma a seleção da data
            nonlocal start_date
            selected_date_str = cal.get_date() # Pega o valor da data
            selected_date = datetime.datetime.strptime(selected_date_str, "%m/%d/%y") # Formata o campo de data
            start_date = selected_date.strftime("%d/%m/%Y")
            entry_start_date.delete(0, "end") # Deleta o que tiver presente no entry
            entry_start_date.insert(0, start_date) # Adiciona a nova data no entry
            frame_select_date.destroy() # volta para o frame_main

        frame_select_date = ctk.CTkFrame(master=frame_main, width=290, height=295, corner_radius=8)
        frame_select_date.place(x=10, y=10)

        button_back = ctk.CTkButton(master=frame_select_date, width=100, height=30, corner_radius=8, text="Cancelar", command=back)
        button_back.place(x=45, y=260)

        button_confirm = ctk.CTkButton(master=frame_select_date, width=100, height=30, corner_radius=8, text="Confirmar", command=confirm)
        button_confirm.place(x=155, y=260)

        label_start = ctk.CTkLabel(master=frame_select_date, text="Selecione a data de inicio:")
        label_start.place(x=75, y=0)

        cal = Calendar(frame_select_date, selectmode="day", year=year, month=month)
        cal.place(x=25, y=30)

    def select_final_date(): # Cria um frame para selecionar a data de fim de vencimento
        def back(): # Volta a tela
            frame_select_date.destroy()
        def confirm(): # Confirma a seleção da data
            nonlocal final_date # Chama a variavel nonlocal start date
            selected_date_str = cal.get_date() # Pega o valor da data
            selected_date = datetime.datetime.strptime(selected_date_str, "%m/%d/%y")  # Formata o campo de data
            final_date = selected_date.strftime("%d/%m/%Y")
            entry_final_date.delete(0, "end") # Deleta o que tiver presente no entry
            entry_final_date.insert(0, final_date) # Adiciona a nova data no entry
            frame_select_date.destroy() # volta para o frame_main

        frame_select_date = ctk.CTkFrame(master=frame_main, width=290, height=295, corner_radius=8)
        frame_select_date.place(x=10, y=10)

        button_back = ctk.CTkButton(master=frame_select_date, width=100, height=30, corner_radius=8, text="Cancelar", command=back)
        button_back.place(x=45, y=260)

        button_confirm = ctk.CTkButton(master=frame_select_date, width=100, height=30, corner_radius=8, text="Confirmar", command=confirm)
        button_confirm.place(x=155, y=260)

        label_final = ctk.CTkLabel(master=frame_select_date, text="Selecione a data de fim:")
        label_final.place(x=75, y=0)

        cal = Calendar(frame_select_date, selectmode="day", year=year, month=month)
        cal.place(x=25, y=30)

    def create_confirmation_frame(): # Cria um frame de confirmação
        nonlocal text
        def back(): # Volta a tela
            frame_confirmation.destroy()
        def confirm(): # Confirma o update do agente cobrador
            print("comando executado")

        frame_confirmation = ctk.CTkFrame(master=frame_main, width=290, height=295, corner_radius=8)
        frame_confirmation.place(x=10, y=10)

        label_warning = ctk.CTkLabel(master=frame_confirmation, text=text)
        label_warning.place(x=50, y=50)

        button_back = ctk.CTkButton(master=frame_confirmation, width=100, height=30, corner_radius=8, text="Cancelar", command=back)
        button_back.place(x=45, y=260)

        button_confirm = ctk.CTkButton(master=frame_confirmation, width=100, height=30, corner_radius=8, text="Confirmar", command=confirm)
        button_confirm.place(x=155, y=260)

    def check_field(): # Faz a verificação se todos os campos estão preenchidos e chama a função query_db
        try:
            # Chama as variaveis nonLocal
            nonlocal establishment, start_date, final_date, collection_agent, query_cont_result, result, client

            # Converte a data
            start_date_dt = datetime.datetime.strptime(start_date, "%d/%m/%Y")
            final_date_dt = datetime.datetime.strptime(final_date, "%d/%m/%Y")

            establishment = combobox_establishment.get() # Verifica qual estabelecimento é e atribui o valor a ele
            if establishment == "SC":
                establishment = "1"
            elif establishment == "RS":
                establishment = "2"
            else:
                messagebox.showerror("ATENÇÃO!", "Selecione um estabelecimento!")

            start_date = entry_start_date.get() # Pega o campo data inicio
            final_date = entry_final_date.get() # Pega o campo data final
            collection_agent = entry_collection_agent.get() # Pega o campo agente cobrador
            client = entry_client.get() # Pega o campo cliente

            # Verifica se todos os campos estão preenchidos
            if start_date_dt < final_date_dt and start_date != "" and final_date != "" and collection_agent != "" and client != "" and (establishment == "1" or establishment == "2"):

                establishment = int(establishment) # Converte para inteiro
                collection_agent = int(collection_agent) # Converte para inteiro

                access_db() # Acessa o banco de dados
                query_cont_result = query_db(client, collection_agent, establishment, start_date, final_date) # Faz a consulta e pega os parametros com base nas informações preenchidas
                result = query_cont_result[0][0] # Pega o número de consulta
                messagebox.showinfo("Atenção", f"Selecionado {result}!") # Exibe quantas linhas foram selecionadas
                create_confirmation_frame() # Cria o frame para confirmação de alteração
                print("deu certo!")
            else:
                print("Preencha todos os campos!")
                print(start_date)
                print(final_date)
                print(collection_agent)
                print(establishment)

        except Exception as e:
            messagebox.showerror("ATENÇÃO", "Preencha todos os campos!")
            print(f"Erro: {str(e)}")


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

    label_client = ctk.CTkLabel(master=frame_main, text="Selecione um client:")
    label_client.place(x=10, y=140)

    entry_client = ctk.CTkEntry(master=frame_main, width=100, height=30, corner_radius=8)
    entry_client.place(x=200, y=140)

    option_establishment = ["SC", "RS"]  # Opções de estabelecimento
    combobox_establishment = ctk.CTkComboBox(master=frame_main, values=option_establishment, width=290, height=30, state="readonly")
    combobox_establishment.set("---Selecione uma linguagem---") # Indica que precisa escolher um estabelecimento
    combobox_establishment.configure(justify="center") # Centraliza o texto na combobox
    combobox_establishment.place(x=10, y=180)

    # Centraliza o texto no entry
    entry_collection_agent.configure(justify="center")
    entry_client.configure(justify="center")
    entry_start_date.configure(justify="center")
    entry_final_date.configure(justify="center")

    button_select = ctk.CTkButton(master=frame_main, width=100, height=30, corner_radius=8, command=check_field, text= "Selecionar")
    button_select.place(x=105, y=275)

    frame_main.mainloop()

create_main_frame()
