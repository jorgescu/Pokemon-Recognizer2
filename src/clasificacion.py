# src/clasificacion.py

from sklearn.svm import SVC
import pickle

def entrenar_modelo(X_train, y_train, C=1.0, gamma='scale'):
    """Entrena un modelo SVM con los datos proporcionados."""
    modelo = SVC(C=C, gamma=gamma, kernel='rbf')
    modelo.fit(X_train, y_train)
    return modelo

def guardar_modelo(modelo, ruta_modelo):
    """Guarda el modelo entrenado en disco."""
    with open(ruta_modelo, 'wb') as archivo:
        pickle.dump(modelo, archivo)

def cargar_modelo(ruta_modelo):
    """Carga un modelo entrenado desde disco."""
    with open(ruta_modelo, 'rb') as archivo:
        modelo = pickle.load(archivo)
    return modelo
