# data/descargar_datasets.py

import kagglehub
import os
import zipfile


def descargar_dataset_imagenes():
    # Descargar el dataset de imágenes
    path_imagenes = kagglehub.dataset_download("kvpratama/pokemon-images-dataset")
    print("Dataset de imágenes descargado en:", path_imagenes)

    # Extraer las imágenes si es necesario
    for file in os.listdir(path_imagenes):
        if file.endswith('.zip'):
            with zipfile.ZipFile(os.path.join(path_imagenes, file), 'r') as zip_ref:
                zip_ref.extractall('data/images/')
            print(f"Extraído {file} a data/images/")


def descargar_dataset_csv():
    # Descargar el dataset CSV
    path_csv = kagglehub.dataset_download("rounakbanik/pokemon")
    print("Dataset CSV descargado en:", path_csv)

    # Extraer el CSV si está comprimido
    for file in os.listdir(path_csv):
        if file.endswith('.zip'):
            with zipfile.ZipFile(os.path.join(path_csv, file), 'r') as zip_ref:
                zip_ref.extractall('data/csv/')
            print(f"Extraído {file} a data/csv/")


if __name__ == "__main__":
    descargar_dataset_imagenes()
    descargar_dataset_csv()
