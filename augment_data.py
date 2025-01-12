# augment_data.py

import os
import cv2
import numpy as np

def augment_image(img):
    """
    Aplica varias transformaciones para crear versiones distintas:
    - Giro 90°, 180°, 270°
    - Espejo horizontal
    - Espejo vertical
    - (Opcional: añadir ruido, cambio de brillo, etc.)
    Retorna una lista de imágenes transformadas (arrays).
    """
    augmented = []

    # Original (la primera la puedes omitir si no quieres duplicar sin cambio)
    # augmented.append(img)

    # Giro 90
    rot90 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    augmented.append(rot90)

    # Giro 180
    rot180 = cv2.rotate(img, cv2.ROTATE_180)
    augmented.append(rot180)

    # Giro 270
    rot270 = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    augmented.append(rot270)

    # Flip horizontal
    flip_h = cv2.flip(img, 1)  # 1: flip horizontal
    augmented.append(flip_h)

    # Flip vertical
    flip_v = cv2.flip(img, 0)  # 0: flip vertical
    augmented.append(flip_v)

    # (Opcional) Agregar otras transformaciones:
    # - Ruido aleatorio, cambio de brillo, etc.

    return augmented

def main():
    # Carpeta de imágenes originales
    original_folder = os.path.join("data", "images", "pokemon-images")
    # Carpeta de destino para imágenes aumentadas
    augmented_folder = os.path.join("data", "images", "pokemon-images-augmented")

    os.makedirs(augmented_folder, exist_ok=True)

    valid_extensions = (".png", ".jpg", ".jpeg")

    # Recorremos todos los archivos
    for file_name in os.listdir(original_folder):
        file_lower = file_name.lower()
        if file_lower.endswith(valid_extensions):
            file_path = os.path.join(original_folder, file_name)
            # Leer imagen con OpenCV
            img = cv2.imread(file_path)
            if img is None:
                print(f"No se pudo leer {file_name}. Ignorando.")
                continue

            # Generar versiones aumentadas
            aug_imgs = augment_image(img)

            # Guardar la imagen original en la carpeta nueva (opcional)
            # para que también quede copiada allí:
            # cv2.imwrite(os.path.join(augmented_folder, file_name), img)

            # Guardar versiones aumentadas
            base_name, ext = os.path.splitext(file_name)
            for idx, aug_img in enumerate(aug_imgs, start=1):
                new_name = f"{base_name}_aug{idx}{ext}"
                save_path = os.path.join(augmented_folder, new_name)
                cv2.imwrite(save_path, aug_img)
                print(f"Guardada: {new_name}")

if __name__ == "__main__":
    main()
