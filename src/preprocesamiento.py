# src/preprocesamiento.py

import cv2
import numpy as np

def aplicar_filtro_mediana(imagen, ksize=5):
    """Aplica un filtro de mediana para reducir el ruido."""
    return cv2.medianBlur(imagen, ksize)

def convertir_a_grises(imagen):
    """Convierte una imagen RGB a escala de grises."""
    return cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)

# Añade más funciones según sea necesario
