# src/battle_simulator.py

import random

class BattleSimulator:
    def __init__(self):
        pass

    def simulate_battle(self, pokemon1, pokemon2):
        """
        Simula una batalla entre dos Pokémon y retorna el resultado.

        Args:
            pokemon1 (dict): Diccionario con las estadísticas del primer Pokémon.
            pokemon2 (dict): Diccionario con las estadísticas del segundo Pokémon.

        Returns:
            dict: Resultado de la batalla incluyendo el ganador y el log de la batalla.
        """

        # Inicializar HP
        p1_hp = pokemon1['hp']
        p2_hp = pokemon2['hp']

        # Determinar el orden de ataque basado en la velocidad
        if pokemon1['speed'] > pokemon2['speed']:
            attacker, defender = pokemon1, pokemon2
            attacker_hp, defender_hp = p1_hp, p2_hp
        else:
            attacker, defender = pokemon2, pokemon1
            attacker_hp, defender_hp = p2_hp, p1_hp

        battle_log = []
        turn = 1

        battle_log.append(f"Comienza la batalla entre {pokemon1['name']} y {pokemon2['name']}!\n")
        battle_log.append(f"{attacker['name']} ataca primero debido a su mayor velocidad.\n\n")

        while attacker_hp > 0 and defender_hp > 0:
            battle_log.append(f"--- Turno {turn} ---\n")
            # Calcular daño
            damage = self.calculate_damage(attacker['attack'], defender['defense'])
            defender_hp -= damage
            defender_hp = max(defender_hp, 0)  # Evitar HP negativo

            battle_log.append(f"{attacker['name']} ataca a {defender['name']} causando {damage} de daño.\n")
            battle_log.append(f"HP de {defender['name']}: {defender_hp}/{defender['hp']}\n")

            if defender_hp == 0:
                battle_log.append(f"\n{defender['name']} ha sido derrotado!\n")
                battle_log.append(f"¡{attacker['name']} es el ganador de la batalla!\n")
                break

            # Cambiar de turno
            attacker, defender = defender, attacker
            attacker_hp, defender_hp = defender_hp, attacker_hp
            turn += 1
            battle_log.append("\n")

        winner = attacker['name'] if attacker_hp > 0 else defender['name']

        return {
            'winner': winner,
            'log': ''.join(battle_log)
        }

    def calculate_damage(self, attack, defense):
        """
        Calcula el daño infligido basado en las estadísticas de ataque y defensa.

        Args:
            attack (int): Estadística de ataque del atacante.
            defense (int): Estadística de defensa del defensor.

        Returns:
            int: Daño calculado.
        """
        # Fórmula simple de daño
        damage = attack - (defense / 2)
        damage = max(int(damage), 1)  # Asegurar al menos 1 de daño
        # Introducir aleatoriedad
        damage = random.randint(int(damage * 0.8), int(damage * 1.2))
        return damage
