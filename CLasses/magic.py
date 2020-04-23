import random


class Spell:
    def __init__(self, name, cost, power, type):
        self.name = name
        self.cost = cost
        self.power = power
        self.type = type

    def generate_spell_damage(self):
        # ±10% difference
        mgl = int(self.power * 0.9)
        mgh = int(self.power * 1.1)
        return random.randrange(mgl, mgh)

    def get_name(self):
        return self.name

    def get_cost(self):
        return self.cost

    def get_power(self):
        return self.power

    def get_type(self):
        return self.type


