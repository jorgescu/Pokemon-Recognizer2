# src/clasificacion.py (verificar que está correcto)

import os
import cv2
import numpy as np
import joblib
from src.caracteristicas import extraer_caracteristicas
from src.procesar_datos import cargar_datos_pokemon, preparar_datos
from src.logica_borrosa import crear_sistema_logico, calcular_peligrosidad
from src.descripciones import generar_descripcion

# Cargar el modelo entrenado
modelo = joblib.load('data/models/modelo_svm.pkl')

# Cargar el LabelEncoder
le = joblib.load('data/models/label_encoder.pkl')

# Cargar y preparar los datos
df_pokemon = cargar_datos_pokemon()
df_pokemon, _ = preparar_datos(df_pokemon)

# Crear el sistema difuso una vez
simulador_difuso = crear_sistema_logico()


def predecir_pokemon(imagen):
    """Predice el Pokémon en la imagen y genera una descripción."""
    # Extraer características
    caracteristicas = extraer_caracteristicas(imagen)
    caracteristicas = np.array(caracteristicas).reshape(1, -1)

    # Predecir el índice del Pokémon
    prediccion = modelo.predict(caracteristicas)[0]
    # Decodificar el nombre del Pokémon
    nombre_predicho = le.inverse_transform([prediccion])[0]

    # Obtener los datos del Pokémon
    datos_pokemon = df_pokemon[df_pokemon['name'] == nombre_predicho].iloc[0]

    # Calcular peligrosidad
    datos_pokemon['peligrosidad'] = calcular_peligrosidad(datos_pokemon, simulador_difuso)

    # Generar descripción
    descripcion = generar_descripcion(datos_pokemon)

    return nombre_predicho, descripcion
