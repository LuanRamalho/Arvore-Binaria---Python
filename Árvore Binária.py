import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)

    def draw_tree(self):
        return self._draw_recursive(self.root, 0, 300, 60, 200)

    def _draw_recursive(self, node, level, x, y, dx):
        if node is None:
            return []
        lines = []
        lines.append((x, y, node.value))
        left_lines = self._draw_recursive(node.left, level + 1, x - dx, y + 80, dx // 2)
        right_lines = self._draw_recursive(node.right, level + 1, x + dx, y + 80, dx // 2)
        lines.extend(left_lines)
        lines.extend(right_lines)
        return lines

class BinaryTreeApp:
    def __init__(self, root):
        self.window = tk.Tk()
        self.window.title("Árvore Binária Simples")
        self.window.geometry("800x600")
        self.window.config(bg="#f4f4f9")
        self.tree = BinaryTree()
        self.create_widgets()

    def create_widgets(self):
        # Fontes para os textos
        self.font_title = tkFont.Font(family="Helvetica", size=16, weight="bold")
        self.font_label = tkFont.Font(family="Helvetica", size=14)
        self.font_button = tkFont.Font(family="Helvetica", size=12, weight="bold")

        # Cabeçalho
        self.header_label = tk.Label(self.window, text="Árvore Binária Simples", font=self.font_title, bg="#f4f4f9", fg="#4b9cd3")
        self.header_label.pack(pady=10)

        # Instruções
        self.label = tk.Label(self.window, text="Digite um número para inserir na árvore:", font=self.font_label, bg="#f4f4f9", fg="#333")
        self.label.pack(pady=10)

        # Caixa de texto para o número
        self.entry = tk.Entry(self.window, font=self.font_label, width=20, bd=2, relief="solid", justify="center")
        self.entry.pack(pady=10)

        # Botão para inserir o número na árvore
        self.insert_button = tk.Button(self.window, text="Inserir", font=self.font_button, bg="#4b9cd3", fg="white", width=15, command=self.insert_number)
        self.insert_button.pack(pady=10)

        # Frame para o Canvas com as barras de rolagem
        self.canvas_frame = tk.Frame(self.window)
        self.canvas_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        # Barra de rolagem horizontal
        self.scroll_x = tk.Scrollbar(self.canvas_frame, orient="horizontal")
        self.scroll_x.grid(row=1, column=0, sticky="ew")

        # Barra de rolagem vertical
        self.scroll_y = tk.Scrollbar(self.canvas_frame, orient="vertical")
        self.scroll_y.grid(row=0, column=1, sticky="ns")

        # Canvas para desenhar a árvore
        self.canvas = tk.Canvas(self.canvas_frame, bg="#f0f0f0", bd=2, relief="solid",
                                xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Configura as barras de rolagem
        self.scroll_x.config(command=self.canvas.xview)
        self.scroll_y.config(command=self.canvas.yview)

        # Atualiza o layout do canvas e das barras de rolagem
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)

    def insert_number(self):
        try:
            value = int(self.entry.get())
            self.tree.insert(value)
            self.entry.delete(0, tk.END)
            self.draw_tree()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido.")

    def draw_tree(self):
        self.canvas.delete("all")  # Limpar o canvas antes de desenhar
        lines = self.tree.draw_tree()

        # Encontrar os limites para ajustar as barras de rolagem
        if lines:
            min_x = min([line[0] for line in lines])
            max_x = max([line[0] for line in lines])
            max_y = max([line[1] for line in lines])

            # Definir o scrollregion com base nos limites da árvore
            self.canvas.config(scrollregion=(min_x - 50, 0, max_x + 50, max_y + 80))  # Ajuste da área de rolagem

            # Desenhar a árvore
            for x, y, value in lines:
                # Desenhando o texto para o nó
                self.canvas.create_text(x, y, text=str(value), font=self.font_label, fill="black", anchor="center")
                # Desenhando as linhas para os nós filhos
                if x > 300:  # Filho à direita
                    self.canvas.create_line(x - 40, y + 40, x, y, fill="blue", width=2)
                elif x < 300:  # Filho à esquerda
                    self.canvas.create_line(x + 40, y + 40, x, y, fill="blue", width=2)

        self.canvas.update_idletasks()  # Atualiza o canvas para que as barras de rolagem funcionem corretamente

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = BinaryTreeApp(None)
    app.run()
