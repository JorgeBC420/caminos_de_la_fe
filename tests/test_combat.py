import unittest
from systems.combat_system import calculate_damage

class TestCombat(unittest.TestCase):
    def test_damage_calculation(self):
        class Dummy:
            def __init__(self, attack_damage, fuerza=0, defensa=0):
                self.attack_damage = attack_damage
                self.stats = {'fuerza': fuerza, 'defensa': defensa}
        attacker = Dummy(100, fuerza=10)
        defender = Dummy(0, defensa=50)
        damage = calculate_damage(attacker, defender)
        self.assertEqual(damage, 60)

if __name__ == '__main__':
    unittest.main()
