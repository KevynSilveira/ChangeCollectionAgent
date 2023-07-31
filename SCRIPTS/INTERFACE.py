import customtkinter as ctk
from CONSULTA import update_db, query_count_db, access_db, query_db
from tkcalendar import Calendar
import datetime
from tkinter import messagebox

# Variaveis global
establishment = ""
start_date = ""
final_date = ""
collection_agent = ""
result = 0
query_cont_result = 0
client = ""
portion = ""
order = ""

def create_main_frame(): # Cria a interface grafica

    data_hora_atual = datetime.datetime.now() # Obtem a data e hora atual
    month = data_hora_atual.month # Obtem o mês atual
    year = data_hora_atual.year # Obtem o dia atual


    # Definindo parâmetros do frame main
    frame_main = ctk.CTk()
    frame_main.geometry("310x310") # Definindo o tamanho do frame
    frame_main.title("ALTERAÇÃO AGENTE COBRADOR") # Definindo o titulo do frame
    frame_main.resizable(False, False) # Tirando o botão de maximizar

    def select_start_date(): # Cria um frame para selecionar a data de fim de vencimento
        def back(): # Volta a tela
            frame_select_date.destroy()
        def confirm(): # Confirma a seleção da data
            global start_date
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

        global text
        text = f"Você selecionou {result}"
        def back(): # Volta a tela
            frame_select_date.destroy()
        def confirm(): # Confirma a seleção da data
            global final_date # Chama a variavel global start date
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
        global result, establishment, start_date, final_date, client, collection_agent, order
        def back(): # Volta a tela
            frame_confirmation.destroy()
        def confirm(): # Confirma o update do agente cobrador
            print("comando executado")
            print("estabelecimento:", establishment)
            print("Data inicio:", start_date)
            print("Data final:", final_date)
            print("Cliente:", client)
            print("Agente cobrador:", collection_agent)

            new_collection_agent = entry_new_collection_agent.get()
            #new_collection_agent = int(new_collection_agent)

            if not new_collection_agent:  # Verifica se a variável está vazia
                messagebox.showerror("Erro", "Preencha todos os campos!")

            else:
                response = messagebox.askyesno("Confirmação", f"Você tem certeza que deseja alterar o agente cobrador {collection_agent} pelo {new_collection_agent}?")
                if response:
                    # Código a ser executado se o usuário confirmar a ação
                    print("Ação confirmada!")
                    access_db()
                    lines_affected = update_db(client, collection_agent, new_collection_agent, establishment,portion, start_date, final_date)
                    messagebox.showinfo("Atenção", f"Foram afetadas {lines_affected} linhas")
                else:
                    # Código a ser executado se o usuário cancelar a ação
                    print("Ação cancelada!")


        frame_confirmation = ctk.CTkFrame(master=frame_main, width=290, height=295, corner_radius=8)
        frame_confirmation.place(x=10, y=10)

        label_select = ctk.CTkLabel(master=frame_confirmation, text=f"Você selecinou {result} linhas!", width=150)
        label_select.place(x=70, y=20)

        label_new_collection_agent = ctk.CTkLabel(master=frame_confirmation, text="Digite o código do\n novo agente cobrador", width=150)
        label_new_collection_agent.place(x=70, y=90)

        entry_new_collection_agent = ctk.CTkEntry(master=frame_confirmation, width=150, height=30, corner_radius=8)
        entry_new_collection_agent.place(x=70, y=130)
        entry_new_collection_agent.configure(justify="center")

        button_back = ctk.CTkButton(master=frame_confirmation, width=100, height=30, corner_radius=8, text="Cancelar", command=back)
        button_back.place(x=45, y=260)

        button_confirm = ctk.CTkButton(master=frame_confirmation, width=100, height=30, corner_radius=8, text="Confirmar", command=confirm)
        button_confirm.place(x=155, y=260)

    def check_field(): # Faz a verificação se todos os campos estão preenchidos e chama a função query_db
        try:
            # Chama as variaveis global
            global establishment, start_date, final_date, collection_agent, query_cont_result, result, client, portion, order

            # Converte a data
            start_date_dt = datetime.datetime.strptime(start_date, "%d/%m/%Y")
            final_date_dt = datetime.datetime.strptime(final_date, "%d/%m/%Y")


            start_date = entry_start_date.get() # Pega o campo data inicio
            final_date = entry_final_date.get() # Pega o campo data final
            collection_agent = entry_collection_agent.get() # Pega o campo agente cobrador
            client = entry_client.get() # Pega o campo cliente
            portion = combobox_portion.get() # Pega o campo parcela
            establishment = combobox_establishment.get() # Verifica qual estabelecimento é e atribui o valor a ele
            order = combobox_order.get()

            if establishment == "SC":
                establishment = "1"

            elif establishment == "RS":
                establishment = "2"

            else:
                messagebox.showerror("ATENÇÃO!", "Selecione um estabelecimento!")

            if order == "Data Vencimento":
                order = "dat_vencimento ASC"

            elif order == "Maior Valor":
                order = "vlr_documento DESC"

            elif order == "Menor Valor":
                order = "vlr_documento ASC"

            else:
                messagebox.showerror("ATENÇÃO!", "Selecione a ordenação!")

            if portion == "Parcela":
                messagebox.showerror("Atenção", "Selecione uma parcela!")

            if client == "":
                messagebox.showerror("Atenção", "Selecione uma cliente!")

            if collection_agent == "":
                messagebox.showerror("Atenção", "Selecione um agente cobrador!")


            # Verifica se todos os campos estão preenchidos
            if start_date_dt < final_date_dt and start_date != "" and final_date != "" and collection_agent != "" and client != "" and (establishment == "1" or establishment == "2") and portion != "Parcela":

                global result
                establishment = int(establishment) # Converte para inteiro
                collection_agent = int(collection_agent) # Converte para inteiro

                access_db() # Acessa o banco de dados
                query_cont_result = query_count_db(client, collection_agent, establishment, portion, start_date, final_date, order) # Faz a consulta e pega os parametros com base nas informações preenchidas
                selected_lines = query_cont_result[0][0] # Pega o número de consulta
                result = selected_lines
                messagebox.showinfo("Atenção", f"Foi gerado um excel com os paramêtros selecionados!") # Exibe quantas linhas foram selecionadas
                query_db(client, collection_agent, establishment, portion, start_date, final_date, order)
                create_confirmation_frame()  # Cria o frame para confirmação de alteração
                print("Valor de result:", result)
                print("deu certo!")
            else:
                messagebox.showerror("Atenção", "Preencha todos os campos!")
                print(start_date)
                print(final_date)
                print(collection_agent)
                print(establishment)
                print(portion)
                print(order)

        except Exception as e:
            messagebox.showerror("ATENÇÃO", "Verifique se o arquivo (Troca agente cobrador.xlsx) está aberto!")
            print(f"Erro: {str(e)}")

    button_start_date = ctk.CTkButton(master=frame_main, width=170, height=30, corner_radius=8, text="Data incial", command=select_start_date)
    button_start_date.place(x=10, y=10)

    button_final_date = ctk.CTkButton(master=frame_main, width=170, height=30, corner_radius=8, text="Data final", command=select_final_date)
    button_final_date.place(x=10, y=50)

    entry_start_date = ctk.CTkEntry(master=frame_main, width=100, height=30, corner_radius=8)
    entry_start_date.place(x=200, y=10)

    entry_final_date = ctk.CTkEntry(master=frame_main, width=100, height=30, corner_radius=8)
    entry_final_date.place(x=200, y=50)

    label_collection_agent = ctk.CTkLabel(master=frame_main, text="Agente cobrador:", width=170)
    label_collection_agent.place(x=10, y=90)

    entry_collection_agent = ctk.CTkEntry(master=frame_main, width=100, height=30, corner_radius=8)
    entry_collection_agent.place(x=200, y=90)

    label_client = ctk.CTkLabel(master=frame_main, text="Cliente:", width=170)
    label_client.place(x=10, y=130)

    entry_client = ctk.CTkEntry(master=frame_main, width=100, height=30, corner_radius=8)
    entry_client.place(x=200, y=130)

    option_establishment = ["SC", "RS"]  # Opções de estabelecimento
    combobox_establishment = ctk.CTkComboBox(master=frame_main, values=option_establishment, width=140, height=30, state="readonly")
    combobox_establishment.set("Estabelecimento") # Indica que precisa escolher um estabelecimento
    combobox_establishment.configure(justify="center") # Centraliza o texto na combobox
    combobox_establishment.place(x=10, y=180)

    option_portion = ["A", "B", "C", "D", "E", "F"]  # Opções de estabelecimento
    combobox_portion = ctk.CTkComboBox(master=frame_main, values=option_portion, width=140, height=30, state="readonly")
    combobox_portion.set("Parcela") # Indica que precisa escolher um estabelecimento
    combobox_portion.configure(justify="center") # Centraliza o texto na combobox
    combobox_portion.place(x=160, y=180)

    option_order = ["Data Vencimento", "Maior Valor", "Menor Valor"]  # Opções de estabelecimento
    combobox_order = ctk.CTkComboBox(master=frame_main, values=option_order, width=140, height=30, state="readonly")
    combobox_order.set("Ordenação") # Indica que precisa escolher um ordenação
    combobox_order.configure(justify="center") # Centraliza o texto na combobox
    combobox_order.place(x=80, y=220)


    # Centraliza o texto no entry
    entry_collection_agent.configure(justify="center")
    entry_client.configure(justify="center")
    entry_start_date.configure(justify="center")
    entry_final_date.configure(justify="center")
    label_client.configure(justify="center")
    label_collection_agent.configure(justify="center")

    button_select = ctk.CTkButton(master=frame_main, width=100, height=30, corner_radius=8, command=check_field, text= "Selecionar")
    button_select.place(x=105, y=275)

    frame_main.mainloop()

create_main_frame()
