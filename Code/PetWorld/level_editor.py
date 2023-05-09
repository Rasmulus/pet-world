import os
from PyQt6.QtWidgets import QApplication
from PyQt6 import QtCore
from gui import GUI

from direction import Direction
from petworld import *
from coordinates import *
from pet import *
from dog import *
from bird import *
from rodent import *
from cat import *
from reptile import *
def main():
    """
    Reads a savefile and creates a PetWorld, adds pets and launches the Graphical User Interface.
    """
    name = ""

    # Open the savegame
    with open('savedata/level_editor.ptwrld', 'r') as file:
        # Read the lines from the file
        #current_line = file.readline().rstrip()
        for current_line in file:
            try:
                current_line = current_line.rstrip()
                if current_line[0] == "#":
                    header_parts = current_line.split(" ")
                    category = header_parts[1]
                    if category == "Name":
                        name = file.readline().rstrip()
                    if category == "Size":
                        current_line = file.readline().rstrip()
                        parts = current_line.split("=")
                        dimensions = parts[1].rstrip()
                        dimensions = dimensions.split(",")
                        world = PetWorld(int(dimensions[0]), int(dimensions[1]), name, time)
                    if category == "Walls":
                        current_line = file.readline().rstrip()
                        parts = current_line.split("=")
                        coordinates = parts[1].rstrip()
                        coordinates = eval(coordinates)
                        for i in coordinates:
                            world.add_wall(Coordinates(i[0], i[1]))
                    if category == "Time":
                        current_line = file.readline().rstrip()
                        time = eval(current_line)
                        time = QtCore.QTime(time[0], time[1], time[2])

                    if category == "Turn":
                        current_line = file.readline().rstrip()
                        world.active_team = current_line

                    if category == "Pets":
                        while True:
                            current_line = file.readline().rstrip()
                            if current_line.startswith("#"):
                                # Reached the next category, break out of the loop
                                break
                            else:
                                # Execute the line as code
                                exec(current_line)
                    else:
                        pass
                else:
                    current_line = file.readline()

            except:
                pass




    global app # Use global to prevent crashing on exit
    app = QApplication(sys.argv)
    gui = GUI(world, 50)

    # Start the Qt event loop. (i.e. make it possible to interact with the gui)
    sys.exit(app.exec())

    # Any code below this point will only be executed after the gui is closed.


if __name__ == "__main__":
    main()