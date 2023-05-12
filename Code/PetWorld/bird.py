from direction import Direction
from pet_brain import PetBrain


class Bird(PetBrain):
    """
    The Bird class is a subclass of the class Pet.
    """
    def __init__(self, body):

        super().__init__(body)
        self.body.range = 5
        self.body.att_range = 1
        self.body.strength = 30
        self.body.flying = True
        self.body.class_name = "Bird"