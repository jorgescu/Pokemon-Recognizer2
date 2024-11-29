# src/segmentacion.py

import cv2
import numpy as np
from src.preprocesamiento import convertir_a_grises


def segmentar_imagen(imagen):
    """Segmenta el Pokémon de la imagen utilizando detección de contornos."""
    # Convertir a escala de grises y aplicar desenfoque
    imagen_gris = convertir_a_grises(imagen)
    imagen_blur = cv2.GaussianBlur(imagen_gris, (5, 5), 0)

    # Aplicar umbralización
    _, umbral = cv2.threshold(imagen_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Encontrar contornos
    contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Seleccionar el contorno más grande (asumiendo que es el Pokémon)
    if contornos:
        contorno_max = max(contornos, key=cv2.contourArea)
        # Crear máscara
        mascara = np.zeros_like(imagen_gris)
        cv2.drawContours(mascara, [contorno_max], -1, 255, -1)
        # Aplicar máscara a la imagen original
        imagen_segmentada = cv2.bitwise_and(imagen, imagen, mask=mascara)
        return imagen_segmentada
    else:
        # Si no se encuentran contornos, devolver la imagen original
        return imagen

# Puedes agregar más métodos de segmentación si es necesario
