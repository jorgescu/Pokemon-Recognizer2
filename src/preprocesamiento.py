# src/preprocesamiento.py

import cv2
import numpy as np

def aplicar_filtro_mediana(imagen, ksize=5):
    """Aplica un filtro de mediana para reducir el ruido."""
    return cv2.medianBlur(imagen, ksize)

def convertir_a_grises(imagen):
    """Convierte una imagen BGR a escala de grises."""
    return cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

def normalizar_imagen(imagen):
    """Normaliza la imagen para que los valores estén entre 0 y 1."""
    return imagen / 255.0

def redimensionar_imagen(imagen, dimensiones=(256, 256)):
    """Redimensiona la imagen a las dimensiones especificadas."""
    return cv2.resize(imagen, dimensiones, interpolation=cv2.INTER_AREA)

def equalizar_histograma(imagen):
    """Equaliza el histograma para mejorar el contraste."""
    if len(imagen.shape) == 2:
        return cv2.equalizeHist(imagen)
    else:
        imagen_yuv = cv2.cvtColor(imagen, cv2.COLOR_BGR2YUV)
        imagen_yuv[:, 0] = cv2.equalizeHist(imagen_yuv[:, 0])
        return cv2.cvtColor(imagen_yuv, cv2.COLOR_YUV2BGR)

def correccion_iluminacion(imagen):
    """Corrige la iluminación de la imagen."""
    imagen_lab = cv2.cvtColor(imagen, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(imagen_lab)
    l_eq = cv2.equalizeHist(l)
    imagen_lab_eq = cv2.merge((l_eq, a, b))
    imagen_corregida = cv2.cvtColor(imagen_lab_eq, cv2.COLOR_LAB2BGR)
    return imagen_corregida

def eliminar_fondo(imagen):
    """Elimina el fondo utilizando segmentación por color o umbralización."""
    imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    mascara = cv2.inRange(imagen_hsv, (0, 0, 0), (180, 255, 255))
    imagen_sin_fondo = cv2.bitwise_and(imagen, imagen, mask=mascara)
    return imagen_sin_fondo

def preprocesar_imagen(imagen_ruta):
    """Aplica todos los pasos de preprocesamiento a una imagen."""
    imagen = cv2.imread(imagen_ruta)
    imagen = redimensionar_imagen(imagen)
    imagen = aplicar_filtro_mediana(imagen)
    imagen = correccion_iluminacion(imagen)
    imagen = eliminar_fondo(imagen)
    imagen = convertir_a_grises(imagen)
    imagen = equalizar_histograma(imagen)
    imagen = normalizar_imagen(imagen)
    return imagen

# Añade más funciones si es necesario
