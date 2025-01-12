# src/preprocessor.py

import pandas as pd


class Preprocessor:
    def __init__(self, csv_path='data/pokemon.csv'):
        """
        Inicializa el preprocesador con la ruta al archivo CSV de Pokémon.

        Args:
            csv_path (str): Ruta al archivo CSV que contiene los datos de Pokémon.
        """
        self.csv_path = csv_path

    def load_pokemon_data(self):
        """
        Carga los datos de Pokémon desde el archivo CSV.

        Returns:
            pd.DataFrame: DataFrame con los datos de Pokémon.
        """
        try:
            df = pd.read_csv(self.csv_path)
            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo CSV en la ruta: {self.csv_path}")
        except pd.errors.EmptyDataError:
            raise ValueError("El archivo CSV está vacío.")
        except Exception as e:
            raise Exception(f"Error al cargar el archivo CSV: {e}")
