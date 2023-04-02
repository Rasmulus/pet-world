from direction import Direction
from pet_brain import PetBrain


class Reptile(PetBrain):
    """
    The class Reptile represents the "brains" (or AI) of robots that move where their nose is pointing, in straight
    lines, turning right when they are forced to.

    See the documentation of PetWorld
    """
    def __init__(self, body):

        super().__init__(body)
        self.body.range = 1
        self.body.att_range = 2
        self.body.strength = 20
        self.body.class_name = "Reptile"
    def move_body(self):
        """
        Moves the given "body", i.e., the robot given as a parameter. A reptile first looks at the next square in the
        direction of its nose. If that square is empty, it moves there and ends its turn. If the square was not empty,
        it turns its nose 90 degrees clockwise and tries again, moving if possible, etc. If the robot makes a full 360
        turnabout without finding a suitable square to move in, it ends its turn without moving. As a reptile always
        looks where it's going, so it can never collide with anything during its own turn.

        This method assumes that it is called only if the robot is not broken or stuck.
        """

        turned = 0
        while (turned < 360):
            position = self.body.get_location()
            facing = self.body.get_facing()
            next_coordinate = position.get_neighbor(facing)
            next_square = self.body.get_world().get_square(next_coordinate)
            if (next_square.is_empty()):
                self.body.move_forward()
                return
            else:
                facing = Direction.get_next_clockwise(facing)
                self.body.spin(facing)
                turned += 90
