from PyQt6 import QtWidgets, QtCore, QtGui

from pet_graphics_item import PetGraphicsItem
from coordinates import Coordinates
from square import Square
from level_end_widget import LevelEndWidget
from gui_exercise import GuiExercise
from pet import *
from dog import *
from bird import *
from rodent import *
from cat import *
from reptile import *
import os

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
        self.possible_squares = None
        self.possible_drawn = False
        self.init_window()
        self.init_buttons()
        self.gui_exercise = GuiExercise(self.world, self.scene, self.square_size)
        self.showMaximized()
        self.showFullScreen()



        self.add_pet_world_grid_items()
        self.add_robot_graphics_items()
        self.update_robots()

        # Set a timer to call the update function periodically
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_robots)
        self.timer.start(10) # Milliseconds


        #do other things
        self.pos = None
        self.item = None
        self.end_widget_activated = False

        # Create a timer that fires every second
        self.elapsed_time = self.world.time  # initialize elapsed time to saved time
        self.clock = QtCore.QTimer(self)
        self.clock.timeout.connect(self.showTime)
        self.clock.start(1000)  # update elapsed time every second

        # Create a LCD display widget
        self.lcd = QtWidgets.QLCDNumber(self)
        self.lcd.setSegmentStyle(QtWidgets.QLCDNumber.SegmentStyle.Filled)
        self.lcd.setDigitCount(8)
        #self.lcd.setSize(300, 80) # Set the size of the clock widget
        self.layout().addWidget(self.lcd)
        self.lcd.setStyleSheet("background-color: white; color: black;")
        self.lcd.setGeometry(2090,10,300,80)


    def showTime(self):
        # Increment elapsed time by 1 second
        self.elapsed_time = self.elapsed_time.addSecs(1)
        self.world.time = self.elapsed_time

        # Set the format of the time
        timeString = self.elapsed_time.toString('hh:mm:ss')

        # Display the time on the LCD display widget
        self.lcd.display(timeString)
    def add_pet_world_grid_items(self):
        """
        Implement me in gui_exercise.py!

        Adds an QGraphicsItem for each square in the robot world.
        Qt uses QGraphicsItems to draw objects in the QGraphicsScene.
        QGraphicsRectItem is a subclass of QGraphicsItem, and is useful for
        easily drawing rectangular items.
        This method should only be called once, otherwise it creates duplicates!
        """
        # Calls your code in gui_exercise.py
        self.gui_exercise.add_pet_world_grid_items()


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
        self.end_turn_btn = QtWidgets.QPushButton("End Turn")
        self.end_turn_btn.clicked.connect(self.world.change_active_team)

        self.save_game_btn = QtWidgets.QPushButton("Save and Quit")
        self.save_game_btn.clicked.connect(self.show_confirmation_dialog)

        self.save_as_btn = QtWidgets.QPushButton("Save World As")
        self.save_as_btn.clicked.connect(self.show_saving_window)

        self.load_game_btn = QtWidgets.QPushButton("Load Game")
        self.load_game_btn.clicked.connect(self.choose_save_window)
        self.horizontal.addWidget(self.load_game_btn)

        self.change_size_btn = QtWidgets.QPushButton("Change World Size")
        self.change_size_btn.clicked.connect(self.change_size_window)
        self.horizontal.addWidget(self.change_size_btn)

        self.debug_btn = QtWidgets.QPushButton("Debug")
        self.debug_btn.clicked.connect(self.end_level)
        self.horizontal.addWidget(self.debug_btn)

        if self.world.active_team == "Level Editor":
            self.horizontal.addWidget(self.save_as_btn)

        else:
            self.horizontal.addWidget(self.end_turn_btn)
            self.horizontal.addWidget(self.save_game_btn)

    def end_level(self):
        if not self.end_widget_activated:
            timeString = self.elapsed_time.toString('hh:mm:ss')
            self.level_end_widget = LevelEndWidget(self, self.world.won, timeString, True)
            #self.level_end_widget.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
            self.level_end_widget.exec()
            self.level_end_widget.start_animation()
            self.end_widget_activated = True

    def show_confirmation_dialog(self):
        """
        Shows a confirmation dialog when the user clicks the "Save and Quit" button
        """
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg_box.setText("Are you sure you want to quit? Any moves you have made during this turn will not be saved.")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        ret = msg_box.exec()

        if ret == QtWidgets.QMessageBox.StandardButton.Yes:
            self.close()

    def update_robots(self):
        """
        Iterates over all robot items and updates their position to match
        their physical representations in the robot world.
        """
        for robot_item in self.get_robot_graphics_items():
            robot_item.updateAll()
        self.scene.update()
        self.update_window()
        if self.world.moving and self.possible_squares is None and self.possible_drawn is False:
            self.possible_drawn = True
            for i in self.world.get_robots():
                #print("debug")
                if i.get_moving_state():
                    possible_moves = i.get_possible_moves()
                    self.possible_squares = self.gui_exercise.draw_possible_squares(possible_moves)

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

        # Set the background color
        if self.world.active_team == "Blue":
            self.view.setStyleSheet("background-color: blue;")
        elif self.world.active_team == "Red":
            self.view.setStyleSheet("background-color: red;")
        else:
            self.view.setStyleSheet("background-color: grey;")

        # Create stage name widget
        self.stage_name = QtWidgets.QLabel(self.world.name)
        #self.stage_name.setFixedSize(1000, 1000) # Set the size of the clock widget
        self.stage_name.setGeometry(0, -50, self.world.width * 50, 50)
        self.stage_name.setStyleSheet(
            "QLabel { font-size: 32px; font-weight: bold; border: 2px solid black; background-color: beige }")

        self.stage_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.scene.addWidget(self.stage_name)

    def update_window(self):
        if self.world.active_team == "Blue":
            self.view.setStyleSheet("background-color: blue;")
        elif self.world.active_team == "Red":
            self.view.setStyleSheet("background-color: red;")
        else:
            self.view.setStyleSheet("background-color: grey;")

        if self.world.won is not None:
            self.end_level()
    def change_size_window(self):

        self.change_size_window = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(self.change_size_window)

        width_label = QtWidgets.QLabel("Enter desired width of the world:")
        layout.addWidget(width_label)

        width_layout = QtWidgets.QHBoxLayout()
        self.width_input = QtWidgets.QLineEdit()
        width_layout.addWidget(self.width_input)



        layout.addLayout(width_layout)

        height_label = QtWidgets.QLabel("Enter desired height of the world:")
        layout.addWidget(height_label)

        self.height_input = QtWidgets.QLineEdit()
        layout.addWidget(self.height_input)

        confirm_btn = QtWidgets.QPushButton("Confirm")
        confirm_btn.clicked.connect(self.confirm_change)
        layout.addWidget(confirm_btn)

        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.change_size_window.close)
        layout.addWidget(cancel_btn)

        self.change_size_window.show()

    def confirm_change(self):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setText(f"Are you sure you want to change the size of the world? All changes will be lost.")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel)
        result = msg_box.exec()

        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            self.change_dimensions()

    def change_dimensions(self):
        width = self.width_input.text()
        height = self.height_input.text()

        # removes all pets from the world
        for i in self.world.get_robots():
            i.set_health(0)
        # removes all obstacles
        for i in self.gui_exercise.squares:
            coordinates = str(self.gui_exercise.square_coordinates[i])
            coordinates = eval(coordinates)
            if coordinates in self.world.obstacles:
                coordinates = Coordinates(int(coordinates[0]), int(coordinates[1]))
                self.toggle_obstacle(coordinates)

        # removes all grid items
        self.gui_exercise.remove_pet_world_grid_items()

        # adds new grid items
        self.world.width = int(width)
        self.world.height = int(height)

        for x in range(self.world.width):  # stepper
            self.world.squares[x] = [None] * self.world.height
            for y in range(self.world.height):  # stepper
                self.world.squares[x][y] = Square()

        self.gui_exercise.add_pet_world_grid_items()

        # updates the stage name widget
        self.stage_name.hide()
        self.stage_name.setText(self.world.name)
        self.stage_name.setGeometry(0, -50, self.world.width * 50, 50)
        self.stage_name.show()

    def choose_save_window(self):
        self.choose_save_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(self.choose_save_widget)

        saves = os.listdir("savedata")
        for save in saves:
            save_btn = QtWidgets.QPushButton(save)
            save_btn.clicked.connect(lambda checked, save=save: self.confirm_load(save))
            layout.addWidget(save_btn)

        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.choose_save_widget.close)
        layout.addWidget(cancel_btn)

        self.choose_save_widget.show()

    def confirm_load(self, save):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setText(f"Are you sure you want to load this world: {save}?")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel)
        result = msg_box.exec()

        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            self.load_world(save)
            self.choose_save_widget.close()
    def load_world(self, save):
        #removes all pets from the world
        for i in self.world.get_robots():
            i.set_health(0)
        #removes all obstacles
        for i in self.gui_exercise.squares:
            coordinates = str(self.gui_exercise.square_coordinates[i])
            coordinates = eval(coordinates)
            if coordinates in self.world.obstacles:
                coordinates = Coordinates(int(coordinates[0]), int(coordinates[1]))
                self.toggle_obstacle(coordinates)

        #removes all grid items
        self.gui_exercise.remove_pet_world_grid_items()

        # loads information from the save
        self.world.load_game(save)

        #adds new grid items
        self.gui_exercise.add_pet_world_grid_items()

        #adds new pets
        self.gui_exercise.add_robot_graphics_items()

        #updates timer to reflect saved time
        self.elapsed_time = self.world.new_time

        # updates the stage name widget
        self.stage_name.hide()
        self.stage_name.setText(self.world.name)
        self.stage_name.setGeometry(0, -50, self.world.width * 50, 50)
        self.stage_name.show()

    def show_saving_window(self):
        self.saving_window = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(self.saving_window)

        filename_label = QtWidgets.QLabel("Enter the filename that you would like to save the level to:")
        layout.addWidget(filename_label)

        filename_layout = QtWidgets.QHBoxLayout()
        self.filename_input = QtWidgets.QLineEdit()
        filename_layout.addWidget(self.filename_input)

        extension_label = QtWidgets.QLabel(".ptwrld")
        filename_layout.addWidget(extension_label)

        layout.addLayout(filename_layout)

        worldname_label = QtWidgets.QLabel("What should your world be called?")
        layout.addWidget(worldname_label)

        self.worldname_input = QtWidgets.QLineEdit()
        layout.addWidget(self.worldname_input)

        save_btn = QtWidgets.QPushButton("Save")
        save_btn.clicked.connect(self.save)
        layout.addWidget(save_btn)

        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.saving_window.close)
        layout.addWidget(cancel_btn)

        self.saving_window.show()

    def save(self):
        filename = self.filename_input.text() + ".ptwrld"
        worldname = self.worldname_input.text()
        self.world.save_game_as(filename, worldname)

    def toggle_obstacle(self, coordinates):
        self.world.toggle_wall(coordinates)
        self.gui_exercise.update_pet_world_grid_items()

    def mousePressEvent(self, event, *args, **kwargs):
        if self.world.active_team == "Level Editor":
            # Get the item that was clicked on
            pos = self.view.mapToScene(event.pos())
            self.pos = pos
            # print(self.pos)
            pos = self.view.mapFromScene(pos)
            item = self.view.itemAt(pos)
            self.item = item
            # print(self.item.coordinates.get_x())
            self.pos = pos
            # print(self.pos)
            print(item)
            # print(self.gui_exercise.square_coordinates[self.item])
            if isinstance(item, QtWidgets.QGraphicsRectItem):  # check if it's a SquareItem
                menu = QtWidgets.QMenu()
                font = menu.font()
                font.setPointSize(font.pointSize() + 5)
                menu.setFont(font)
                rows = ["Toggle Obstacle", "Add Pet"]
                for row in rows:
                    action = QtWidgets.QWidgetAction(menu)
                    label = QtWidgets.QLabel(row)
                    action.setDefaultWidget(label)
                    menu.addAction(action)
                    if row == "Add Pet":
                        submenu = QtWidgets.QMenu("Add Pet", menu)
                        pet_types = ["Dog", "Cat", "Rodent", "Reptile", "Bird"]
                        for pet_type in pet_types:
                            pet_action = QtWidgets.QWidgetAction(submenu)
                            pet_label = QtWidgets.QLabel(pet_type)
                            pet_action.setDefaultWidget(pet_label)
                            submenu.addAction(pet_action)
                            submenu.setFont(font)
                            pet_action.triggered.connect(
                                lambda checked, pet_type=pet_type: self.handleContextMenuAction(pet_type))

                        action.setMenu(submenu)

                    else:
                        action.triggered.connect(
                            lambda checked, row=row: self.handleContextMenuAction(row))
                # Show the menu at the position of the event
                # pos = self.view.mapFromGlobal(self.view.mapToGlobal(event.pos()))
                menu.exec(pos)

        if self.world.moving:
            # Get the item that was clicked on
            pos = self.view.mapToScene(event.pos())
            self.pos = pos
            #print(self.pos)
            pos = self.view.mapFromScene(pos)
            item = self.view.itemAt(pos)
            self.item = item
            #print(self.item.coordinates.get_x())
            self.pos = pos
            #print(self.pos)
            print(item)
            #print(self.gui_exercise.square_coordinates[self.item])
            if isinstance(item, QtWidgets.QGraphicsRectItem):  # check if it's a SquareItem
                menu = QtWidgets.QMenu()
                font = menu.font()
                font.setPointSize(font.pointSize() + 5)
                menu.setFont(font)
                rows = ["Move here", "Cancel"]
                for row in rows:
                    action = QtWidgets.QWidgetAction(menu)
                    label = QtWidgets.QLabel(row)
                    action.setDefaultWidget(label)
                    menu.addAction(action)
                    action.triggered.connect(
                        lambda checked, row=row: self.handleContextMenuAction(row))
                # Show the menu at the position of the event
                #pos = self.view.mapFromGlobal(self.view.mapToGlobal(event.pos()))
                menu.exec(pos)

    def handleContextMenuAction(self, row):
        print(f"handleContextMenuAction called with row={row}")
        if row == "Move here":
            for i in self.world.get_robots():
                if i.get_moving_state():
                    print(i.get_possible_moves())
                    print(self.gui_exercise.square_coordinates[self.item])
                    #print(self.world.squares)
                    i.move_to(self.gui_exercise.square_coordinates[self.item])
                    self.world.reset_moving()
            for square in self.gui_exercise.highlighted_squares:
                self.gui_exercise.scene.removeItem(square)
            self.possible_drawn = False


        elif row == "Cancel":
            for square in self.gui_exercise.highlighted_squares:
                self.gui_exercise.scene.removeItem(square)
            self.possible_drawn = False
            self.world.reset_moving()

        elif row == "Toggle Obstacle":
            coordinates = str(self.gui_exercise.square_coordinates[self.item])
            coordinates = eval(coordinates)
            coordinates = Coordinates(int(coordinates[0]), int(coordinates[1]))

            self.toggle_obstacle(coordinates)

        elif row == "Dog":
            coordinates = str(self.gui_exercise.square_coordinates[self.item])
            coordinates = eval(coordinates)
            location = Coordinates(int(coordinates[0]), int(coordinates[1]))
            body = Pet('Dog')
            brain = Dog(body)
            body.set_brain(brain)
            self.world.add_robot(body, location, Direction.NORTH)
            self.gui_exercise.add_robot_graphics_items()

        elif row == "Cat":
            coordinates = str(self.gui_exercise.square_coordinates[self.item])
            coordinates = eval(coordinates)
            location = Coordinates(int(coordinates[0]), int(coordinates[1]))
            body = Pet('Cat')
            brain = Cat(body)
            body.set_brain(brain)
            self.world.add_robot(body, location, Direction.NORTH)
            self.gui_exercise.add_robot_graphics_items()

        elif row == "Rodent":
            coordinates = str(self.gui_exercise.square_coordinates[self.item])
            coordinates = eval(coordinates)
            location = Coordinates(int(coordinates[0]), int(coordinates[1]))
            body = Pet('Rodent')
            brain = Rodent(body)
            body.set_brain(brain)
            self.world.add_robot(body, location, Direction.NORTH)
            self.gui_exercise.add_robot_graphics_items()

        elif row == "Reptile":
            coordinates = str(self.gui_exercise.square_coordinates[self.item])
            coordinates = eval(coordinates)
            location = Coordinates(int(coordinates[0]), int(coordinates[1]))
            body = Pet('Reptile')
            brain = Reptile(body)
            body.set_brain(brain)
            self.world.add_robot(body, location, Direction.NORTH)
            self.gui_exercise.add_robot_graphics_items()

        elif row == "Bird":
            coordinates = str(self.gui_exercise.square_coordinates[self.item])
            coordinates = eval(coordinates)
            location = Coordinates(int(coordinates[0]), int(coordinates[1]))
            body = Pet('Bird')
            brain = Bird(body)
            body.set_brain(brain)
            self.world.add_robot(body, location, Direction.NORTH)
            self.gui_exercise.add_robot_graphics_items()

        else:
            pass

