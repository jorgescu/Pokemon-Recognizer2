import os

# Ajusta aquí la lista de archivos a incluir.
# Cada elemento es una tupla: (ruta_relativa, descripción_opcional)
FILES_TO_INCLUDE = [
    ("main.py", "Script principal (punto de entrada)"),
    ("train.py", "Script de entrenamiento SVM"),
    ("augment_data.py", "Script de data augmentation (opcional)"),
    # ("clean_images.py", "Script para limpiar perfiles ICC (no usado finalmente)"),
    ("requirements.txt", "Lista de dependencias del proyecto"),
    ("src/classification.py", "Módulo con la clase PokemonClassifier (SVM)"),
    ("src/data_manager.py", "Carga del CSV de Pokémon"),
    ("src/feature_extraction.py", "Extracción de características (HOG, hist. color)"),
    ("src/fuzzy_logic.py", "Módulo de lógica borrosa para peligrosidad"),
    ("src/description_generation.py", "Genera descripción textual del Pokémon"),
    ("src/knowledge_manager.py", "Gestor de conocimiento/QA simple"),
    ("src/extras.py", "Funciones extra (recomendaciones, noticias...)"),
    ("src/virtual_environment.py", "Simulación de entorno virtual 3D"),
    ("src/gui.py", "Interfaz gráfica Tkinter"),
    ("src/image_processing.py", "Preprocesamiento de imágenes con OpenCV"),
    ("src/optimization.py", "Algoritmo genético (DEAP) para optimizar el SVM"),
]

def main():
    output_file = "all_code.txt"
    with open(output_file, "w", encoding="utf-8") as out:
        out.write("# Proyecto Reconocedor de Pokémon - Todos los archivos\n")
        out.write("# ---------------------------------------------------\n\n")

        for filepath, desc in FILES_TO_INCLUDE:
            # Si el archivo existe, se lee y se escribe en all_code.txt
            if os.path.exists(filepath):
                # Separador visual
                out.write(f"===== [Fichero] {filepath} ({desc}) =====\n\n")
                try:
                    with open(filepath, "r", encoding="utf-8") as infile:
                        code = infile.read()
                    out.write(code)
                except UnicodeDecodeError:
                    # Si hay algún archivo binario o con codificación distinta
                    out.write(f"# [AVISO] No se pudo leer correctamente el archivo: {filepath}\n")
                out.write("\n\n")  # Espacio entre archivos
            else:
                out.write(f"# [AVISO] No se encontró el archivo: {filepath}\n\n")
    print(f"Se ha creado el archivo '{output_file}' con todo el código concatenado.")


if __name__ == "__main__":
    main()

