import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta

# Função para carregar os dados salvos
def carregar_dados():
    try:
        with open("dados_clientes.txt", "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []

# Função para salvar os dados
def salvar_dados():
    cliente = entry_cliente.get()
    barco = entry_barco.get()
    data_entrada = entry_data_entrada.get()
    valor_mensalidade = entry_valor_mensalidade.get()

    if cliente and barco and data_entrada and valor_mensalidade:
        # Calcula a data de vencimento (1 mês após a data de entrada)
        try:
            data_entrada_obj = datetime.strptime(data_entrada, "%d/%m/%Y")
            data_vencimento = data_entrada_obj + timedelta(days=30)
            data_vencimento_str = data_vencimento.strftime("%d/%m/%Y")
        except ValueError:
            messagebox.showwarning("Erro", "Data de entrada deve estar no formato DD/MM/AAAA.")
            return

        with open("dados_clientes.txt", "a") as file:
            file.write(f"{cliente};{barco};{data_entrada};{valor_mensalidade};{data_vencimento_str};Não Pago\n")

        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
        limpar_campos()
        abrir_nova_tela()  # Abre a nova tela com os dados
    else:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")

# Função para limpar os campos de entrada
def limpar_campos():
    entry_cliente.delete(0, ctk.END)
    entry_barco.delete(0, ctk.END)
    entry_data_entrada.delete(0, ctk.END)
    entry_valor_mensalidade.delete(0, ctk.END)

# Função para confirmar pagamento
def confirmar_pagamento(index, status_label):
    # Lê os dados do arquivo
    dados = carregar_dados()
    if index < len(dados):
        cliente_info = dados[index].strip().split(";")
        cliente_info[5] = "Pago"  # Atualiza o status

        # Calcula a nova data de vencimento (um mês após a data atual)
        data_vencimento_obj = datetime.strptime(cliente_info[4], "%d/%m/%Y")
        nova_data_vencimento = data_vencimento_obj + timedelta(days=30)
        cliente_info[4] = nova_data_vencimento.strftime("%d/%m/%Y")  # Atualiza a nova data de vencimento
        dados[index] = ";".join(cliente_info) + "\n"  # Atualiza a linha

        # Salva os dados atualizados no arquivo
        with open("dados_clientes.txt", "w") as file:
            file.writelines(dados)

        # Atualiza o label de status
        status_label.configure(text="Pago")
        messagebox.showinfo("Sucesso", "Pagamento confirmado! Data de vencimento atualizada.")

# Função para abrir uma janela para alterar a data de vencimento
def alterar_data_vencimento(index):
    def salvar_nova_data():
        nova_data = entry_nova_data.get()
        try:
            nova_data_obj = datetime.strptime(nova_data, "%d/%m/%Y")
            # Atualiza a data de vencimento no arquivo
            dados = carregar_dados()
            if index < len(dados):
                cliente_info = dados[index].strip().split(";")
                cliente_info[4] = nova_data_obj.strftime("%d/%m/%Y")  # Atualiza a nova data de vencimento
                dados[index] = ";".join(cliente_info) + "\n"  # Atualiza a linha

                # Salva os dados atualizados no arquivo
                with open("dados_clientes.txt", "w") as file:
                    file.writelines(dados)

                messagebox.showinfo("Sucesso", "Data de vencimento atualizada com sucesso!")
                nova_tela.destroy()  # Fecha a janela de alteração
            else:
                messagebox.showwarning("Erro", "Índice inválido.")
        except ValueError:
            messagebox.showwarning("Erro", "Data deve estar no formato DD/MM/AAAA.")

    # Cria uma nova janela para entrada da nova data
    nova_tela = ctk.CTkToplevel(root)
    nova_tela.title("Alterar Data de Vencimento")
    nova_tela.geometry("300x200")

    label_nova_data = ctk.CTkLabel(nova_tela, text="Nova Data de Vencimento (DD/MM/AAAA):")
    label_nova_data.pack(pady=10)

    entry_nova_data = ctk.CTkEntry(nova_tela)
    entry_nova_data.pack(pady=10)

    button_salvar = ctk.CTkButton(nova_tela, text="Salvar", command=salvar_nova_data)
    button_salvar.pack(pady=10)

# Função para abrir a nova tela de dados
def abrir_nova_tela():
    nova_tela = ctk.CTkToplevel(root)
    nova_tela.title("Dados Registrados")
    nova_tela.geometry("600x400")
    
    label_dados = ctk.CTkLabel(nova_tela, text="Dados dos Clientes:")
    label_dados.pack(pady=10)

    # Frame para lista de clientes
    frame_clientes = ctk.CTkScrollableFrame(nova_tela, width=550, height=300)
    frame_clientes.pack(pady=10)

    # Carrega os dados na nova tela
    dados = carregar_dados()
    for index, linha in enumerate(dados):
        cliente_info = linha.strip().split(";")
        if len(cliente_info) == 6:  # Adicionamos um campo para o status do pagamento
            # Criando um Frame para cada cliente
            cliente_frame = ctk.CTkFrame(frame_clientes, fg_color="#e0e0e0")  # Cor de fundo do Frame
            cliente_frame.pack(pady=5, padx=10, fill="x")

            # Adicionando as informações do cliente ao frame com cores
            ctk.CTkLabel(cliente_frame, text="Cliente:", anchor="w", fg_color="#cce5ff").pack(anchor="w", padx=10, pady=2)
            ctk.CTkLabel(cliente_frame, text=cliente_info[0], anchor="w").pack(anchor="w", padx=10)

            ctk.CTkLabel(cliente_frame, text="Barco:", anchor="w", fg_color="#cce5ff").pack(anchor="w", padx=10, pady=2)
            ctk.CTkLabel(cliente_frame, text=cliente_info[1], anchor="w").pack(anchor="w", padx=10)

            ctk.CTkLabel(cliente_frame, text="Data de Entrada:", anchor="w", fg_color="#cce5ff").pack(anchor="w", padx=10, pady=2)
            ctk.CTkLabel(cliente_frame, text=cliente_info[2], anchor="w").pack(anchor="w", padx=10)

            ctk.CTkLabel(cliente_frame, text="Valor Mensalidade:", anchor="w", fg_color="#cce5ff").pack(anchor="w", padx=10, pady=2)
            ctk.CTkLabel(cliente_frame, text=cliente_info[3], anchor="w").pack(anchor="w", padx=10)

            ctk.CTkLabel(cliente_frame, text="Data de Vencimento:", anchor="w", fg_color="#cce5ff").pack(anchor="w", padx=10, pady=2)
            ctk.CTkLabel(cliente_frame, text=cliente_info[4], anchor="w").pack(anchor="w", padx=10)

            ctk.CTkLabel(cliente_frame, text="Status:", anchor="w", fg_color="#cce5ff").pack(anchor="w", padx=10, pady=2)
            status_label = ctk.CTkLabel(cliente_frame, text=cliente_info[5], anchor="w")
            status_label.pack(anchor="w", padx=10)

            # Botão para confirmar pagamento
            confirmar_button = ctk.CTkButton(cliente_frame, text="Confirmar Pagamento", 
                                               command=lambda i=index, sl=status_label: confirmar_pagamento(i, sl))
            confirmar_button.pack(pady=5)

            # Botão para alterar a data de vencimento
            alterar_button = ctk.CTkButton(cliente_frame, text="Alterar Data de Vencimento",
                                            command=lambda i=index: alterar_data_vencimento(i))
            alterar_button.pack(pady=5)

# Função para centralizar e organizar os elementos na tela principal
def criar_layout_responsivo():
    # Usando grid para criar um layout mais flexível e responsivo
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.grid_rowconfigure(4, weight=1)
    root.grid_rowconfigure(5, weight=1)

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

    label_cliente.grid(row=0, column=1, pady=10, sticky="ew")
    entry_cliente.grid(row=1, column=1, pady=10, sticky="ew")

    label_barco.grid(row=2, column=1, pady=10, sticky="ew")
    entry_barco.grid(row=3, column=1, pady=10, sticky="ew")

    label_data_entrada.grid(row=4, column=1, pady=10, sticky="ew")
    entry_data_entrada.grid(row=5, column=1, pady=10, sticky="ew")

    label_valor_mensalidade.grid(row=6, column=1, pady=10, sticky="ew")
    entry_valor_mensalidade.grid(row=7, column=1, pady=10, sticky="ew")

    button_salvar.grid(row=8, column=1, pady=10, sticky="ew")

# Criando a janela principal
ctk.set_appearance_mode("light")  # ou "dark"
ctk.set_default_color_theme("blue")  # ou "dark-blue", "green", etc.

root = ctk.CTk()  # Usando CTk para criar a janela principal
root.title("Registro de Clientes")
root.geometry("600x500")  # Tamanho inicial da janela

# Definindo estilo
bg_color = "#f0f0f0"
root.configure(bg=bg_color)

# Criando labels e entradas
label_cliente = ctk.CTkLabel(root, text="Nome do Cliente:")
entry_cliente = ctk.CTkEntry(root)

label_barco = ctk.CTkLabel(root, text="Nome do Barco:")
entry_barco = ctk.CTkEntry(root)

label_data_entrada = ctk.CTkLabel(root, text="Data de Entrada (DD/MM/AAAA):")
entry_data_entrada = ctk.CTkEntry(root)

label_valor_mensalidade = ctk.CTkLabel(root, text="Valor Mensalidade:")
entry_valor_mensalidade = ctk.CTkEntry(root)

button_salvar = ctk.CTkButton(root, text="Salvar", command=salvar_dados)

# Chama a função para criar o layout responsivo
criar_layout_responsivo()

def alterar_data_vencimento(index):
    # Função interna para salvar a nova data e fechar a janela
    def salvar_nova_data():
        nova_data = entry_nova_data.get()
        try:
            nova_data_obj = datetime.strptime(nova_data, "%d/%m/%Y")
            # Atualiza a data de vencimento no arquivo
            dados = carregar_dados()
            if index < len(dados):
                cliente_info = dados[index].strip().split(";")
                cliente_info[4] = nova_data_obj.strftime("%d/%m/%Y")  # Atualiza a nova data de vencimento
                dados[index] = ";".join(cliente_info) + "\n"  # Atualiza a linha

                # Salva os dados atualizados no arquivo
                with open("dados_clientes.txt", "w") as file:
                    file.writelines(dados)

                messagebox.showinfo("Sucesso", "Data de vencimento atualizada com sucesso!")
                nova_tela.destroy()  # Fecha a janela de alteração
            else:
                messagebox.showwarning("Erro", "Índice inválido.")
        except ValueError:
            messagebox.showwarning("Erro", "Data deve estar no formato DD/MM/AAAA.")

    # Cria uma nova janela para entrada da nova data
    nova_tela = ctk.CTkToplevel(root)
    nova_tela.title("Alterar Data de Vencimento")
    nova_tela.geometry("300x200")

    label_nova_data = ctk.CTkLabel(nova_tela, text="Nova Data de Vencimento (DD/MM/AAAA):")
    label_nova_data.pack(pady=10)

    entry_nova_data = ctk.CTkEntry(nova_tela)
    entry_nova_data.pack(pady=10)

    button_salvar = ctk.CTkButton(nova_tela, text="Salvar", command=salvar_nova_data)
    button_salvar.pack(pady=10)

    # Adicionando um botão para fechar a janela
    button_fechar = ctk.CTkButton(nova_tela, text="Fechar", command=nova_tela.destroy)
    button_fechar.pack(pady=5)


def alterar_data_vencimento(index):
    # Função interna para salvar a nova data e fechar a janela
    def salvar_nova_data():
        nova_data = entry_nova_data.get()
        try:
            nova_data_obj = datetime.strptime(nova_data, "%d/%m/%Y")
            # Atualiza a data de vencimento no arquivo
            dados = carregar_dados()
            if index < len(dados):
                cliente_info = dados[index].strip().split(";")
                cliente_info[4] = nova_data_obj.strftime("%d/%m/%Y")  # Atualiza a nova data de vencimento
                dados[index] = ";".join(cliente_info) + "\n"  # Atualiza a linha

                # Salva os dados atualizados no arquivo
                with open("dados_clientes.txt", "w") as file:
                    file.writelines(dados)

                messagebox.showinfo("Sucesso", "Data de vencimento atualizada com sucesso!")
                nova_tela.destroy()  # Fecha a janela de alteração
                abrir_nova_tela()  # Reabre a tela de dados para mostrar as alterações
            else:
                messagebox.showwarning("Erro", "Índice inválido.")
        except ValueError:
            messagebox.showwarning("Erro", "Data deve estar no formato DD/MM/AAAA.")

    # Cria uma nova janela para entrada da nova data
    nova_tela = ctk.CTkToplevel(root)
    nova_tela.title("Alterar Data de Vencimento")
    nova_tela.geometry("300x200")

    label_nova_data = ctk.CTkLabel(nova_tela, text="Nova Data de Vencimento (DD/MM/AAAA):")
    label_nova_data.pack(pady=10)

    entry_nova_data = ctk.CTkEntry(nova_tela)
    entry_nova_data.pack(pady=10)

    button_salvar = ctk.CTkButton(nova_tela, text="Salvar", command=salvar_nova_data)
    button_salvar.pack(pady=10)

    # Adicionando um botão para fechar a janela
    button_fechar = ctk.CTkButton(nova_tela, text="Fechar", command=nova_tela.destroy)
    button_fechar.pack(pady=5)



# Inicia o loop da interface
root.mainloop()
