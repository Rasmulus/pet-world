from direction import Direction
from pet_brain import PetBrain


class Dog(PetBrain):
    """
    The Dog class is a subclass of the class Pet.
    """
    def __init__(self, body):

        super().__init__(body)
        self.body.range = 4
        self.body.att_range = 2
        self.body.strength = 40
        self.body.class_name = "Dog"
