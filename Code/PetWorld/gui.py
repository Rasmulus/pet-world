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
import time
from PIL import ImageGrab

class GUI(QtWidgets.QMainWindow):
    """
    The class GUI handles the drawing of a PetWorld and allows user to
    interact with it.
    """

    def __init__(self, world, square_size):
        super().__init__()
        self.setCentralWidget(QtWidgets.QWidget()) # QMainWindown must have a centralWidget to be able to add layouts
        self.horizontal = QtWidgets.QHBoxLayout() # Horizontal main layout
        self.vertical = QtWidgets.QVBoxLayout() # Vertical button layout

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
        self.timer.start(100) # Milliseconds


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
        self.lcd.setGeometry(self.vertical.geometry().x(), 10, 300, 80)


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
        self.end_turn_btn.clicked.connect(self.on_end_turn)
        self.end_turn_btn.setFont(QtGui.QFont("Arial", 30))
        self.end_turn_btn.setMinimumHeight(100)
        self.vertical.addWidget(self.end_turn_btn)


        self.save_game_btn = QtWidgets.QPushButton("Save and Quit")
        self.save_game_btn.clicked.connect(self.show_confirmation_dialog)
        self.save_game_btn.setFont(QtGui.QFont("Arial", 30))
        self.save_game_btn.setMinimumHeight(100)
        self.vertical.addWidget(self.save_game_btn)

        self.save_as_btn = QtWidgets.QPushButton("Save World As")
        self.save_as_btn.clicked.connect(self.show_saving_window)
        self.save_as_btn.setFont(QtGui.QFont("Arial", 30))
        self.save_as_btn.setMinimumHeight(100)
        self.vertical.addWidget(self.save_as_btn)

        self.load_game_btn = QtWidgets.QPushButton("Load Game")
        self.load_game_btn.clicked.connect(self.choose_save_window)
        self.load_game_btn.setFont(QtGui.QFont("Arial", 30))
        self.vertical.addWidget(self.load_game_btn)
        self.load_game_btn.setMinimumHeight(100)

        self.change_size_btn = QtWidgets.QPushButton("Change World Size")
        self.change_size_btn.clicked.connect(self.change_size_window)
        self.change_size_btn.setFont(QtGui.QFont("Arial", 30))
        self.vertical.addWidget(self.change_size_btn)
        self.change_size_btn.setMinimumHeight(100)

        self.debug_btn = QtWidgets.QPushButton("Debug")
        self.debug_btn.clicked.connect(self.end_level)
        self.debug_btn.setFont(QtGui.QFont("Arial", 30))
        self.vertical.addWidget(self.debug_btn)
        self.debug_btn.setMinimumHeight(100)

        self.horizontal.addLayout(self.vertical)

    def on_end_turn(self):
        self.world.change_active_team()
        self.save_screenshot("savegame")

    def end_level(self):
        if not self.end_widget_activated:
            #self.load_world(self.world.file_name)

            timeString = self.elapsed_time.toString('hh:mm:ss')
            self.level_end_widget = LevelEndWidget(self, self.world.won, timeString, True)
            #self.level_end_widget.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

            #self.level_end_widget.exec()
            self.level_end_widget.exec()
            self.end_widget_activated = True
            result = self.level_end_widget.result
            if result == "try_again":
                self.restart_level()

            elif result == "next_level":
                self.next_level()

            elif result == "main_menu":
                self.main_menu()

            #self.level_end_widget.start_animation()

    def restart_level(self):
        self.world.won = None
        if self.world.file_name == "savegame.ptwrld":
            self.world.file_name = self.world.name
            self.world.file_name = self.world.file_name.replace("Level ", "level_")
            self.world.file_name += ".ptwrld"
        self.load_world(self.world.file_name)
        self.end_widget_activated = False

    def next_level(self):
        self.world.won = None
        if self.world.file_name == "savegame.ptwrld":
            self.world.file_name = self.world.name
            self.world.file_name = self.world.file_name.replace("Level ", "level_")
            self.world.file_name += ".ptwrld"

        if "level" in self.world.file_name:
            parts = self.world.file_name.split("_")
            number = int(parts[1][0])
            number += 1
            self.world.file_name = f"level_{str(number)}.ptwrld"
        try:
            self.load_world(self.world.file_name)
            self.end_widget_activated = False
        except:
            self.end_widget_activated = False


    def main_menu(self):
        self.end_widget_activated = False

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

        # Add background to level
        filename = "level_n_bg.jpg"
        found = False
        for i in self.world.name:
            if i.isnumeric():
                filename = filename.replace("n", i)
                found = True
        if found is False:
            filename = "bg.png"

        pixmap = QtGui.QPixmap(f"savedata/{filename}").scaled(
            self.world.width * self.square_size,
            self.world.height * self.square_size
        )
        self.pixmap_item = QtWidgets.QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.pixmap_item)
        self.pixmap_item.setPos(0, 0)

        # Add a view for showing the scene
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.show()
        self.horizontal.addWidget(self.view)
        self.scene.setSceneRect(-500, -500, 2000, 2000)

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
        self.view.scale(0.75, 0.75)
        #self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        #self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.view.setDragMode(QtWidgets.QGraphicsView.dragMode(self.view).ScrollHandDrag)
    def wheelEvent(self, event):
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        # Zoom
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        self.view.scale(zoomFactor, zoomFactor)
        event.accept()


    def update_window(self):
        if self.world.active_team == "Blue":
            self.view.setStyleSheet("background-color: blue;")
            self.change_size_btn.hide()
            self.save_as_btn.hide()
            self.end_turn_btn.show()


        elif self.world.active_team == "Red":
            self.view.setStyleSheet("background-color: red;")
            self.change_size_btn.hide()
            self.save_as_btn.hide()
            self.end_turn_btn.show()


        else:
            self.view.setStyleSheet("background-color: grey;")
            self.change_size_btn.show()
            self.save_as_btn.show()
            self.end_turn_btn.hide()

        if self.world.won is not None:
            self.end_level()

    def change_size_window(self):

        self.change_size_window = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(self.change_size_window)

        width_label = QtWidgets.QLabel("Enter desired width of the world:")
        width_label.setFont(QtGui.QFont("Arial", 30))
        layout.addWidget(width_label)

        width_layout = QtWidgets.QHBoxLayout()
        self.width_input = QtWidgets.QLineEdit()
        self.width_input.setFont(QtGui.QFont("Arial", 30))
        width_layout.addWidget(self.width_input)



        layout.addLayout(width_layout)

        height_label = QtWidgets.QLabel("Enter desired height of the world:")
        height_label.setFont(QtGui.QFont("Arial", 30))
        layout.addWidget(height_label)

        self.height_input = QtWidgets.QLineEdit()
        self.height_input.setFont(QtGui.QFont("Arial", 30))
        layout.addWidget(self.height_input)

        confirm_btn = QtWidgets.QPushButton("Confirm")
        confirm_btn.clicked.connect(self.confirm_change)
        confirm_btn.setFont(QtGui.QFont("Arial", 30))
        layout.addWidget(confirm_btn)

        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.change_size_window.close)
        cancel_btn.setFont(QtGui.QFont("Arial", 30))
        layout.addWidget(cancel_btn)

        self.change_size_window.setGeometry(1525, 500, 650, 500)

        self.change_size_window.setWindowFlags(
            QtCore.Qt.WindowType.Window | QtCore.Qt.WindowType.CustomizeWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint | QtCore.Qt.WindowType.FramelessWindowHint)
        # Create the rounded rectangle shape
        rounded_rect = QtGui.QPainterPath()
        rounded_rect.addRoundedRect(
            QtCore.QRectF(0, 0, self.change_size_window.width(), self.change_size_window.height()), 20, 20)

        # Set the widget mask to the rounded rectangle shape
        path = QtGui.QPainterPath()
        rect = self.change_size_window.rect()
        rectf = QtCore.QRectF(rect.x(), rect.y(), rect.width(), rect.height())
        path.addRoundedRect(rectf, 20, 20)

        mask = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.change_size_window.setMask(mask)
        # Set the widget stylesheet
        self.change_size_window.setObjectName("chooseSaveWidget")
        self.change_size_window.setStyleSheet("""
                    #chooseSaveWidget {
                        background-color: white;
                        border: 5px solid black;
                        border-radius: 20px;
                    }
                """)
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

        # updates background
        filename = "level_n_bg.jpg"
        found = False
        for i in self.world.name:
            if i.isnumeric():
                filename = filename.replace("n", i)
                found = True
        if found is False:
            filename = "bg.png"


        self.pixmap_item.hide()
        pixmap = QtGui.QPixmap(f"savedata/{filename}").scaled(
        self.world.width * self.square_size,
        self.world.height * self.square_size
        )
        self.pixmap_item.setPixmap(pixmap)
        self.pixmap_item.show()


    def choose_save_window(self):
        self.choose_save_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(self.choose_save_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        #change UI
        self.choose_save_widget.setFixedSize(800, 600)

        self.choose_save_widget.setLayout(layout)
        self.choose_save_widget.setWindowFlags(
            QtCore.Qt.WindowType.Window | QtCore.Qt.WindowType.CustomizeWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint | QtCore.Qt.WindowType.FramelessWindowHint)
        # Create the rounded rectangle shape
        rounded_rect = QtGui.QPainterPath()
        rounded_rect.addRoundedRect(QtCore.QRectF(0, 0, self.choose_save_widget.width(), self.choose_save_widget.height()), 20, 20)

        # Set the widget mask to the rounded rectangle shape
        path = QtGui.QPainterPath()
        rect = self.choose_save_widget.rect()
        rectf = QtCore.QRectF(rect.x(), rect.y(), rect.width(), rect.height())
        path.addRoundedRect(rectf, 20, 20)

        mask = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.choose_save_widget.setMask(mask)
        # Set the widget stylesheet
        self.choose_save_widget.setObjectName("chooseSaveWidget")
        self.choose_save_widget.setStyleSheet("""
            #chooseSaveWidget {
                background-color: white;
                border: 15px solid black;
                border-radius: 20px;
            }
        """)

        # Create the header
        self.header = QtWidgets.QLabel(f"Load Game", self)
        self.header.setFont(QtGui.QFont("Arial", 60, QtGui.QFont.Weight.Bold))
        self.header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(60)
        font.setBold(True)
        self.header.setFont(font)
        layout.addWidget(self.header)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scrollContent = QtWidgets.QWidget(scroll)
        scrollLayout = QtWidgets.QVBoxLayout(scrollContent)
        scrollContent.setLayout(scrollLayout)

        saves = [f for f in os.listdir("savedata") if f.endswith('.ptwrld')]
        for save in saves:
            # Remove the file extension from the button label
            button_label = os.path.splitext(save)[0]

            # Check if there is a corresponding image file with a ".jpg" extension
            image_file = os.path.join("savedata", button_label + ".jpg")
            if os.path.exists(image_file):
                icon = QtGui.QIcon(image_file)
                pixmap = icon.pixmap(QtCore.QSize(100, 100))  # change the size of the icon
                button_label = button_label.replace(button_label, f"    {button_label}")
                button_label = button_label.replace("level_", "Level ")
                save_btn = QtWidgets.QPushButton(button_label)
                save_btn.setIconSize(QtCore.QSize(100, 100))  # change the size of the icon on the button
                save_btn.setIcon(QtGui.QIcon(pixmap))
            else:
                button_label = button_label.replace(button_label, f"    {button_label}")
                button_label = button_label.replace("level_", "Level ")
                save_btn = QtWidgets.QPushButton(button_label)

            save_btn.clicked.connect(lambda checked, save=save: self.confirm_load(save))
            save_btn.setFont(QtGui.QFont("Arial", 30))
            save_btn.setMinimumHeight(100)
            scrollLayout.addWidget(save_btn)

        scroll.setWidget(scrollContent)
        layout.addWidget(scroll)

        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.setFont(QtGui.QFont("Arial", 30))
        cancel_btn.setMinimumHeight(100)

        cancel_btn.clicked.connect(self.choose_save_widget.close)
        layout.addWidget(cancel_btn)

        self.choose_save_widget.show()

    def confirm_load(self, save):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setText(f"Are you sure you want to load this world: {save}?")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel)
        msg_box.setWindowFlags(
            QtCore.Qt.WindowType.Window | QtCore.Qt.WindowType.CustomizeWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        # Create the rounded rectangle shape
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

        # updates background
        filename = "level_n_bg.jpg"
        found = False
        for i in self.world.name:
            if i.isnumeric():
                filename = filename.replace("n", i)
                found = True
        if found is False:
            filename = "bg.png"


        self.pixmap_item.hide()
        pixmap = QtGui.QPixmap(f"savedata/{filename}").scaled(
        self.world.width * self.square_size,
        self.world.height * self.square_size
        )
        self.pixmap_item.setPixmap(pixmap)
        self.pixmap_item.show()

    def show_saving_window(self):
        self.saving_window = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(self.saving_window)

        filename_label = QtWidgets.QLabel("Enter the filename that you would\nlike to save the level to:")
        filename_label.setFont(QtGui.QFont("Arial", 30))
        #filename_label.setMaximumHeight(50)
        layout.addWidget(filename_label)

        filename_layout = QtWidgets.QHBoxLayout()
        self.filename_input = QtWidgets.QLineEdit()
        self.filename_input.setFont(QtGui.QFont("Arial", 30))
        #self.filename_input.setMinimumHeight(100)
        filename_layout.addWidget(self.filename_input)

        extension_label = QtWidgets.QLabel(".ptwrld")
        extension_label.setFont(QtGui.QFont("Arial", 30))
        #extension_label.setMinimumHeight(100)
        filename_layout.addWidget(extension_label)

        layout.addLayout(filename_layout)

        worldname_label = QtWidgets.QLabel("What should your world be called?")
        worldname_label.setFont(QtGui.QFont("Arial", 30))

        layout.addWidget(worldname_label)

        self.worldname_input = QtWidgets.QLineEdit()
        self.worldname_input.setFont(QtGui.QFont("Arial", 30))
        #self.worldname_input.setMinimumHeight(100)
        layout.addWidget(self.worldname_input)

        save_btn = QtWidgets.QPushButton("Save")
        save_btn.clicked.connect(self.save)
        save_btn.clicked.connect(self.saving_window.close)
        save_btn.setFont(QtGui.QFont("Arial", 30))
        #save_btn.setMinimumHeight(100)
        layout.addWidget(save_btn)

        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.saving_window.close)
        cancel_btn.setFont(QtGui.QFont("Arial", 30))
        #cancel_btn.setMinimumHeight(100)
        layout.addWidget(cancel_btn)

        self.saving_window.setGeometry(1525, 500, 650, 500)

        self.saving_window.setWindowFlags(
            QtCore.Qt.WindowType.Window | QtCore.Qt.WindowType.CustomizeWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint | QtCore.Qt.WindowType.FramelessWindowHint)
        # Create the rounded rectangle shape
        rounded_rect = QtGui.QPainterPath()
        rounded_rect.addRoundedRect(
            QtCore.QRectF(0, 0, self.saving_window.width(), self.saving_window.height()), 20, 20)

        # Set the widget mask to the rounded rectangle shape
        path = QtGui.QPainterPath()
        rect = self.saving_window.rect()
        rectf = QtCore.QRectF(rect.x(), rect.y(), rect.width(), rect.height())
        path.addRoundedRect(rectf, 20, 20)

        mask = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.saving_window.setMask(mask)
        # Set the widget stylesheet
        self.saving_window.setObjectName("chooseSaveWidget")
        self.saving_window.setStyleSheet("""
                    #chooseSaveWidget {
                        background-color: white;
                        border: 5px solid black;
                        border-radius: 20px;
                    }
                """)

        self.saving_window.show()

    def save_screenshot(self, filename):
        screenshot_file = os.path.join("savedata/", os.path.splitext(filename)[0] + ".jpg")
        scene_rect = self.scene.sceneRect()
        pixmap = QtGui.QPixmap(scene_rect.size().toSize())
        pixmap.fill(QtCore.Qt.GlobalColor.white)
        painter = QtGui.QPainter(pixmap)
        self.scene.setSceneRect(0, 0, self.world.width * self.square_size, self.world.height * self.square_size)
        self.scene.render(painter)
        painter.end()
        pixmap.save(screenshot_file, "JPG")

    def save(self):
        filename = self.filename_input.text() + ".ptwrld"
        worldname = self.worldname_input.text()
        self.world.save_game_as(filename, worldname)
        self.save_screenshot(filename)

    def toggle_obstacle(self, coordinates):
        self.world.toggle_wall(coordinates)
        self.gui_exercise.update_pet_world_grid_items()

    def mousePressEvent(self, event, *args, **kwargs):

        # engage dragging
        self.dragging = True
        self.lastMousePos = event.pos()

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

