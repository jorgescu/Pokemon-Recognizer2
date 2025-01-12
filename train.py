# train.py

"""
Script para entrenar un modelo SVM que reconozca Pokémon a partir de imágenes.
1) Reescribe las imágenes en disco sin perfiles ICC usando Pillow.
2) Luego, construye el dataset usando OpenCV y scikit-image.
3) Entrena y guarda un modelo SVM.
"""

import os
import pickle
import numpy as np
import pandas as pd
import cv2
import warnings
import re  # Importación añadida para manejar expresiones regulares

from PIL import Image

from skimage.color import rgb2gray
from skimage.feature import hog
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from collections import Counter


def remove_icc_profiles_in_place(images_path):
    """
    Recorre 'images_path' y para cada .png/.jpg, lo reescribe en disco
    sin perfiles ICC usando Pillow. Así se evitan los libpng warnings.
    """
    valid_extensions = (".png", ".jpg", ".jpeg")
    image_files = os.listdir(images_path)

    print(f"Eliminando perfiles ICC directamente en disco dentro de {images_path}...")
    for file_name in image_files:
        if file_name.lower().endswith(valid_extensions):
            file_path = os.path.join(images_path, file_name)
            try:
                with Image.open(file_path) as pil_img:
                    # Convertir a RGB para eliminar perfiles y metadatos
                    pil_img = pil_img.convert("RGB")

                    # Sobrescribir el archivo sin perfiles ICC
                    pil_img.save(file_path, optimize=True, icc_profile=None)
            except Exception as e:
                print(f"No se pudo limpiar {file_name}: {e}")


def remove_icc_profiles_with_opencv(images_path):
    """
    Alternativa: Reescribe las imágenes usando OpenCV para eliminar perfiles ICC.
    """
    valid_extensions = (".png", ".jpg", ".jpeg")
    image_files = os.listdir(images_path)

    print(f"Eliminando perfiles ICC directamente en disco dentro de {images_path} usando OpenCV...")
    for file_name in image_files:
        if file_name.lower().endswith(valid_extensions):
            file_path = os.path.join(images_path, file_name)
            try:
                img = cv2.imread(file_path)
                if img is not None:
                    # Para PNG, puedes especificar la compresión si lo deseas
                    if file_name.lower().endswith(".png"):
                        cv2.imwrite(file_path, img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
                    else:
                        cv2.imwrite(file_path, img)
            except Exception as e:
                print(f"No se pudo limpiar {file_name}: {e}")


def check_icc_profile(image_path):
    """
    Verifica si una imagen contiene un perfil ICC.
    """
    with Image.open(image_path) as img:
        icc = img.info.get('icc_profile')
        if icc:
            print(f"{image_path} contiene un perfil ICC.")
            return True
        else:
            print(f"{image_path} no contiene un perfil ICC.")
            return False


def load_pokemon_csv(csv_path):
    """
    Carga el CSV con información de Pokémon.
    Retorna un DataFrame de pandas.
    """
    df = pd.read_csv(csv_path)
    return df


def preprocess_image(img, size=(128, 128)):
    """
    Preprocesa la imagen:
      1. Redimensiona a 'size'.
      2. Convierte de BGR a RGB.
      3. Normaliza a rango [0,1].
    Retorna la imagen procesada (numpy array).
    """
    img_resized = cv2.resize(img, size)
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    img_norm = img_rgb / 255.0
    return img_norm


def extract_features(img):
    """
    Extrae características de la imagen:
      - HOG (skimage, sobre escala de grises)
      - Histograma de color (simple en 3 canales)
    Retorna un vector con las características concatenadas.
    """
    # Convertir a gris
    gray = rgb2gray(img)

    # HOG features
    hog_features = hog(
        gray,
        orientations=8,
        pixels_per_cell=(16, 16),
        cells_per_block=(1, 1),
        visualize=False
    )

    # Histograma de color (3 canales)
    hist_r, _ = np.histogram(img[:, :, 0], bins=16, range=(0, 1))
    hist_g, _ = np.histogram(img[:, :, 1], bins=16, range=(0, 1))
    hist_b, _ = np.histogram(img[:, :, 2], bins=16, range=(0, 1))

    # Concatenar
    features = np.concatenate([hog_features, hist_r, hist_g, hist_b])
    return features


def extract_pokedex_num(file_name):
    """
    Extrae el número de Pokédex del nombre del archivo.
    Permite nombres como '001.png', '001_1.png', '001a.png', etc.
    Retorna el número como entero o None si no se puede extraer.
    """
    match = re.match(r'^(\d+)', file_name)
    if match:
        return int(match.group(1))
    else:
        return None


def build_dataset(images_path, df_pokemon):
    """
    Recorre el directorio 'images_path', para cada imagen .png/.jpg:
      - Extrae el pokedex_number del nombre de archivo.
      - Verifica si está en df_pokemon (opcional).
      - Lee con OpenCV.
      - Preprocesa y extrae características.
    Retorna X (lista de vectores) y y (lista de pokedex_number).
    """
    X = []
    y = []

    valid_extensions = (".png", ".jpg", ".jpeg")
    image_files = os.listdir(images_path)

    for file_name in image_files:
        if file_name.lower().endswith(valid_extensions):
            pokedex_num = extract_pokedex_num(file_name)
            if pokedex_num is None:
                print(f"Archivo {file_name} no se reconoce como pokedex_number válido.")
                continue

            # (Opcional) Verificar si existe en CSV
            if pokedex_num not in df_pokemon["pokedex_number"].values:
                print(f"Advertencia: El pokedex_number {pokedex_num} no está en pokemon.csv.")
                continue

            file_path = os.path.join(images_path, file_name)
            img_cv2 = cv2.imread(file_path)
            if img_cv2 is None:
                print(f"No se pudo leer la imagen {file_path}. Se ignora.")
                continue

            # Preprocesar
            img_preprocessed = preprocess_image(img_cv2)
            # Extraer features
            features = extract_features(img_preprocessed)

            X.append(features)
            y.append(pokedex_num)

    X = np.array(X)
    y = np.array(y)
    return X, y


def train_svm(X, y, test_size=0.2, random_state=42, c_val=1.0, gamma_val='scale'):
    """
    Entrena un clasificador SVM con los datos X, y.
    Hace un split train/test y retorna el modelo y su accuracy en test.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    model = SVC(C=c_val, gamma=gamma_val, probability=True)
    model.fit(X_train, y_train)
    test_acc = model.score(X_test, y_test)
    return model, test_acc


def cross_validation_score_func(X, y, model=None, cv=5):
    """
    Aplica cross-validation con K folds y retorna el accuracy promedio.
    """
    if model is None:
        model = SVC(probability=True)
    scores = cross_val_score(model, X, y, cv=cv)
    return scores.mean()


def print_class_distribution(y):
    """
    Imprime la distribución de clases en el conjunto de etiquetas y.
    """
    counter = Counter(y)
    print("\nDistribución de clases:")
    for cls, count in sorted(counter.items()):
        print(f"Clase {cls}: {count} muestras")
    return counter


def main():
    # Ajustar rutas a tu estructura
    csv_path = os.path.join("data", "csv", "pokemon.csv")
    images_path = os.path.join("data", "images", "pokemon-images-augmented")
    model_path = os.path.join("models", "svm_model.pkl")

    # 1) Eliminar perfiles ICC en disco (in-place) para todas las imágenes usando Pillow
    remove_icc_profiles_in_place(images_path)

    # Opcional: Si las advertencias persisten, utiliza la alternativa con OpenCV
    # remove_icc_profiles_with_opencv(images_path)

    # 1.1) Verificar que las imágenes no contienen perfiles ICC
    print("\nVerificando eliminación de perfiles ICC...")
    sample_images = os.listdir(images_path)[:5]  # Verificar las primeras 5 imágenes
    for file_name in sample_images:
        if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
            file_path = os.path.join(images_path, file_name)
            check_icc_profile(file_path)

    # 2) Cargar CSV
    print("\nCargando CSV de Pokémon...")
    df_pokemon = load_pokemon_csv(csv_path)

    # 3) Construir dataset
    print("\nConstruyendo dataset de imágenes...")
    X, y = build_dataset(images_path, df_pokemon)
    print(f"Total de muestras cargadas: {len(X)}")
    if len(X) == 0:
        print("No se encontraron imágenes válidas para entrenar.")
        return

    # 3.1) Imprimir distribución de clases
    class_counts = print_class_distribution(y)

    # 4) Determinar el número adecuado de folds para cross-validation
    min_samples_per_class = min(class_counts.values())
    desired_cv = 5
    if min_samples_per_class < desired_cv:
        if min_samples_per_class < 2:
            print(f"\nError: La clase con menos muestras tiene {min_samples_per_class} muestras. "
                  f"Es necesario tener al menos 2 muestras por clase para la validación cruzada.")
            print("Considera recolectar más imágenes por clase o eliminar clases con pocas muestras.")
            return
        else:
            cv_folds = min_samples_per_class
            print(f"\nAdvertencia: La clase con menos muestras tiene {min_samples_per_class} muestras. "
                  f"Reduciendo el número de folds de {desired_cv} a {cv_folds}.")
    else:
        cv_folds = desired_cv

    # 5) Cross-Validation sencilla para ver un accuracy de base
    print(f"\nEvaluando modelo base con Cross-Validation ({cv_folds} folds)...")
    base_cv_score = cross_validation_score_func(X, y, model=SVC(probability=True), cv=cv_folds)
    print(f"Accuracy promedio (SVC default) = {base_cv_score:.2f}")

    # 6) Entrenar con train/test split
    print("\nEntrenando modelo final SVM con train/test split...")
    model, test_acc = train_svm(X, y, test_size=0.2, random_state=42)
    print(f"Exactitud en test: {test_acc:.2f}")

    # 7) Guardar modelo entrenado
    print(f"\nGuardando modelo en {model_path} ...")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    print("\nEntrenamiento completado con éxito.")


if __name__ == "__main__":
    # Opcional: Suprimir advertencias específicas de libpng si persisten
    warnings.filterwarnings("ignore", message=".*libpng warning: iCCP: known incorrect sRGB profile.*")
    main()
