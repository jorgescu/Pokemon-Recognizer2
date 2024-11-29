# src/descripciones.py

import random
import pandas as pd

def generar_descripcion(datos_pokemon):
    """Genera una descripción detallada y creativa del Pokémon."""
    nombre = datos_pokemon['name']
    tipo1 = datos_pokemon['type1']
    tipo2 = datos_pokemon['type2'] if pd.notna(datos_pokemon['type2']) else ''
    tipos = f"{tipo1}" + (f" y {tipo2}" if tipo2 else '')
    clasificacion = datos_pokemon['classification']
    habilidades = ', '.join(datos_pokemon['abilities'])
    zona = datos_pokemon['zona_de_recreo']
    rareza = datos_pokemon['rareza']
    peligrosidad = datos_pokemon['peligrosidad']
    altura = datos_pokemon['height_m']
    peso = datos_pokemon['weight_kg']
    genero = datos_pokemon['percentage_male']

    # Frases creativas
    descripciones = [
        f"¡Te has encontrado con {nombre}, un Pokémon de tipo {tipos}!",
        f"{nombre} es conocido como {clasificacion.lower()} y habita en la región de {zona}.",
        f"Con habilidades como {habilidades}, {nombre} es un Pokémon de rareza {rareza}.",
        f"Tiene una altura de {altura} metros y un peso de {peso} kg.",
        f"Su peligrosidad es considerada {peligrosidad}, ¡ten cuidado!",
        f"El porcentaje de machos en esta especie es {genero}%.",
    ]

    # Añadir datos curiosos o historias (puedes expandir esta sección)
    datos_curiosos = [
        f"Se dice que {nombre} aparece en noches de luna llena.",
        f"Es un Pokémon que suele acompañar a entrenadores valientes.",
        f"En antiguos escritos, {nombre} es mencionado como un guardián de los bosques.",
    ]

    descripcion_completa = '\n'.join(descripciones + [random.choice(datos_curiosos)])
    return descripcion_completa

# Puedes añadir funciones para generar descripciones en diferentes idiomas o estilos
