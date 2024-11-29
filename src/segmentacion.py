# src/segmentacion.py

import cv2
import numpy as np

def umbralizacion_otsu(imagen):
    """Aplica umbralización de Otsu para segmentar la imagen."""
    _, imagen_otsu = cv2.threshold(imagen, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return imagen_otsu

def deteccion_bordes_canny(imagen, umbral1=100, umbral2=200):
    """Detecta bordes utilizando el método de Canny."""
    return cv2.Canny(imagen, umbral1, umbral2)

# Añade más funciones según sea necesario
