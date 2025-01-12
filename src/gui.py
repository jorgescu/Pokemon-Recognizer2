# src/gui.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import webbrowser
import tempfile
from src.battle_simulator import BattleSimulator  # Importar el módulo de simulación
import pandas as pd

class App(tk.Frame):
    def __init__(self, master, classifier, extractor, preprocessor, danger_evaluator, desc_generator, extras_manager,
                 knowledge_manager, vr_integration, images_path, df_pokemon):
        super().__init__(master)
        self.master = master
        self.classifier = classifier
        self.extractor = extractor
        self.preprocessor = preprocessor
        self.danger_evaluator = danger_evaluator
        self.desc_generator = desc_generator
        self.extras_manager = extras_manager
        self.knowledge_manager = knowledge_manager
        self.vr_integration = vr_integration
        self.images_path = images_path
        self.df_pokemon = df_pokemon  # Almacenar el DataFrame

        # Inicializar el simulador de batallas
        self.battle_simulator = BattleSimulator()

        # Asignar el DataFrame a una variable local
        self.pokemon_data = self.df_pokemon

        # Lista para almacenar la colección de Pokémon
        self.team = []

        # Configurar la barra de título y el tamaño de la ventana
        self.master.title("Reconocedor de Pokémon - Sistemas Inteligentes")
        self.master.geometry("1200x800")  # Ajustar tamaño inicial de la ventana

        # Crear Canvas y Scrollbar para la interfaz principal
        self.canvas = tk.Canvas(self.master, borderwidth=0, background="#f0f0f0")
        self.frame = tk.Frame(self.canvas, background="#f0f0f0")
        self.vsb = tk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        # Crear los widgets dentro de self.frame en lugar de self
        self.create_widgets()

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_widgets(self):
        # Sección de Cargar Imagen y Información
        info_frame = tk.Frame(self.frame, background="#f0f0f0")
        info_frame.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        # Botón de Cargar Imagen
        self.load_button = tk.Button(info_frame, text="Cargar Imagen de Pokémon", command=self.load_image, width=25, height=2)
        self.load_button.pack(side=tk.LEFT, padx=5)

        # Botón para ver el mapa de hábitat
        self.map_button = tk.Button(info_frame, text="Ver Mapa de Hábitat", command=self.view_habitat_map, width=20, height=2)
        self.map_button.pack(side=tk.LEFT, padx=5)

        # Botón para simular batalla
        self.battle_button = tk.Button(info_frame, text="Simular Batalla", command=self.simulate_battle, width=20, height=2)
        self.battle_button.pack(side=tk.LEFT, padx=5)

        # Sección de Información del Pokémon
        info_text_frame = tk.Frame(self.frame, background="#f0f0f0")
        info_text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10, padx=10)

        self.info_label = tk.Label(info_text_frame, text="Información del Pokémon:", font=("Arial", 14), background="#f0f0f0")
        self.info_label.pack(anchor='w')

        self.info_text = tk.Text(info_text_frame, height=15, width=100, wrap=tk.WORD)
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,5))

        # Scrollbar para el cuadro de información
        info_scrollbar = tk.Scrollbar(info_text_frame, command=self.info_text.yview)
        info_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.info_text.configure(yscrollcommand=info_scrollbar.set)

        # Sección de Recomendaciones y Noticias
        recommendations_news_frame = tk.Frame(self.frame, background="#f0f0f0")
        recommendations_news_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10, padx=10)

        # Recomendaciones
        rec_frame = tk.Frame(recommendations_news_frame, background="#f0f0f0")
        rec_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.recommendations_label = tk.Label(rec_frame, text="Recomendaciones similares:", font=("Arial", 14), background="#f0f0f0")
        self.recommendations_label.pack(anchor='w')

        self.recommendations_box = tk.Listbox(rec_frame, width=40, height=10)
        self.recommendations_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar para recomendaciones
        rec_scrollbar = tk.Scrollbar(rec_frame, command=self.recommendations_box.yview)
        rec_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.recommendations_box.configure(yscrollcommand=rec_scrollbar.set)

        # Noticias
        news_frame = tk.Frame(recommendations_news_frame, background="#f0f0f0")
        news_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.news_label = tk.Label(news_frame, text="Noticias:", font=("Arial", 14), background="#f0f0f0")
        self.news_label.pack(anchor='w')

        self.news_box = tk.Listbox(news_frame, width=40, height=10)
        self.news_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar para noticias
        news_scrollbar = tk.Scrollbar(news_frame, command=self.news_box.yview)
        news_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.news_box.configure(yscrollcommand=news_scrollbar.set)

        # Sección de Preguntas (Chat simple)
        chat_frame = tk.Frame(self.frame, background="#f0f0f0")
        chat_frame.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        self.question_label = tk.Label(chat_frame, text="Haz una pregunta sobre Pokémon o el sistema inteligente:",
                                       font=("Arial", 14), background="#f0f0f0")
        self.question_label.pack(anchor='w')

        self.question_entry = tk.Entry(chat_frame, width=80)
        self.question_entry.pack(side=tk.LEFT, padx=(0,5), pady=5)

        self.ask_button = tk.Button(chat_frame, text="Preguntar", command=self.ask_question, width=10)
        self.ask_button.pack(side=tk.LEFT, padx=5)

        # Sección de Instrucciones para la Batalla
        battle_instructions_frame = tk.Frame(self.frame, background="#f0f0f0")
        battle_instructions_frame.pack(side=tk.TOP, fill=tk.X, pady=5, padx=10)

        battle_instructions_label = tk.Label(
            battle_instructions_frame,
            text="Selecciona exactamente dos Pokémon en la colección para simular una batalla.\n"
                 "Usa Shift + Click para seleccionar un rango o Ctrl + Click para selecciones individuales.",
            font=("Arial", 10),
            justify=tk.LEFT,
            background="#f0f0f0"
        )
        battle_instructions_label.pack(anchor='w')

        # Botón para integrar con entorno virtual
        vr_frame = tk.Frame(self.frame, background="#f0f0f0")
        vr_frame.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        self.vr_button = tk.Button(vr_frame, text="Colocar Pokémon en entorno virtual 3D", command=self.place_in_vr, width=35, height=2)
        self.vr_button.pack()

        # Sección de Colección de Pokémon
        collection_frame = tk.Frame(self.frame, borderwidth=2, relief=tk.GROOVE, background="#f0f0f0")
        collection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10, padx=10)

        self.collection_label = tk.Label(collection_frame, text="Colección de Pokémon:", font=("Arial", 14), background="#f0f0f0")
        self.collection_label.pack(anchor='w')

        # Aumentar el tamaño del Listbox de la colección y permitir selección múltiple
        self.team_box = tk.Listbox(collection_frame, width=50, height=15, selectmode='extended')
        self.team_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,5), pady=5)

        # Scrollbar para la colección
        team_scrollbar = tk.Scrollbar(collection_frame, command=self.team_box.yview)
        team_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.team_box.configure(yscrollcommand=team_scrollbar.set)

        # Botón para eliminar Pokémon de la colección
        remove_button = tk.Button(collection_frame, text="Eliminar Pokémon", command=self.remove_pokemon, width=15)
        remove_button.pack(side=tk.LEFT, padx=5, pady=5)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            initialdir=self.images_path,
            title="Seleccione una imagen",
            filetypes=(("Imagenes", "*.png;*.jpg;*.jpeg"), ("Todos los archivos", "*.*"))
        )
        if file_path:
            try:
                img_processed = self.preprocessor.preprocess(file_path)
                features = self.extractor.extract_features(img_processed)
                predicted_pokedex = self.classifier.predict(features)

                # Calcular peligrosidad borrosa
                poke_data = self.df_pokemon[self.df_pokemon['pokedex_number'] == predicted_pokedex].iloc[0]
                attack_val = poke_data['attack']
                defense_val = poke_data['defense']
                speed_val = poke_data['speed']
                hp_val = poke_data['hp']
                danger_score = self.danger_evaluator.evaluate(attack_val, defense_val)

                description = self.desc_generator.generate_description(predicted_pokedex, danger_score)
                self.info_text.delete('1.0', tk.END)
                self.info_text.insert(tk.END, description)

                # Recomendaciones
                recs = self.extras_manager.get_recommendations(predicted_pokedex)
                self.recommendations_box.delete(0, tk.END)
                for r in recs:
                    self.recommendations_box.insert(tk.END, r)

                # Noticias
                news = self.extras_manager.get_news()
                self.news_box.delete(0, tk.END)
                for n in news:
                    self.news_box.insert(tk.END, n)

                # Guardar pokedex_number actual para VR y Mapa
                self.current_pokedex = predicted_pokedex

                # Añadir el Pokémon a la colección
                pokemon_entry = f"{poke_data['name']} (N.° {predicted_pokedex})"
                self.team_box.insert(tk.END, pokemon_entry)
                self.team.append(predicted_pokedex)

            except Exception as e:
                messagebox.showerror("Error", str(e))

    def remove_pokemon(self):
        selected_indices = self.team_box.curselection()
        if not selected_indices:
            messagebox.showwarning("Atención", "Por favor, selecciona al menos un Pokémon para eliminar.")
            return

        for index in reversed(selected_indices):
            self.team_box.delete(index)
            del self.team[index]

    def ask_question(self):
        question = self.question_entry.get()
        if question.strip():
            answer = self.knowledge_manager.answer_question(question)
            messagebox.showinfo("Respuesta", answer)
        else:
            messagebox.showwarning("Atención", "Por favor, introduce una pregunta.")

    def place_in_vr(self):
        if hasattr(self, 'current_pokedex'):
            result = self.vr_integration.place_pokemon_in_virtual_world(self.current_pokedex)
            messagebox.showinfo("Entorno Virtual", result)
        else:
            messagebox.showwarning("Atención", "Primero debes reconocer un Pokémon.")

    def view_habitat_map(self):
        if hasattr(self, 'current_pokedex'):
            try:
                # Obtener la ruta del archivo HTML del mapa
                map_file = self.extras_manager.get_habitat_map(self.current_pokedex)

                # Abrir el mapa en el navegador predeterminado
                webbrowser.open(f'file:///{map_file}')

            except Exception as e:
                messagebox.showerror("Error al generar el mapa", str(e))
        else:
            messagebox.showwarning("Atención", "Primero debes reconocer un Pokémon.")

    def simulate_battle(self):
        selected_indices = self.team_box.curselection()
        if len(selected_indices) != 2:
            messagebox.showwarning("Atención", "Por favor, selecciona exactamente dos Pokémon para la batalla.")
            return

        pokedex1 = self.team[selected_indices[0]]
        pokedex2 = self.team[selected_indices[1]]

        # Obtener los datos de ambos Pokémon
        poke1_data = self.pokemon_data[self.pokemon_data['pokedex_number'] == pokedex1].iloc[0]
        poke2_data = self.pokemon_data[self.pokemon_data['pokedex_number'] == pokedex2].iloc[0]

        # Crear diccionarios con las estadísticas necesarias
        pokemon1 = {
            'name': poke1_data['name'],
            'hp': poke1_data['hp'],
            'attack': poke1_data['attack'],
            'defense': poke1_data['defense'],
            'speed': poke1_data['speed']
        }

        pokemon2 = {
            'name': poke2_data['name'],
            'hp': poke2_data['hp'],
            'attack': poke2_data['attack'],
            'defense': poke2_data['defense'],
            'speed': poke2_data['speed']
        }

        # Simular la batalla
        result = self.battle_simulator.simulate_battle(pokemon1, pokemon2)

        # Mostrar el resultado en una ventana emergente
        battle_window = tk.Toplevel(self.master)
        battle_window.title("Resultado de la Batalla")
        battle_window.geometry("600x400")

        result_label = tk.Label(battle_window, text=f"¡{result['winner']} ha ganado la batalla!", font=("Arial", 16, "bold"))
        result_label.pack(pady=10)

        battle_log_text = tk.Text(battle_window, wrap=tk.WORD, height=20, width=70)
        battle_log_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        battle_log_text.insert(tk.END, result['log'])
        battle_log_text.configure(state='disabled')  # Hacer el texto de solo lectura

        # Botón para cerrar la ventana de batalla
        close_button = tk.Button(battle_window, text="Cerrar", command=battle_window.destroy, width=10)
        close_button.pack(pady=10)
