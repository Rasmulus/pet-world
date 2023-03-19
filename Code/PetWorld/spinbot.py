from direction import Direction
from pet_brain import PetBrain


class Spinbot(PetBrain):
    """
    The class C{Spinbot} represents the "brains"
    (or AI) of very simple, boring robots that stand still
    and merely spin clockwise.
    """


    def move_body(self):
        """
        Moves the given "body", i.e., the robot given as a parameter.
        A spinbot just spins 90 degrees clockwise as its move.

        This method assumes that it is called only if the robot is not
        broken or stuck.
        """
        facing = self.body.get_facing()
        next_facing = Direction.get_next_clockwise(facing)
        self.body.spin(next_facing)
