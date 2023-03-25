from coordinates import Coordinates
from pet_graphics_item import PetGraphicsItem
from petworld import PetWorld
from PyQt6 import QtWidgets, QtGui


class GuiExercise():
    """
    Normally these methods would be implemented in gui.py, but to make automatic
    exercise grading easier, they are implemented here.
    """

    def __init__(self, pet_world, scene, square_size):
        """
        Parameters:
        pet_world: PetWorld of the Gui-class
        scene: The QGraphicsScene of the Gui-class
        square_size: The width and height of a single square
        """
        self.pet_world = pet_world
        self.scene = scene
        self.square_size = square_size
        self.added_robots = []
        self.square_coordinates = {}
        self.highlighted_squares = []

    def add_pet_world_grid_items(self):
        """
        Implement me!

        The PetWorld already has the logical squares for the game
        and you can get these squares using its get_square method,
        but the squares for the user interface will be created here.
        This method adds an QGraphicsItem for each square in the robot world.
        Qt uses QGraphicsItems to draw objects in the QGraphicsScene.
        QGraphicsRectItem is a subclass of QGraphicsItem, and is useful for
        easily drawing rectangular items.
        This method should only be called once, otherwise it creates duplicates!

        What to do:


        1. Pseudocode:
            For each square in the PetWorld:
                -Create a new QGraphicsRectItem with the correct position, width, and height.
                -Add the newly created item to the scene (QGraphicsScene, in other words the variable scene set in __init__).


        2. The QGraphicsItems should be positioned as follows:
            1. The top left corner (origin) of the first square should be located at (0, 0).
            2. The second square on the x-axis (1, 0) should be located at (square_size, 0).
            3. The second square on the y-axis (0, 1) should be located at (0, square_size).
            4. etc..



        3. For full points, the walls in the PetWorld must be drawn as Dark gray
            and other squares must be drawn as Light gray. (See: RobotWold.add_wall)

            The rgb color values must be:
            Light gray: (211, 211, 211)
            Dark gray: (20, 20, 20)



        See PetWorld for getting the size of the world.

        Also see: https://doc.qt.io/qtforpython/PySide6/QtWidgets/QGraphicsItem.html
        and  https://doc.qt.io/qtforpython/PySide6/QtWidgets/QGraphicsRectItem.html
        and addItem() at  https://doc.qt.io/qtforpython/PySide6/QtWidgets/QGraphicsScene.html

        For changing the colors see:
        setBrush() at https://doc.qt.io/qtforpython/PySide6/QtWidgets/QAbstractGraphicsShapeItem.html
        and QBrush at https://doc.qt.io/qtforpython/PySide6/QtGui/QBrush.html
        and QColor at https://doc.qt.io/qtforpython/PySide6/QtGui/QColor.html
        """
        # Iterate over all squares in robot world
        # for x...:
            # for y...:

        height = PetWorld.get_height(self.pet_world)
        width = PetWorld.get_width(self.pet_world)
        for x in range(width):
            for y in range(height):
                coordinates = Coordinates(x, y)
                square = self.pet_world.get_square(coordinates)

                rect_item = QtWidgets.QGraphicsRectItem(x * self.square_size, y * self.square_size, self.square_size, self.square_size)

                if square.is_wall:
                    brush = QtGui.QBrush(QtGui.QColor(20, 20, 20))
                else:
                    brush = QtGui.QBrush(QtGui.QColor(211, 211, 211))
                rect_item.setBrush(brush)

                self.scene.addItem(rect_item)
                self.square_coordinates[rect_item] = coordinates

    def add_robot_graphics_items(self):
        """
        Implement me!

        Finds all robots in the PetWorld, which do not yet have a
        PetGraphicsItem and adds a PetGraphicsItem for them.
        If every robot already has a PetGraphicsItem, this method does nothing.

        NOTE: You don't have to check if any robots have been removed from the PetWorld

        What to do:

        1. Find all robots in the PetWorld, which do not yet have a PetGraphicsItem.
        2. Create PetGraphicsItem for all such robots and add these items to the QGraphicsScene.

        Hint: You can utilize the empty self.added_robots list for checking which robots have already been added

        See: PetGraphicsItem and PetWorld
        """

        robot_list = self.pet_world.get_robots()

        for i in robot_list:
            if i not in self.added_robots:
                self.added_robots.append(i)
                robot = PetGraphicsItem(i, self.square_size)

                #self.scene.addItem(robot)
                self.scene.addItem(robot)
                #self.scene.addItem(robot.makeHealthBar())


    def draw_possible_squares(self, possible_moves):

        # Iterate over all possible moves
        for move in possible_moves:
            print("debug")
            x, y = move[0], move[1]
            print("debug")
            rect_item = QtWidgets.QGraphicsRectItem(x * self.square_size, y * self.square_size, self.square_size,
                                                    self.square_size)


            if self.pet_world.active_team == "Red":
                # Set border color to solid red
                pen = QtGui.QPen(QtGui.QColor(254, 1, 154))
                pen.setWidth(1)
                rect_item.setPen(pen)

                # Set fill color to transparent red
                brush = QtGui.QBrush(QtGui.QColor(254, 1, 154, 25))
                rect_item.setBrush(brush)
                rect_item.setOpacity(0.75)
                self.highlighted_squares.append(rect_item)
                self.scene.addItem(rect_item)
                self.square_coordinates[rect_item] = Coordinates(x, y)
            else:
                # Set border color to solid blue
                pen = QtGui.QPen(QtGui.QColor(0, 255, 255))
                pen.setWidth(1)
                rect_item.setPen(pen)

                # Set fill color to transparent blue
                brush = QtGui.QBrush(QtGui.QColor(0, 255, 255, 25))
                rect_item.setBrush(brush)
                rect_item.setOpacity(0.75)
                self.highlighted_squares.append(rect_item)
                self.scene.addItem(rect_item)
                self.square_coordinates[rect_item] = Coordinates(x, y)