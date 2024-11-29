# src/entrenamiento.py (modificado)

import os
import cv2
import numpy as np
import joblib
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from preprocesamiento import preprocesar_imagen
from caracteristicas import extraer_caracteristicas
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm
from procesar_datos import cargar_datos_pokemon, preparar_datos

def cargar_imagenes_y_etiquetas(ruta_imagenes, diccionario_mapeo):
    """Carga las imágenes y sus etiquetas utilizando el diccionario de mapeo."""
    imagenes = []
    etiquetas = []
    for archivo in os.listdir(ruta_imagenes):
        if archivo.endswith(('.png', '.jpg', '.jpeg')):
            # Obtener el número de Pokédex del nombre del archivo
            numero_pokedex = os.path.splitext(archivo)[0]
            try:
                numero_pokedex = int(numero_pokedex)
                # Obtener el nombre del Pokémon usando el diccionario de mapeo
                nombre_pokemon = diccionario_mapeo.get(numero_pokedex)
                if nombre_pokemon:
                    ruta_imagen = os.path.join(ruta_imagenes, archivo)
                    imagenes.append(ruta_imagen)
                    etiquetas.append(nombre_pokemon)
                else:
                    print(f"El número de Pokédex {numero_pokedex} no se encontró en el diccionario de mapeo.")
            except ValueError:
                print(f"Nombre de archivo inválido: {archivo}")
    return imagenes, etiquetas


def preparar_datos(imagenes, etiquetas):
    """Preprocesa las imágenes y extrae características."""
    X = []
    for imagen_ruta in tqdm(imagenes, desc="Procesando imágenes"):
        imagen = preprocesar_imagen(imagen_ruta)
        # Asegurarse de que la imagen tenga 3 canales
        if len(imagen.shape) == 2:
            imagen = cv2.cvtColor(imagen, cv2.COLOR_GRAY2BGR)
        caracteristicas = extraer_caracteristicas(imagen)
        X.append(caracteristicas)
    X = np.array(X)
    return X, etiquetas

def entrenar_modelo_svm(X_train, y_train, X_test, y_test):
    """Entrena el modelo SVM y evalúa su rendimiento."""
    # Opcional: Optimizar los hiperparámetros usando algoritmos genéticos
    # C, gamma = optimizar_modelo(X_train, y_train)
    # Para simplificar, usaremos valores predeterminados
    modelo = SVC(kernel='rbf', C=1.0, gamma='scale', probability=True)
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Precisión del modelo: {accuracy * 100:.2f}%")
    return modelo

def guardar_modelo(modelo, ruta):
    """Guarda el modelo entrenado en la ruta especificada."""
    joblib.dump(modelo, ruta)
    print(f"Modelo guardado en: {ruta}")

if __name__ == "__main__":
    # Ruta donde están las imágenes organizadas por carpetas según su clase
    ruta_imagenes = 'data/images/pokemon-images/'
    # Asegúrate de que las imágenes están organizadas en subcarpetas por nombre de Pokémon
    imagenes, etiquetas = cargar_imagenes_y_etiquetas(ruta_imagenes)

    # Preprocesar imágenes y extraer características
    X, y = preparar_datos(imagenes, etiquetas)

    # Codificar las etiquetas
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    # Guardar el LabelEncoder para decodificar etiquetas en el futuro
    joblib.dump(le, 'data/models/label_encoder.pkl')

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)

    # Entrenar el modelo SVM
    modelo = entrenar_modelo_svm(X_train, y_train, X_test, y_test)

    # Guardar el modelo entrenado
    ruta_modelo = 'data/models/modelo_svm.pkl'
    guardar_modelo(modelo, ruta_modelo)

# src/entrenamiento.py (continuación)

if __name__ == "__main__":
    # Cargar y preparar los datos del CSV
    df_pokemon = cargar_datos_pokemon()
    df_pokemon, diccionario_mapeo = preparar_datos(df_pokemon)

    # Ruta donde están las imágenes nombradas por número de Pokédex
    ruta_imagenes = 'data/images/pokemon-images/'

    # Cargar las imágenes y sus etiquetas
    imagenes, etiquetas = cargar_imagenes_y_etiquetas(ruta_imagenes, diccionario_mapeo)

    # Verificar que se hayan cargado imágenes
    if not imagenes:
        print("No se encontraron imágenes para entrenar.")
        exit()

    # Preprocesar imágenes y extraer características
    X, y = preparar_datos(imagenes, etiquetas)

    # Codificar las etiquetas
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    # Guardar el LabelEncoder para decodificar etiquetas en el futuro
    joblib.dump(le, 'data/models/label_encoder.pkl')

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)

    # Entrenar el modelo SVM
    modelo = entrenar_modelo_svm(X_train, y_train, X_test, y_test)

    # Guardar el modelo entrenado
    ruta_modelo = 'data/models/modelo_svm.pkl'
    guardar_modelo(modelo, ruta_modelo)
