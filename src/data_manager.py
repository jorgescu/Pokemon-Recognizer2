import pandas as pd


class DataManager:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def load_data(self):
        """
        Carga el DataFrame con información de Pokémon.
        Representación del conocimiento: aquí pasamos de datos brutos (CSV) a información estructurada (DataFrame).
        """
        df = pd.read_csv(self.csv_path)
        return df
