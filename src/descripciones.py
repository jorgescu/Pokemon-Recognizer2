# src/descripciones.py

def determinar_habitat(tipo):
    """Determina el hábitat probable según el tipo de Pokémon."""
    habitats = {
        'Agua': 'ríos, lagos y océanos',
        'Fuego': 'volcanes y áreas cálidas',
        # ...
    }
    return habitats.get(tipo, 'hábitats desconocidos')

def generar_descripcion(nombre, tipo, habitat, peligrosidad):
    """Genera una descripción del Pokémon."""
    descripcion = f"{nombre} es un Pokémon de tipo {tipo}. "
    descripcion += f"Suele habitar en {habitat}. "
    descripcion += f"Su peligrosidad es de {peligrosidad:.2f} sobre 10."
    return descripcion
