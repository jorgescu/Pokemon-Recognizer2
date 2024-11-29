# main.py

from src.interfaz import Aplicacion
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
