# src/logica_borrosa.py

import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np

def crear_sistema_borroso():
    """Crea y devuelve un sistema de lógica borrosa."""
    # Definir variables y reglas difusas
    # ...
    return sistema_simulacion

def inferir_peligrosidad(sistema_simulacion, tipo_valor):
    """Utiliza el sistema borroso para inferir la peligrosidad."""
    sistema_simulacion.input['tipo_pokemon'] = tipo_valor
    sistema_simulacion.compute()
    return sistema_simulacion.output['peligrosidad']
