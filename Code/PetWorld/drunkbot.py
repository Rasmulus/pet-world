import random

from direction import Direction
from pet_brain import PetBrain


class Drunkbot(PetBrain):
    """
    The class Drunkbot represents the "brains" (or AI) of robots which stagger from place to place. The AI of such a
    robot brains is based purely on a (pseudo)random number generator.

    See the documentation of robotworld.PetWorld
    """

    def __init__(self, body, random_seed):
        """
        Creates a new drunkbot brain that controls the given robot body.

        Each Drunkbot has its own unique Random object (a random number generator). Drunkbot does not create a
        new Random number generator every time this method is called.

        See the documentation of random (in https://docs.python.org/3.4/library/random.html).

        Parameter body is the robot whose actions the nosebot brain is supposed to control: Pet

        Parameter random_seed is the seed that feeds the random generator that guides the bot: int
        """
        super(Drunkbot, self).__init__(body)
        self.random = random.Random(random_seed)


    def move_body(self):
        """
        Moves the robot. A drunkbot selects a random direction and tries to move to the adjacent square in that
        direction. If there is a wall or another robot in that square, the robot will collide (and does not move). If
        the drunkbot collides with something, it remains facing whatever it collided with and ends its turn there. If
        the drunkbot did not collide with anything, it turns in a new direction after moving. The new facing is again
        selected again at random. Note: this means that assuming that the drunkbot did not collide, it picks two random
        directions per turn, one to move in and one to face in.

        The drunkbot selects a random direction using the following algorithm:

        - Get all the direction constants in a list, in the order defined by the direction module.

        - Select a random list item (for example, using random.choice(sequence)).

        - Use the direction found.

        This method assumes that it is called only if the robot is not broken or stuck.

        See direction.get_values()

        See random.choice()
        """
        if self.body.move(self.get_random_direction()):
            self.body.spin(self.get_random_direction())


    def get_random_direction(self):
        """
        Selects a random direction.

        Returns: random direction: tuple
        """
        directions = Direction.get_values()
        return self.random.choice(directions)
