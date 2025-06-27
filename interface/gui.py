import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
import numpy as np
from tkinter import Toplevel, ttk
from tkinter import messagebox



# Importar os métodos
from core.methods.galerkin_method import GalerkinMethod
from core.methods.rayleigh_ritz_method import RayleighRitzMethod
from core.methods.least_squares_method import LeastSquaresMethod
from core.methods.moments_method import MomentsMethod
from core.methods.colocacao_method import CollocationMethod
from core.methods.SubregionsMethod import SubregionsMethod


class EDPSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparador de Métodos para EDPs")

        # Frame de controle
        self.controls = tk.Frame(root)
        self.controls.pack(padx=10, pady=10)

        # Label para seleção de métodos
        tk.Label(self.controls, text="Selecione os métodos:").grid(row=0, column=0, sticky="w")
        
        # Opções de métodos com checkboxes
        self.opcoes_metodos = {
            "Galerkin": tk.BooleanVar(value=True),
            "Rayleigh-Ritz": tk.BooleanVar(value=False),
            "Least Squares": tk.BooleanVar(value=False),
            "Momentos": tk.BooleanVar(value=False),
            "Colocação": tk.BooleanVar(value=False),
            "Sub-regiões": tk.BooleanVar(value=False)
        }

        # Criar checkboxes para cada método
        for i, (nome, var) in enumerate(self.opcoes_metodos.items()):
            tk.Checkbutton(self.controls, text=nome, variable=var).grid(row=1 + i // 2, column=i % 2, sticky="w")

        # Número de termos
        tk.Label(self.controls, text="n_terms:").grid(row=4, column=0, sticky="w")
        self.terms_var = tk.IntVar(value=3)
        tk.Spinbox(self.controls, from_=1, to=10, textvariable=self.terms_var).grid(row=4, column=1, padx=5)

        # Botão de resolver
        self.solve_button = tk.Button(self.controls, text="Resolver", command=self.rodar_metodo)
        self.solve_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Botão para mostrar tabela de erros
        self.table_button = tk.Button(self.controls, text="Mostrar Tabela de Erros", command=self.mostrar_tabela)
        self.table_button.grid(row=6, column=0, columnspan=2, pady=5)

        # Área do gráfico
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        # Dicionário para armazenar erros
        self.erros_calculados = {}

    def rodar_metodo(self):
        n_terms = self.terms_var.get()

        x = sp.Symbol('x')
        f_de_x = sp.pi**2 * sp.sin(sp.pi * x)
        domain = (0, 1)
        condicoes = [(0, 0), (1, 0)]

        metodos_classes = {
            "Galerkin": GalerkinMethod,
            "Rayleigh-Ritz": RayleighRitzMethod,
            "Least Squares": LeastSquaresMethod,
            "Momentos": MomentsMethod,
            "Colocação": CollocationMethod,
            "Sub-regiões": SubregionsMethod
        }

        # Limpar gráfico
        self.ax.clear()
        
        # Plotar solução exata
        x_vals = np.linspace(0, 1, 200)
        y_real = np.sin(np.pi * x_vals)
        self.ax.plot(x_vals, y_real, 'k-', linewidth=3, label="Solução Exata: sin(πx)")

        # Limpar erros anteriores
        self.erros_calculados = {}

        # Cores para diferentes métodos
        cores = ['blue', 'red', 'green', 'purple', 'orange', 'brown']

        # Executar métodos selecionados
        for i, (metodo_nome, var) in enumerate(self.opcoes_metodos.items()):
            if var.get():  # Se o método estiver selecionado
                try:
                    metodo_classe = metodos_classes[metodo_nome]
                    metodo = metodo_classe(f_de_x, domain, condicoes)
                    sol = metodo.solve(n_terms=n_terms)
                    
                    if sol is not None:
                        u_aprox = sp.lambdify(x, sol, modules=['numpy'])
                        y_aprox = u_aprox(x_vals)
                        erro_max = np.max(np.abs(y_aprox - y_real))
                        
                        # Armazenar erro
                        self.erros_calculados[metodo_nome] = erro_max
                        
                        # Plotar
                        self.ax.plot(x_vals, y_aprox, '--', linewidth=2, 
                                   color=cores[i % len(cores)], 
                                   label=f"{metodo_nome} (erro: {erro_max:.1e})")
                    else:
                        self.erros_calculados[metodo_nome] = float('inf')
                        print(f"Erro: {metodo_nome} retornou None")
                        
                except Exception as e:
                    self.erros_calculados[metodo_nome] = float('inf')
                    print(f"Erro ao executar {metodo_nome}: {e}")

        # Configurar gráfico
        self.ax.set_title(f"Comparação dos Métodos com n_terms = {n_terms}")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("u(x)")
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        self.canvas.draw()

    def mostrar_tabela(self):
        if not self.erros_calculados:
            tk.messagebox.showwarning("Aviso", "Execute os métodos primeiro!")
            return
        
        mostrar_tabela_erros(self.erros_calculados)


def mostrar_tabela_erros(erros_dict):
    janela = Toplevel()
    janela.title("Tabela de Erros Máximos")
    janela.geometry("300x200")

    tabela = ttk.Treeview(janela, columns=("Método", "Erro Máximo"), show="headings")
    tabela.heading("Método", text="Método")
    tabela.heading("Erro Máximo", text="Erro Máximo")
    tabela.column("Método", width=150)
    tabela.column("Erro Máximo", width=120)

    for metodo, erro in erros_dict.items():
        if erro == float('inf'):
            erro_str = "Erro"
        else:
            erro_str = f"{erro:.2e}"
        tabela.insert("", "end", values=(metodo, erro_str))

    tabela.pack(expand=True, fill="both", padx=10, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = EDPSolverGUI(root)
    root.mainloop()