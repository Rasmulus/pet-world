import sys
from PyQt6.QtWidgets import QApplication

from gui import GUI

from direction import Direction
from petworld import *
from coordinates import *
from pet import *
from spinbot import *
from drunkbot import *
from nosebot import *
from lovebot import *
from dog import *


def main():
    """
    Creates a PetWorld, adds robots and launches the Graphical User Interface.

    Use this for testing your code.

    You can modify this however you like.
    """
    test_world = PetWorld(15, 15)
    wall1_coordinates = Coordinates(2, 4)
    test_world.add_wall(wall1_coordinates)
    wall2_coordinates = Coordinates(0, 5)
    test_world.add_wall(wall2_coordinates)
    wall3_coordinates = Coordinates(2, 2)
    test_world.add_wall(wall3_coordinates)
    wall4_coordinates = Coordinates(1, 3)
    test_world.add_wall(wall4_coordinates)


    dog_location = Coordinates(2, 3)
    dog_body = Pet('Dog')
    dog_brain = Dog(dog_body)
    dog_body.set_brain(dog_brain)
    test_world.add_robot(dog_body, dog_location, Direction.EAST)

    bad_dog_location = Coordinates(5, 3)
    dog_body = Pet('Bad Dog')
    dog_brain = Dog(dog_body)
    dog_body.set_brain(dog_brain)
    dog_body.change_team()
    test_world.add_robot(dog_body, bad_dog_location, Direction.EAST)

    dog_location = Coordinates(9, 7)
    dog_body = Pet('Dog')
    dog_brain = Dog(dog_body)
    dog_body.set_brain(dog_brain)
    test_world.add_robot(dog_body, dog_location, Direction.EAST)

    bad_dog_location = Coordinates(8, 5)
    dog_body = Pet('Bad Dog')
    dog_brain = Dog(dog_body)
    dog_body.set_brain(dog_brain)
    dog_body.change_team()
    test_world.add_robot(dog_body, bad_dog_location, Direction.EAST)



    # Every Qt application must have one instance of QApplication.
    global app # Use global to prevent crashing on exit
    app = QApplication(sys.argv)
    gui = GUI(test_world, 50)

    # Start the Qt event loop. (i.e. make it possible to interact with the gui)
    sys.exit(app.exec())

    # Any code below this point will only be executed after the gui is closed.


if __name__ == "__main__":
    main()
