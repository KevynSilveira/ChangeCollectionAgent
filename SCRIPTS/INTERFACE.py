import customtkinter as ctk

def create_main_frame(): # Cria a interface

    valor = "teste"

    # Definindo parâmetros do frame main
    frame_main = ctk.CTk()
    frame_main.geometry("500x300")
    frame_main.title("Correção FDIk")
    frame_main.resizable(False, False)

    def create_confirmation_frame():
        nonlocal valor

        frame_confirmation = ctk.CTkFrame(master=frame_main, width=480, height=280, corner_radius=8)
        frame_confirmation.place(x=10, y=10)

        label_warning = ctk.CTkLabel(master=frame_confirmation, text=valor)

        button_back = ctk.CTkButton(master=frame_confirmation, width=100, height=30, corner_radius=8, text= "Cancelar")
        button_back.place(x=145, y=240)

        button_confirm = ctk.CTkButton(master=frame_confirmation, width=100, height=30, corner_radius=8, text= "Confirmar")
        button_confirm.place(x=255, y=240)



    button_select = ctk.CTkButton(master=frame_main, width=100, height=30, corner_radius=8, command=create_confirmation_frame, text= "Selecionar")
    button_select.place(x=200, y=260)


    frame_main.mainloop()

create_main_frame()
