import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl


class FuzzyDangerEvaluator:
    def __init__(self):
        """
        Lógica borrosa para estimar la peligrosidad. (Lógica Borrosa)
        """
        self.attack = ctrl.Antecedent(np.arange(0, 201, 1), 'attack')
        self.defense = ctrl.Antecedent(np.arange(0, 201, 1), 'defense')
        self.danger = ctrl.Consequent(np.arange(0, 101, 1), 'danger')

        self.attack['low'] = fuzz.trapmf(self.attack.universe, [0, 0, 50, 80])
        self.attack['medium'] = fuzz.trimf(self.attack.universe, [50, 100, 150])
        self.attack['high'] = fuzz.trapmf(self.attack.universe, [120, 150, 200, 200])

        self.defense['low'] = fuzz.trapmf(self.defense.universe, [0, 0, 50, 80])
        self.defense['medium'] = fuzz.trimf(self.defense.universe, [50, 100, 150])
        self.defense['high'] = fuzz.trapmf(self.defense.universe, [120, 150, 200, 200])

        self.danger['low'] = fuzz.trimf(self.danger.universe, [0, 25, 50])
        self.danger['medium'] = fuzz.trimf(self.danger.universe, [30, 50, 70])
        self.danger['high'] = fuzz.trimf(self.danger.universe, [60, 80, 100])

        rule1 = ctrl.Rule(self.attack['low'] & self.defense['low'], self.danger['low'])
        rule2 = ctrl.Rule(
            (self.attack['medium'] | self.defense['medium']) & ~((self.attack['high'] & self.defense['high'])),
            self.danger['medium'])
        rule3 = ctrl.Rule(self.attack['high'] & self.defense['high'], self.danger['high'])

        system = ctrl.ControlSystem([rule1, rule2, rule3])
        self.sim = ctrl.ControlSystemSimulation(system)

    def evaluate(self, attack_val, defense_val):
        self.sim.input['attack'] = attack_val
        self.sim.input['defense'] = defense_val
        self.sim.compute()
        return self.sim.output['danger']
