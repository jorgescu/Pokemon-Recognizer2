# src/caracteristicas.py

import cv2
import numpy as np
from skimage.feature import hog


def extraer_caracteristicas(imagen):
    """Extrae características combinadas de la imagen para clasificación."""
    # Convertir a escala de grises
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Extraer características HOG
    caracteristicas_hog = extraer_hog(imagen_gris)

    # Calcular momentos de Hu
    momentos_hu = calcular_momentos_hu(imagen_gris)

    # Calcular histogramas de color
    hist_color = calcular_histogramas_color(imagen)

    # Concatenar todas las características
    caracteristicas = np.concatenate([caracteristicas_hog, momentos_hu, hist_color])

    return caracteristicas


def extraer_hog(imagen_gris):
    """Extrae características HOG de la imagen en escala de grises."""
    hog_features, hog_image = hog(
        imagen_gris,
        orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        block_norm='L2-Hys',
        visualize=True
    )
    return hog_features


def calcular_momentos_hu(imagen_gris):
    """Calcula los Momentos de Hu de la imagen en escala de grises."""
    momentos = cv2.moments(imagen_gris)
    momentos_hu = cv2.HuMoments(momentos).flatten()
    # Aplicar logaritmo para escalar los valores
    momentos_hu = -np.sign(momentos_hu) * np.log10(np.abs(momentos_hu) + 1e-10)
    return momentos_hu


def calcular_histogramas_color(imagen):
    """Calcula los histogramas de color de la imagen en BGR."""
    hist_b = cv2.calcHist([imagen], [0], None, [256], [0, 256])
    hist_g = cv2.calcHist([imagen], [1], None, [256], [0, 256])
    hist_r = cv2.calcHist([imagen], [2], None, [256], [0, 256])
    hist_color = np.concatenate([hist_b, hist_g, hist_r]).flatten()
    # Normalizar el histograma
    hist_color = hist_color / np.sum(hist_color)
    return hist_color

# Puedes agregar más funciones de extracción de características si lo consideras necesario
