import sys
from PyQt6.QtWidgets import QApplication
from PyQt6 import QtCore

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
from bird import *
from rodent import *
def main():
    """
    Creates a PetWorld, adds robots and launches the Graphical User Interface.

    Use this for testing your code.

    You can modify this however you like.
    """
    time = QtCore.QTime(0, 0, 0)
    test_world = PetWorld(15, 15, "Test World - launch main2.py instead", time)
    wall1_coordinates = Coordinates(2, 4)
    test_world.add_wall(wall1_coordinates)
    wall2_coordinates = Coordinates(0, 5)
    test_world.add_wall(wall2_coordinates)
    wall3_coordinates = Coordinates(2, 2)
    test_world.add_wall(wall3_coordinates)
    wall4_coordinates = Coordinates(1, 3)
    test_world.add_wall(wall4_coordinates)
    test_world.active_team = "Level Editor"
    dog_location = Coordinates(14, 14)
    dog_body = Pet('Dog')
    dog_brain = Dog(dog_body)
    dog_body.set_brain(dog_brain)
    test_world.add_robot(dog_body, dog_location, Direction.NORTH)

    bad_dog_location = Coordinates(14, 0)
    dog_body = Pet('Bad Dog')
    dog_brain = Dog(dog_body)
    dog_body.set_brain(dog_brain)
    dog_body.change_team()
    test_world.add_robot(dog_body, bad_dog_location, Direction.SOUTH)

    bird_location = Coordinates(0, 14)
    bird_body = Pet('Bird')
    bird_brain = Bird(bird_body)
    bird_body.set_brain(bird_brain)
    test_world.add_robot(bird_body, bird_location, Direction.NORTH)

    bad_bird_location = Coordinates(0, 0)
    bird_body = Pet('Bad Bird')
    bird_brain = Bird(bird_body)
    bird_body.set_brain(bird_brain)
    bird_body.change_team()
    test_world.add_robot(bird_body, bad_bird_location, Direction.SOUTH)



    # Every Qt application must have one instance of QApplication.
    global app # Use global to prevent crashing on exit
    app = QApplication(sys.argv)
    gui = GUI(test_world, 50)

    # Start the Qt event loop. (i.e. make it possible to interact with the gui)
    sys.exit(app.exec())

    # Any code below this point will only be executed after the gui is closed.


if __name__ == "__main__":
    main()
