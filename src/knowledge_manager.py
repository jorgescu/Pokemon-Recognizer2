from fuzzywuzzy import process

class KnowledgeManager:
    def __init__(self, df):
        """
        Representación del Conocimiento. Pequeño motor de QA.
        Esto es un ejemplo de cómo podríamos relacionar las preguntas del usuario con respuestas.
        """
        self.df = df
        # Conocimientos simples (podría ser base de hechos/reglas)
        self.knowledge_base = {
            "¿Qué es un Pokémon?": "Un Pokémon es una criatura ficticia que aparece en la franquicia Pokémon.",
            "¿Cuál es el Pokémon número 1?": "El Pokémon número 1 es Bulbasaur.",
            "¿Qué tipo de Pokémon es Bulbasaur?": "Bulbasaur es de tipo Grass/Poison.",
            "¿Qué es la lógica borrosa?": "La lógica borrosa es una forma de razonar que permite valores de verdad parciales, "
                                         "utilizada para manejar la incertidumbre.",
            "¿Qué es un Algoritmo Evolutivo?": "Un Algoritmo Evolutivo es un tipo de metaheurística inspirada en la evolución natural.",
            "¿Qué es el Test de Turing?": "El Test de Turing es una prueba para determinar si una máquina puede exhibir comportamiento inteligente indistinguible del de un humano.",
            "¿Cómo se reconoce un Pokémon a partir de una imagen?": "Se pueden extraer características visuales (HOG, color) y usar un clasificador entrenado (p.ej. SVM).",
            "¿Qué es la Percepción Computacional?": "La percepción computacional es la capacidad de un sistema para interpretar datos sensoriales (imágenes, sonidos) y generar información útil."
        }

    def answer_question(self, question):
        """
        Usa fuzzy matching para encontrar la pregunta más similar en la base de conocimiento.
        """
        keys = list(self.knowledge_base.keys())
        best_match, score = process.extractOne(question, keys)
        if score > 60:
            return self.knowledge_base[best_match]
        else:
            return "No estoy seguro de la respuesta, intenta otra pregunta."
