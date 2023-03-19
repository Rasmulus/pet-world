from PyQt6 import QtWidgets, QtCore, QtGui

from pet_graphics_item import PetGraphicsItem
from coordinates import Coordinates

from gui_exercise import GuiExercise


class GUI(QtWidgets.QMainWindow):
    """
    The class GUI handles the drawing of a PetWorld and allows user to
    interact with it.
    """

    def __init__(self, world, square_size):
        super().__init__()
        self.setCentralWidget(QtWidgets.QWidget()) # QMainWindown must have a centralWidget to be able to add layouts
        self.horizontal = QtWidgets.QHBoxLayout() # Horizontal main layout
        self.centralWidget().setLayout(self.horizontal)
        self.world = world
        self.square_size = square_size
        self.init_window()
        self.init_buttons()
        self.gui_exercise = GuiExercise(self.world, self.scene, self.square_size)

        self.add_robot_world_grid_items()
        self.add_robot_graphics_items()
        self.update_robots()

        # Set a timer to call the update function periodically
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_robots)
        self.timer.start(10) # Milliseconds


    def add_robot_world_grid_items(self):
        """
        Implement me in gui_exercise.py!

        Adds an QGraphicsItem for each square in the robot world.
        Qt uses QGraphicsItems to draw objects in the QGraphicsScene.
        QGraphicsRectItem is a subclass of QGraphicsItem, and is useful for
        easily drawing rectangular items.
        This method should only be called once, otherwise it creates duplicates!
        """
        # Calls your code in gui_exercise.py
        self.gui_exercise.add_robot_world_grid_items()


    def get_robot_graphics_items(self):
        """
        Returns all the PetGraphicsItem in the scene.

        NOTE: This is a silly implementation, it would be much more efficient to store
        all RobotGraphicsItems in a list and simply return that list.
        """
        items = []
        for item in self.scene.items():
            if type(item) is PetGraphicsItem:
                items.append(item)
        return items


    def add_robot_graphics_items(self):
        """
        Implement me in gui_exercise.py!

        Finds all robots in the PetWorld, which do not yet have a
        PetGraphicsItem and adds a PetGraphicsItem for them.
        If every robot already has a PetGraphicsItem, this method does nothing.
        """

        # Calls your code in gui_exercise.py
        self.gui_exercise.add_robot_graphics_items()


    def init_buttons(self):
        """
        Adds buttons to the window and connects them to their respective functions
        See: QPushButton at https://doc.qt.io/qtforpython/PySide6/QtWidgets/QPushButton.html
        """
        self.next_turn_btn = QtWidgets.QPushButton("Next full turn")
        self.next_turn_btn.clicked.connect(self.world.next_full_turn)
        self.horizontal.addWidget(self.next_turn_btn)


    def update_robots(self):
        """
        Iterates over all robot items and updates their position to match
        their physical representations in the robot world.
        """
        for robot_item in self.get_robot_graphics_items():
            robot_item.updateAll()
        self.scene.update()

    def init_window(self):
        """
        Sets up the window.
        """
        self.setGeometry(300, 300, 800, 800)
        self.setWindowTitle('PetWorld')
        self.show()

        # Add a scene for drawing 2d objects
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, 700, 700)

        # Add a view for showing the scene
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.show()
        self.horizontal.addWidget(self.view)
