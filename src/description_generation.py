import numpy as np
import pandas as pd


class DescriptionGenerator:
    def __init__(self, df):
        self.df = df

    def generate_description(self, pokedex_number, danger_score):
        """
        Genera una descripción detallada del Pokémon. (Representación del conocimiento a partir de datos).
        """
        poke_data = self.df[self.df['pokedex_number'] == pokedex_number].iloc[0]

        name = poke_data['name']
        ptype1 = poke_data['type1']
        ptype2 = poke_data['type2'] if not pd.isna(poke_data['type2']) else None
        classification = poke_data['classfication']
        attack = poke_data['attack']
        defense = poke_data['defense']
        sp_attack = poke_data['sp_attack']
        sp_defense = poke_data['sp_defense']
        speed = poke_data['speed']

        base_total = poke_data['base_total']
        if base_total < 400:
            rarity = "común"
        elif base_total < 500:
            rarity = "poco común"
        else:
            rarity = "raro"

        if danger_score < 30:
            danger_level = "baja"
        elif danger_score < 60:
            danger_level = "moderada"
        else:
            danger_level = "alta"

        # Simular evoluciones: asume línea evolutiva ordenada por número de pokédex
        evolution_line = self.df[
            self.df['japanese_name'].str.contains(poke_data['japanese_name'].split('フ')[0], na=False)]
        evolution_numbers = evolution_line['pokedex_number'].tolist()
        evolution_numbers.sort()
        current_index = evolution_numbers.index(pokedex_number)
        next_evo = None
        if current_index < len(evolution_numbers) - 1:
            next_evo = self.df[self.df['pokedex_number'] == evolution_numbers[current_index + 1]].iloc[0]['name']
        evo_text = f"Evoluciona a {next_evo}" if next_evo else "No tiene evoluciones posteriores."

        ttext = ptype1 if ptype2 is None else f"{ptype1} / {ptype2}"

        description = (
            f"¡Has identificado a {name} (N.° {pokedex_number})!\n"
            f"Tipo: {ttext}\n"
            f"Clasificación: {classification}\n"
            f"Nivel de rareza: {rarity}\n"
            f"Evolución: {evo_text}\n"
            f"Nivel de peligrosidad (Lógica Borrosa): {danger_level}\n"
            f"Estadísticas:\n"
            f" - Ataque: {attack}\n"
            f" - Defensa: {defense}\n"
            f" - Ataque Especial: {sp_attack}\n"
            f" - Defensa Especial: {sp_defense}\n"
            f" - Velocidad: {speed}\n"
        )
        return description
