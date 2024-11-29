# src/logica_borrosa.py

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def crear_sistema_logico():
    """Crea y configura el sistema de lógica difusa."""
    # Definir variables difusas
    ataque = ctrl.Antecedent(np.arange(0, 201, 1), 'ataque')
    defensa = ctrl.Antecedent(np.arange(0, 201, 1), 'defensa')
    velocidad = ctrl.Antecedent(np.arange(0, 201, 1), 'velocidad')
    peligrosidad = ctrl.Consequent(np.arange(0, 101, 1), 'peligrosidad')

    # Definir funciones de membresía
    for variable in [ataque, defensa, velocidad]:
        variable['bajo'] = fuzz.trimf(variable.universe, [0, 0, 100])
        variable['medio'] = fuzz.trimf(variable.universe, [50, 100, 150])
        variable['alto'] = fuzz.trimf(variable.universe, [100, 200, 200])

    peligrosidad['baja'] = fuzz.trimf(peligrosidad.universe, [0, 0, 50])
    peligrosidad['media'] = fuzz.trimf(peligrosidad.universe, [25, 50, 75])
    peligrosidad['alta'] = fuzz.trimf(peligrosidad.universe, [50, 100, 100])

    # Definir reglas
    reglas = [
        ctrl.Rule(ataque['alto'] & velocidad['alto'], peligrosidad['alta']),
        ctrl.Rule(defensa['alto'] & ataque['medio'], peligrosidad['media']),
        ctrl.Rule(ataque['bajo'] & defensa['bajo'], peligrosidad['baja']),
        ctrl.Rule(velocidad['alto'] & defensa['baja'], peligrosidad['media']),
        # Añade más reglas si es necesario
    ]

    # Crear sistema de control
    sistema_control = ctrl.ControlSystem(reglas)
    simulador = ctrl.ControlSystemSimulation(sistema_control)

    return simulador

def calcular_peligrosidad(datos_pokemon, simulador):
    """Calcula la peligrosidad usando lógica difusa."""
    simulador.input['ataque'] = datos_pokemon['attack']
    simulador.input['defensa'] = datos_pokemon['defense']
    simulador.input['velocidad'] = datos_pokemon['speed']

    simulador.compute()
    nivel_peligrosidad = simulador.output['peligrosidad']

    if nivel_peligrosidad > 66:
        return 'Alta'
    elif nivel_peligrosidad > 33:
        return 'Media'
    else:
        return 'Baja'
