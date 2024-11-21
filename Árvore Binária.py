import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
        if value == node.value:
            raise ValueError("Números duplicados não são permitidos na árvore.")
        elif value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)

    def remove(self, value):
        self.root = self._remove_recursive(self.root, value)

    def _remove_recursive(self, node, value):
        if node is None:
            raise ValueError("Valor não encontrado na árvore.")
        if value < node.value:
            node.left = self._remove_recursive(node.left, value)
        elif value > node.value:
            node.right = self._remove_recursive(node.right, value)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._remove_recursive(node.right, temp.value)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def draw_tree(self, ax, node=None, x=0, y=0, dx=10, level=0):
        if node is None:
            node = self.root
        if node is not None:
            ax.text(x, y, str(node.value), fontsize=10, ha='center', va='center',
                    bbox=dict(boxstyle="circle", facecolor="#ffd700", edgecolor="black"))
            if node.left:
                ax.plot([x, x - dx], [y, y - 10], color="green", linewidth=2)
                self.draw_tree(ax, node.left, x - dx, y - 10, dx / 2, level + 1)
            if node.right:
                ax.plot([x, x + dx], [y, y - 10], color="blue", linewidth=2)
                self.draw_tree(ax, node.right, x + dx, y - 10, dx / 2, level + 1)


class BinaryTreeApp:
    def __init__(self):
        self.tree = BinaryTree()
        self.window = tk.Tk()
        self.window.title("Árvore Binária Visual")
        self.window.geometry("900x700")
        self.window.config(bg="#282c34")
        self.create_widgets()

    def create_widgets(self):
        # Fontes
        font_title = tkFont.Font(family="Helvetica", size=20, weight="bold")
        font_label = tkFont.Font(family="Helvetica", size=14)
        font_button = tkFont.Font(family="Helvetica", size=12, weight="bold")

        # Título
        self.title_label = tk.Label(
            self.window, text="Árvore Binária Visual", font=font_title, bg="#282c34", fg="#ffd700"
        )
        self.title_label.pack(pady=20)

        # Entrada para inserir
        self.insert_label = tk.Label(
            self.window, text="Inserir valor:", font=font_label, bg="#282c34", fg="#ffffff"
        )
        self.insert_label.pack()
        self.insert_entry = tk.Entry(self.window, font=font_label, bg="#3c3f41", fg="#ffffff")
        self.insert_entry.pack(pady=5)
        self.insert_button = tk.Button(
            self.window, text="Inserir", font=font_button, bg="#4caf50", fg="#ffffff", command=self.insert_value
        )
        self.insert_button.pack(pady=5)

        # Entrada para remover
        self.remove_label = tk.Label(
            self.window, text="Remover valor:", font=font_label, bg="#282c34", fg="#ffffff"
        )
        self.remove_label.pack()
        self.remove_entry = tk.Entry(self.window, font=font_label, bg="#3c3f41", fg="#ffffff")
        self.remove_entry.pack(pady=5)
        self.remove_button = tk.Button(
            self.window, text="Remover", font=font_button, bg="#f44336", fg="#ffffff", command=self.remove_value
        )
        self.remove_button.pack(pady=5)

        # Canvas para exibir a árvore
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.ax.axis("off")
        self.ax.set_facecolor("#3c3f41")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

    def insert_value(self):
        try:
            value = int(self.insert_entry.get())
            self.tree.insert(value)
            self.insert_entry.delete(0, tk.END)
            self.update_tree()
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def remove_value(self):
        try:
            value = int(self.remove_entry.get())
            self.tree.remove(value)
            self.remove_entry.delete(0, tk.END)
            self.update_tree()
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def update_tree(self):
        self.ax.clear()
        self.ax.axis("off")
        self.tree.draw_tree(self.ax, dx=50)
        self.canvas.draw()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = BinaryTreeApp()
    app.run()
