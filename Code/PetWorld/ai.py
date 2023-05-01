import random

from coordinates import Coordinates

class Ai():
    """
    The class Ai is responsible for controlling the other teams' characters when not playing against another human.
    """

    def __init__(self, world):
        self.world = world
        self.targets = []

    def iterate_through_pets(self):
        print("I got here")
        for i in self.world.robots:
            if i.team == "Red":
                self.move(i)

    def move(self, pet):
        found = False
        moves = pet.get_possible_moves()
        self.find_targets()
        for j in moves:
            j = Coordinates(j[0], j[1])
            for i in self.targets:
                if i.get_x() == j.get_x() and i.get_y() == j.get_y():
                    target = j
                    found = True
        if found:
            pet.move_to(target.get_neighbor((random.randint(-1, 1), random.randint(-1, 1))))
            found = False
        else:
            index = random.randint(0, len(moves) - 1)
            pet.move_to(Coordinates(moves[index][0], moves[index][1]))

    def find_targets(self):
        for i in self.world.robots:
            if i.team == "Blue":
                self.targets.append(i.location)


    def attack(self, pet, attacker):
        """

        Attacks the target pet.

        """

        for i in pet.get_world().get_robots():
            if i.attacking == True:
                attacker = i
        if attacker.heavy_attacking:
            pet.set_health(pet.get_health() - int(attacker.strength * 1.5))
            attacker.mana -= 10
        else:
            pet.set_health(pet.get_health() - attacker.strength)
            attacker.mana -= 5
        if pet.get_health() < 0:
            pet.set_health(0)
        for i in pet.get_world().get_robots():
            if i.attacking == True:
                i.attacked = True
        print("debug")
        attacker.attacking = False
        attacker.heavy_attacking = False
        attacker.attacked = True
        attacker.get_world().attacking = False
        pet.get_world().reset_attacking()
