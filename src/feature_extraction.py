import numpy as np
from skimage.feature import hog
from skimage.color import rgb2gray


class FeatureExtractor:
    def __init__(self):
        pass

    def extract_features(self, img):
        """
        Extracción de características (Reconocimiento de Patrones).
        Se extraen características HOG + histograma de color.
        """
        # Convertir a gris
        gray = rgb2gray(img)

        # HOG en imagen 2D (gray)
        hog_features, _ = hog(
            gray,
            orientations=8,
            pixels_per_cell=(16, 16),
            cells_per_block=(1, 1),
            visualize=True
            # Se elimina channel_axis porque gray ya es 2D
        )

        # Histogramas de color en la imagen original (3D)
        hist_r, _ = np.histogram(img[:, :, 0], bins=16, range=(0, 1))
        hist_g, _ = np.histogram(img[:, :, 1], bins=16, range=(0, 1))
        hist_b, _ = np.histogram(img[:, :, 2], bins=16, range=(0, 1))

        # Concatenar las características
        features = np.concatenate([hog_features, hist_r, hist_g, hist_b])
        return features
