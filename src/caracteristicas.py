# src/caracteristicas.py

import cv2
import numpy as np

def extraer_momentos_hu(imagen):
    """Extrae los momentos de Hu de una imagen binaria."""
    momentos = cv2.moments(imagen)
    hu_moments = cv2.HuMoments(momentos).flatten()
    return hu_moments

def extraer_caracteristicas_forma(imagen):
    """Extrae características de forma de la imagen."""
    contornos, _ = cv2.findContours(imagen, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contornos:
        contorno = max(contornos, key=cv2.contourArea)
        area = cv2.contourArea(contorno)
        perimetro = cv2.arcLength(contorno, True)
        return [area, perimetro]
    else:
        return [0, 0]

# Añade más funciones según sea necesario
