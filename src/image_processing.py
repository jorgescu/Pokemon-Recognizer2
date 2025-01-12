# src/image_processing.py

import cv2
import numpy as np


class ImagePreprocessor:
    def __init__(self):
        pass

    def preprocess(self, image_path):
        """
        Preprocesamiento de la imagen (Percepción Computacional: Preproceso, Segmentación).

        Args:
            image_path (str): Ruta a la imagen a preprocesar.

        Returns:
            np.ndarray: Imagen preprocesada.
        """
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"No se encontró la imagen en {image_path}")

        # Cambio de tamaño a 128x128
        img = cv2.resize(img, (128, 128))
        # Normalización
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img / 255.0
        return img
