from direction import Direction
from pet_brain import PetBrain


class Reptile(PetBrain):
    """
    The Reptile class is a subclass of the class Pet.
    """
    def __init__(self, body):

        super().__init__(body)
        self.body.range = 1
        self.body.att_range = 2
        self.body.strength = 20
        self.body.class_name = "Reptile"