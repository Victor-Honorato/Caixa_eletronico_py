import tkinter as tk
from tkinter import simpledialog, messagebox

class Banco:
    def __init__(self, nome):
        self.nome = nome
        self.saldo = 0

    def depositar(self, valor):
        # Função para realizar um depósito na conta do banco
        self.saldo += valor

    def sacar(self, valor):
        # Função para realizar um saque na conta do banco
        if valor <= self.saldo:
            self.saldo -= valor
            return True
        else:
            # Exibe uma mensagem de erro se o saldo for insuficiente
            messagebox.showerror("Erro", "Saldo insuficiente. Saque não realizado.")
            return False

    def extrato(self):
        # Retorna uma string formatada com o extrato da conta
        return f"Saldo atual: R${self.saldo:.2f}"

class InterfaceGrafica:
    def __init__(self, master):
        self.master = master
        self.master.title("Aplicativo Bancário")
        self.master.geometry("350x350")

        self.bancos = {
            "Nubank": Banco("Nubank"),
            "Caixa": Banco("Caixa"),
            "BRB": Banco("BRB")
        }

        self.banco_atual = None

        self.frame_principal = tk.Frame(master, padx=20, pady=20)
        self.frame_principal.pack()

        self.label_titulo = tk.Label(self.frame_principal, text="Bem-vindo ao Aplicativo Bancário", font=("Arial", 14, "bold"))
        self.label_titulo.pack(pady=10)

        self.frame_escolher_banco = tk.Frame(self.frame_principal)

        self.botao_escolher_banco = tk.Button(self.frame_escolher_banco, text="Escolher Banco", command=self.exibir_opcoes_banco, width=15)
        self.botao_escolher_banco.grid(row=0, column=0, padx=5, pady=10)

        self.opcoes_bancos = tk.StringVar(value=list(self.bancos.keys()))
        self.lista_bancos = tk.OptionMenu(self.frame_escolher_banco, self.opcoes_bancos, *self.bancos.keys())
        self.lista_bancos.grid(row=0, column=1, padx=5, pady=10)

        self.botao_selecionar = tk.Button(self.frame_escolher_banco, text="Selecionar", command=self.selecionar_banco, width=15)
        self.botao_selecionar.grid(row=0, column=2, padx=5, pady=10)

        self.frame_escolher_banco.pack()

        self.frame_opcoes_banco = tk.Frame(self.frame_principal)

        self.label_saldo = tk.Label(self.frame_opcoes_banco, text="")
        self.label_saldo.pack(pady=10)

        self.botao_depositar = tk.Button(self.frame_opcoes_banco, text="Depositar", command=self.depositar, state=tk.DISABLED)
        self.botao_depositar.pack(pady=10)

        self.botao_sacar = tk.Button(self.frame_opcoes_banco, text="Sacar", command=self.sacar, state=tk.DISABLED)
        self.botao_sacar.pack(pady=10)

        self.botao_extrato = tk.Button(self.frame_opcoes_banco, text="Extrato", command=self.mostrar_extrato, state=tk.DISABLED)
        self.botao_extrato.pack(pady=10)

        self.botao_voltar = tk.Button(self.frame_opcoes_banco, text="⬅️ Voltar", command=self.voltar, state=tk.DISABLED)
        self.botao_voltar.pack(side=tk.LEFT, padx=10, pady=10)

        self.botao_sair = tk.Button(self.frame_opcoes_banco, text="Sair", command=self.sair, state=tk.DISABLED)
        self.botao_sair.pack(side=tk.RIGHT, padx=10, pady=10)

        self.barra_status = tk.Label(self.frame_principal, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.barra_status.pack(side=tk.BOTTOM, fill=tk.X)

    def exibir_opcoes_banco(self):
        # Função para exibir as opções do banco ao clicar no botão "Escolher Banco"
        self.frame_escolher_banco.pack_forget()
        self.frame_opcoes_banco.pack()
        self.botao_selecionar["state"] = tk.NORMAL
        self.botao_voltar["state"] = tk.NORMAL

    def atualizar_saldo(self):
        # Função para atualizar o rótulo de saldo com o saldo atual do banco
        if self.banco_atual:
            self.label_saldo["text"] = f"Saldo: R${self.banco_atual.saldo:.2f}"

    def selecionar_banco(self):
        # Função para selecionar o banco escolhido e exibir uma mensagem
        banco_selecionado = self.opcoes_bancos.get()
        self.banco_atual = self.bancos[banco_selecionado]
        self.atualizar_saldo()
        self.mostrar_mensagem_status(f"Banco {banco_selecionado} selecionado.")
        self.habilitar_opcoes_banco()

    def habilitar_opcoes_banco(self):
        # Função para habilitar os botões após selecionar o banco
        self.botao_depositar["state"] = tk.NORMAL
        self.botao_sacar["state"] = tk.NORMAL
        self.botao_extrato["state"] = tk.NORMAL
        self.botao_sair["state"] = tk.NORMAL
        self.botao_voltar["state"] = tk.DISABLED

    def depositar(self):
        # Função para realizar um depósito, exibindo uma caixa de diálogo para inserir o valor
        if self.banco_atual:
            valor_deposito = float(simpledialog.askstring("Depositar", "Digite o valor a depositar:"))
            self.banco_atual.depositar(valor_deposito)
            self.atualizar_saldo()
            self.mostrar_mensagem_status("Depósito realizado com sucesso!")

    def sacar(self):
        # Função para realizar um saque, exibindo uma caixa de diálogo para inserir o valor
        if self.banco_atual:
            valor_saque = float(simpledialog.askstring("Sacar", "Digite o valor a sacar:"))
            if self.banco_atual.sacar(valor_saque):
                self.atualizar_saldo()
                self.mostrar_mensagem_status("Saque realizado com sucesso!")

    def mostrar_extrato(self):
        # Função para exibir um diálogo com o extrato da conta bancária
        if self.banco_atual:
            extrato = self.banco_atual.extrato()
            messagebox.showinfo("Extrato", extrato)

    def sair(self):
        # Função para fechar o aplicativo
        self.master.destroy()

    def mostrar_mensagem_status(self, mensagem):
        # Função para exibir mensagens na barra de status
        self.barra_status["text"] = mensagem

    def voltar(self):
        # Função para voltar à tela de escolha do banco
        self.frame_opcoes_banco.pack_forget()
        self.frame_escolher_banco.pack()
        self.botao_selecionar["state"] = tk.NORMAL
        self.botao_voltar["state"] = tk.DISABLED

def main():
    # Função principal para iniciar o aplicativo
    root = tk.Tk()
    app = InterfaceGrafica(root)
    root.mainloop()

if __name__ == "__main__":
    main()
