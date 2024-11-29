# src/optimizacion.py

import random
import numpy as np
from deap import base, creator, tools, algorithms
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC

def optimizar_modelo(X, y):
    """Optimiza los hiperparámetros del SVM utilizando algoritmos genéticos."""

    # Definir el problema de maximización
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    # Definir los atributos y el individuo
    toolbox.register("C", random.uniform, -5, 15)
    toolbox.register("gamma", random.uniform, -15, 3)
    toolbox.register("individual", tools.initCycle, creator.Individual, (toolbox.C, toolbox.gamma), n=1)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Definir la función de evaluación
    def evaluar_individuo(individuo):
        C = 2 ** individuo[0]
        gamma = 2 ** individuo[1]
        modelo = SVC(C=C, gamma=gamma)
        scores = cross_val_score(modelo, X, y, cv=3, scoring='accuracy')
        return scores.mean(),

    toolbox.register("evaluate", evaluar_individuo)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # Configurar el algoritmo genético
    population = toolbox.population(n=20)
    ngen = 10
    cxpb = 0.5
    mutpb = 0.2

    # Ejecutar el algoritmo genético
    algorithms.eaSimple(population, toolbox, cxpb, mutpb, ngen, verbose=False)

    # Obtener el mejor individuo
    best_individual = tools.selBest(population, k=1)[0]
    best_C = 2 ** best_individual[0]
    best_gamma = 2 ** best_individual[1]

    print(f"Mejores parámetros encontrados: C={best_C}, gamma={best_gamma}")
    return best_C, best_gamma

# Esta función se puede usar durante el entrenamiento del modelo para encontrar los mejores hiperparámetros
