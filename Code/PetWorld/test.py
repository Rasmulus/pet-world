import unittest

from petworld import PetWorld
from pet import Pet
from coordinates import Coordinates
from direction import Direction
from spinbot import Spinbot
from drunkbot import Drunkbot
from lovebot import Lovebot
from nosebot import Nosebot


class Test(unittest.TestCase):
    """
    Some tests for the PetWorld-project.
    """

    def setUp(self):
        self.test_world = PetWorld(5, 5)
        wall_coordinates = Coordinates(2, 4)
        self.test_world.add_wall(wall_coordinates)

        first_location = Coordinates(4, 3)
        first_body = Pet('Bart')
        first_brain = Spinbot(first_body)
        first_body.set_brain(first_brain)
        self.test_world.add_robot(first_body, first_location, Direction.EAST)


    def test_nosebot(self):
        """
        Tests the nosebot movements.
        """
        fifth_location = Coordinates(4, 4)
        fifth_body = Pet('Speedy Gonzales')
        fifth_brain = Nosebot(fifth_body)
        fifth_body.set_brain(fifth_brain)
        self.test_world.add_robot(fifth_body, fifth_location, Direction.WEST)


        self.test_world.next_full_turn()
        self.test_world.next_full_turn()

        self.assertEqual('(3, 3)', str(self.test_world.get_robots()[1].get_location()),
                "the nosebot should be in (3, 3) after two moves")


    def test_drunkbot(self):
        """
        Tests the drunkbot movements.
        """
        fifth_location = Coordinates(4, 4)
        fifth_body = Pet('Speedy Gonzales')
        fifth_brain = Nosebot(fifth_body)
        fifth_body.set_brain(fifth_brain)
        self.test_world.add_robot(fifth_body, fifth_location, Direction.WEST)

        second_location = Coordinates(2, 2)
        second_body = Pet('Homer')
        second_brain = Drunkbot(second_body, 4522)
        second_body.set_brain(second_brain)
        self.test_world.add_robot(second_body, second_location, Direction.SOUTH)


        self.test_world.next_full_turn()
        self.test_world.next_full_turn()

        self.assertEqual('(3, 3)', str(self.test_world.get_robots()[1].get_location()),
                "the nosebot should be in (3, 3) after two moves")

        self.assertEqual('(2, 3)', str(self.test_world.get_robots()[2].get_location()),
                "the drunkbot should be in (2, 3) after two moves")

        self.assertTrue(self.test_world.get_robot(1).is_broken(),
                        'the drunkbot collided with the nosebot, the nosebot should be broken')


if __name__ == "__main__":
    unittest.main()
