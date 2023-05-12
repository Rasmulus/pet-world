from direction import Direction
from pet_brain import PetBrain


class Rodent(PetBrain):
    """
    The Rodent class is a subclass of the class Pet.
    """
    def __init__(self, body):

        super().__init__(body)
        self.body.range = 2
        self.body.att_range = 1
        self.body.strength = 20
        self.body.class_name = "Rodent"