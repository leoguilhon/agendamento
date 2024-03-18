import sqlite3
import tkinter as tk
from utils import *
from tkinter import ttk, messagebox

#Estabelece a conexão com o banco de dados (se não existir, será criado)
conn = sqlite3.connect('consultorio.db')

#Criando um cursor para executar comandos SQL
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS visitantes
            (id INTEGER PRIMARY KEY, nome VARCHAR(50), telefone VARCHAR(11), cpf VARCHAR(11), email VARCHAR(50), idade INTEGER, sexo VARCHAR(50), data_agendamento VARCHAR(10), especialidade VARCHAR(50))''')


def salvarAgendamento(janela_agendamento, treeview):
    # Obtenção dos dados inseridos
    nome = entry_nome.get()
    telefone = entry_telefone.get()
    cpf = entry_cpf.get()
    email = entry_email.get()
    idade = entry_idade.get()
    sexo = entry_sexo.get()
    data_agendamento = entry_data_agendamento.get()
    especialidade = entry_especialidade.get()
    
    # Validar os dados inseridos
    if not nome or not nome.replace(" ", "").isalpha():
        messagebox.showerror("Erro", "Nome inválido")
        janela_agendamento.focus_force()
        return
    if not cpf or not re.match(r'^\d{11}$', cpf):
        messagebox.showerror("Erro", "CPF inválido")
        janela_agendamento.focus_force()
        return
    if not email or '@' not in email:
        messagebox.showerror("Erro", "E-mail inválido")
        janela_agendamento.focus_force()
        return
    if not telefone or not telefone.isdigit():
        messagebox.showerror("Erro", "Telefone inválido")
        janela_agendamento.focus_force()
        return
    if not idade or not idade.isdigit():
        messagebox.showerror("Erro", "Idade inválida")
        janela_agendamento.focus_force()
        return
    if not data_agendamento or not re.match(r'^\d{2}/\d{2}/\d{4}$', data_agendamento):
        messagebox.showerror("Erro", "Data de agendamento inválida")
        janela_agendamento.focus_force()
        return

    # Inserir dados
    cursor.execute("INSERT INTO visitantes (nome, telefone, cpf, email, idade, sexo, data_agendamento, especialidade) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (nome, telefone, cpf, email, idade, sexo, data_agendamento, especialidade))
    conn.commit()
    print(f'Agendamento de {nome} para {especialidade} no dia {data_agendamento} realizado com sucesso.')
    listarAgendamentos(treeview)
    janela_agendamento.destroy()
    

def criarJanelaIncluirAgendamento(treeview):
    janela_agendamento = tk.Toplevel(root)
    janela_agendamento.title("Novo Agendamento")
    janela_agendamento.resizable(False, False)

    # Labels e Entradas para os dados de agendamento
    tk.Label(janela_agendamento, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(janela_agendamento, text="Telefone:").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(janela_agendamento, text="CPF:").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(janela_agendamento, text="Email:").grid(row=3, column=0, padx=5, pady=5)
    tk.Label(janela_agendamento, text="Idade:").grid(row=4, column=0, padx=5, pady=5)
    tk.Label(janela_agendamento, text="Sexo:").grid(row=5, column=0, padx=5, pady=5)
    tk.Label(janela_agendamento, text="Data Agendamento:").grid(row=6, column=0, padx=5, pady=5)
    tk.Label(janela_agendamento, text="Especialidade:").grid(row=7, column=0, padx=5, pady=5)

    global entry_nome, entry_telefone, entry_cpf, entry_email, entry_idade, entry_sexo, entry_data_agendamento, entry_especialidade

    entry_nome = tk.Entry(janela_agendamento)
    entry_nome.grid(row=0, column=1, padx=5, pady=5)
    entry_telefone = tk.Entry(janela_agendamento)
    entry_telefone.grid(row=1, column=1, padx=5, pady=5)
    entry_cpf = tk.Entry(janela_agendamento)
    entry_cpf.grid(row=2, column=1, padx=5, pady=5)
    entry_email = tk.Entry(janela_agendamento)
    entry_email.grid(row=3, column=1, padx=5, pady=5)
    entry_idade = tk.Entry(janela_agendamento)
    entry_idade.grid(row=4, column=1, padx=5, pady=5)
    entry_sexo = tk.Entry(janela_agendamento)
    entry_sexo.grid(row=5, column=1, padx=5, pady=5)
    entry_data_agendamento = tk.Entry(janela_agendamento)
    entry_data_agendamento.grid(row=6, column=1, padx=5, pady=5)
    entry_especialidade = tk.Entry(janela_agendamento)
    entry_especialidade.grid(row=7, column=1, padx=5, pady=5)

    # Botão para salvar o agendamento
    button_salvar = tk.Button(janela_agendamento, text="Salvar", command=lambda: salvarAgendamento(janela_agendamento, treeview))
    button_salvar.grid(row=8, column=0, columnspan=2, padx=5, pady=10)

def listarAgendamentos(treeview):
    # Limpar dados anteriores da Treeview
    for row in treeview.get_children():
        treeview.delete(row)

    cursor.execute("SELECT * FROM visitantes")
    visitantes = cursor.fetchall()

    # Adicionar visitantes à Treeview
    for visitante in visitantes:
        treeview.insert('', 'end', values=(visitante))

def deletarAgendamento(treeview):
    # Obter item selecionado na Treeview
    item_selecionado = treeview.selection()
    
    if item_selecionado:
        # Obter valores do item selecionado
        valores_item = treeview.item(item_selecionado, 'values')
        # Obter o ID do item selecionado
        id_agendamento = valores_item[0]
        
        resposta = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir o agendamento selecionado?")
        
        if resposta:
            # Excluir agendamento do banco de dados
            cursor.execute("DELETE FROM visitantes WHERE id=?", (id_agendamento,))
            conn.commit()
            messagebox.showinfo("Exclusão Concluída", "O agendamento foi excluído com sucesso.")
            # Atualizar a lista de agendamentos após a exclusão
            listarAgendamentos(treeview)
    else:
        messagebox.showwarning("Nenhum Item Selecionado", "Por favor, selecione um agendamento para excluir.")




def ordenar_coluna(treeview, coluna, reverse=False):
    dados = [(treeview.set(item, coluna), item) for item in treeview.get_children('')]
    try:
        # Tenta ordenar os dados convertendo para inteiros
        dados.sort(key=lambda x: int(x[0]), reverse=reverse)
    except ValueError:
        # Se a conversão falhar, ordena como strings
        dados.sort(reverse=reverse)
    
    for index, (_, item) in enumerate(dados):
        treeview.move(item, '', index)

    # Alterna a direção da ordenação para a próxima vez
    treeview.heading(coluna, command=lambda: ordenar_coluna(treeview, coluna, not reverse))

# Interface

root = tk.Tk()
root.title("Agendamentos")

# Define as dimensões da janela
root.geometry("800x600")

# Widget Treeview para exibir os agendamentos
treeview = ttk.Treeview(root, columns=("ID", "Nome", "Telefone", "CPF", "Email", "Idade", "Sexo", "Data Agendamento", "Especialidade"), show="headings")
treeview.pack(fill=tk.BOTH, expand=True)

treeview.heading("ID", text="ID", anchor=tk.CENTER, command=lambda: ordenar_coluna(treeview, "ID"))
treeview.column("ID", width=50, anchor=tk.CENTER)

treeview.heading("Nome", text="Nome", anchor=tk.CENTER, command=lambda: ordenar_coluna(treeview, "Nome"))
treeview.column("Nome", width=100, anchor=tk.CENTER)

treeview.heading("Telefone", text="Telefone", anchor=tk.CENTER, command=lambda: ordenar_coluna(treeview, "Telefone"))
treeview.column("Telefone", width=100, anchor=tk.CENTER)

treeview.heading("CPF", text="CPF", anchor=tk.CENTER, command=lambda: ordenar_coluna(treeview, "CPF"))
treeview.column("CPF", width=100, anchor=tk.CENTER)

treeview.heading("Email", text="Email", anchor=tk.CENTER, command=lambda: ordenar_coluna(treeview, "Email"))
treeview.column("Email", width=150, anchor=tk.CENTER)

treeview.heading("Idade", text="Idade", anchor=tk.CENTER, command=lambda: ordenar_coluna(treeview, "Idade"))
treeview.column("Idade", width=50, anchor=tk.CENTER)

treeview.heading("Sexo", text="Sexo", anchor=tk.CENTER, command=lambda: ordenar_coluna(treeview, "Sexo"))
treeview.column("Sexo", width=50, anchor=tk.CENTER)

treeview.heading("Data Agendamento", text="Data Agendamento", anchor=tk.CENTER, command=lambda: ordenar_coluna(treeview, "Data Agendamento"))
treeview.column("Data Agendamento", width=110, anchor=tk.CENTER)

treeview.heading("Especialidade", text="Especialidade", anchor=tk.CENTER, command=lambda: ordenar_coluna(treeview, "Especialidade"))
treeview.column("Especialidade", width=100, anchor=tk.CENTER)
treeview.pack(pady=10)

# Botão para incluir os agendamentos
button_incluir = tk.Button(root, text="Incluir Agendamento", command=lambda: criarJanelaIncluirAgendamento(treeview))
button_incluir.pack(pady=10)

# Botão para abrir a janela de exclusão
button_deletar = tk.Button(root, text="Deletar Agendamento", command=lambda: deletarAgendamento(treeview))
button_deletar.pack(pady=10)

listarAgendamentos(treeview)

root.mainloop()

conn.close()