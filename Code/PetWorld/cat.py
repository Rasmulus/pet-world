from direction import Direction
from pet_brain import PetBrain


class Cat(PetBrain):
    """
    The Cat class is a subclass of the class Pet.
    """
    def __init__(self, body):

        super().__init__(body)
        self.body.range = 3
        self.body.att_range = 4
        self.body.strength = 30
        self.body.class_name = "Cat"