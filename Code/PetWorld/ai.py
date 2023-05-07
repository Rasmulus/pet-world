import random

from coordinates import Coordinates

class Ai():
    """
    The class Ai is responsible for controlling the other teams' characters when not playing against another human.
    """

    def __init__(self, world):
        self.world = world
        self.targets = []
        self.targets_dict = {}

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
        if found and pet.health >= int(pet.max_health * 0.5) and pet.mana >= 5:
            all_pets = self.world.robots
            all_locations = []
            for i in self.world.robots:
                all_locations.append(i.location)
                try:
                    if str(self.targets_dict[i]) == str(target):
                        #attack(i, pet)
                        #target_pet = i
                        #all_locations.append(i.location)

                        self.attack(i, pet)
                        #self.attack(target_pet,pet)
                        pet.move_to(target.get_neighbor((random.randint(-1, 1), random.randint(-1, 1))))
                        while pet.location in self.targets:
                            pet.move_to(target.get_neighbor((random.randint(-1, 1), random.randint(-1, 1))))
                        found = False
                        break
                except KeyError:
                    pass

        elif pet.mana >= 10 and pet.health < pet.max_health:
            index = random.randint(0, len(moves) - 1)
            pet.move_to(Coordinates(moves[index][0], moves[index][1]))
            pet.health = pet.max_health
            pet.mana -= 10

        elif pet.mana < 10:
            pet.mana = pet.max_mana

        else:
            index = random.randint(0, len(moves) - 1)
            pet.move_to(Coordinates(moves[index][0], moves[index][1]))

    def find_targets(self):
        self.targets = []
        self.targets_dict = {}
        for i in self.world.robots:
            if i.team == "Blue":
                if i.location not in self.targets:
                    self.targets.append(i.location)
                self.targets_dict[i] = i.location


    def attack(self, pet, attacker):
        """

        Attacks the target pet.

        """
        if attacker.mana >= 10 and pet.health >= int(pet.max_health * 0.4):
            attacker.heavy_attacking = True
        elif attacker.mana >= 5:
            attacker.attacking = True

        if attacker.heavy_attacking:
            pet.set_health(pet.get_health() - int(attacker.strength * 1.5))
            attacker.mana -= 10
        elif attacker.attacking:
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
        self.check_if_won()

    def check_if_won(self):
        blue_found = False
        red_found = False
        for i in self.world.get_robots():
            if i.team == "Blue":
                blue_found = True
            else:
                red_found = True
        if blue_found == False:
            self.world.won = "Red"
            return True

        elif red_found == False:
            self.world.won = "Blue"
            return True
        else:
            return False
