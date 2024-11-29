# src/interfaz.py

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from src.preprocesamiento import preprocesar_imagen
from src.clasificacion import predecir_pokemon

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Reconocedor de Pokémon")
        self.imagen_label = tk.Label(root)
        self.imagen_label.pack()
        self.descripcion_text = tk.Text(root, height=15, width=80)
        self.descripcion_text.pack()
        self.boton_cargar = tk.Button(root, text="Cargar Imagen", command=self.cargar_imagen)
        self.boton_cargar.pack()

    def cargar_imagen(self):
        ruta_imagen = filedialog.askopenfilename()
        if ruta_imagen:
            imagen = cv2.imread(ruta_imagen)
            imagen_procesada = preprocesar_imagen(ruta_imagen)
            nombre_pokemon, descripcion = predecir_pokemon(imagen_procesada)
            self.mostrar_imagen(imagen)
            self.mostrar_descripcion(descripcion)

    def mostrar_imagen(self, imagen):
        imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        imagen_pil = Image.fromarray(imagen_rgb)
        imagen_pil = imagen_pil.resize((256, 256))
        imagen_tk = ImageTk.PhotoImage(imagen_pil)
        self.imagen_label.configure(image=imagen_tk)
        self.imagen_label.image = imagen_tk

    def mostrar_descripcion(self, descripcion):
        self.descripcion_text.delete(1.0, tk.END)
        self.descripcion_text.insert(tk.END, descripcion)

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
