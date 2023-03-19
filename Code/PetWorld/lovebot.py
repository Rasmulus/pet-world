import math

from direction import Direction
from pet_brain import PetBrain


class Lovebot(PetBrain):
    """
    The class Lovebot represents "brains" (or AI) of robots which have another robot as their "beloved". A lovebot tries to home in on its target.

    See the documentation of PetWorld
    """

    def __init__(self, body, beloved):
        """
        Creates a new lovebot brain for the given robot body. The lovebot considers the given other robot to be its "beloved".

        Parameter body is the robot whose actions the lovebot brain is supposed to control: Pet

        Parameter beloved is another robot that the lovebot is in love with and follows: Pet
        """
        super(Lovebot, self).__init__(body)
        self.beloved = beloved


    def move_body(self):
        """
        Moves the given "body", i.e., the robot given as a parameter. A lovebot tries to home in on its beloved unless
        it already is in an adjacent square (diagonally adjacent is not good enough). The lovebot does not know how to
        avoid obstacles, and blindly follows its primitive urges. If there is a wall or another bot in the chosen
        direction, the lovebot will collide into it (causing it to break instead of moving into the square).

        The path of movement is chosen as follows. First the lovebot calculates its distance to its target in both x and
        y dimension. It moves one square at a time so that either x or y distance decreases by one, depending on which
        one is greater. The greater of the two is decremented. In the case that the distances are equal, x is
        decremented. The lovebot only moves one square per turn. When moving (or colliding) a lovebot turns to face the
        direction it is moving in.

        This method assumes that it is called only if the robot is not broken or stuck.
        """
        location = self.body.get_location()
        next_direction = self.determine_direction(location)
        if next_direction:
            self.body.move(next_direction)

    def get_beloved(self):
        """
        Returns the beloved of the lovebot: Pet
        """
        return self.beloved


    def determine_direction(self, current_location):
        """
        Determines the direction the lovebot will attempt to move in.

        Parameter current_location is the lovebot's current location: Coordinates

        Returns the preferred direction of movement: tuple

        See move_body()
        """
        target_location = self.get_beloved().get_location()
        if target_location != None and current_location != None:
            distance_x = target_location.get_x() - current_location.get_x()
            distance_y = target_location.get_y() - current_location.get_y()
            if math.fabs(distance_x) >= math.fabs(distance_y):
                if distance_x > 1:
                    return Direction.EAST
                elif distance_x < -1:
                    return Direction.WEST
            else:
                if distance_y > 1:
                    return Direction.SOUTH
                elif distance_y < -1:
                    return Direction.NORTH
        return None
