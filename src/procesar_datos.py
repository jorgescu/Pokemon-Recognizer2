# src/procesar_datos.py (actualizado)

import pandas as pd

def cargar_datos_pokemon():
    # Cargar el CSV de Pokémon
    df = pd.read_csv('data/csv/pokemon.csv')
    return df

def preparar_datos(df):
    # Procesar los datos según sea necesario
    df['abilities'] = df['abilities'].apply(eval)
    df['percentage_male'] = df['percentage_male'].fillna('Genderless')
    df['zona_de_recreo'] = df['generation'].apply(asignar_zona_de_recreo)
    # Crear diccionario de mapeo de pokedex_number a name
    df_mapeo = df[['pokedex_number', 'name']].drop_duplicates()
    diccionario_mapeo = dict(zip(df_mapeo['pokedex_number'], df_mapeo['name']))
    return df, diccionario_mapeo

def asignar_zona_de_recreo(generacion):
    zonas = {
        1: 'Kanto',
        2: 'Johto',
        3: 'Hoenn',
        4: 'Sinnoh',
        5: 'Unova',
        6: 'Kalos',
        7: 'Alola',
        8: 'Galar',
    }
    return zonas.get(generacion, 'Desconocido')
