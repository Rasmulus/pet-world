from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import QPropertyAnimation


class LevelEndWidget(QtWidgets.QDialog):
    def __init__(self, parent, won, elapsed_time, new_record, record):
        self.result = None
        super().__init__(parent)
        self.setWindowTitle("Level Complete")
        self.setFixedSize(800, 600)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Window | QtCore.Qt.WindowType.CustomizeWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint | QtCore.Qt.WindowType.FramelessWindowHint)
        # Create the rounded rectangle shape
        rounded_rect = QtGui.QPainterPath()
        rounded_rect.addRoundedRect(QtCore.QRectF(0, 0, self.width(), self.height()), 20, 20)
        #self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        # Set the widget mask to the rounded rectangle shape
        path = QtGui.QPainterPath()
        rect = self.rect()
        rectf = QtCore.QRectF(rect.x(), rect.y(), rect.width(), rect.height())
        path.addRoundedRect(rectf, 20, 20)

        mask = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(mask)
        # Set the widget stylesheet
        self.setStyleSheet("""
            LevelEndWidget {
                background-color: white;
                border: 15px solid black;
            }
        """)
        # Create the UI elements
        self.won_label = QtWidgets.QLabel(f"{won} won!", self)
        self.won_label.setFont(QtGui.QFont("Arial", 80, QtGui.QFont.Weight.Bold))
        self.won_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(80)
        font.setBold(True)
        self.won_label.setFont(font)

        self.time_label = QtWidgets.QLabel(f"Time: {elapsed_time}\n Record: {record}", self)
        self.time_label.setFont(QtGui.QFont("Arial", 40))
        self.time_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignCenter)

        # Create the new record animated stamp
        if new_record:
            self.new_record_stamp = QtWidgets.QLabel(self)
            self.new_record_stamp.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
            self.new_record_stamp.setPixmap(QtGui.QPixmap("new_record.png"))
            self.new_record_stamp.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.new_record_stamp.setHidden(not new_record)

            animation = QPropertyAnimation(self.new_record_stamp, b"pos")
            # Set the duration of the animation
            animation.setDuration(10000)
            # Set the start and end values for the animation
            start_pos = QtCore.QPoint(self.width(), self.new_record_stamp.y())
            end_pos = QtCore.QPoint(self.width() - self.new_record_stamp.width(), self.new_record_stamp.y())
            animation.setStartValue(start_pos)
            animation.setEndValue(end_pos)
            # Start the animation
            #animation.start()

        self.next_level_button = QtWidgets.QPushButton("Next Level", self)
        self.next_level_button.setFont(QtGui.QFont("Arial", 30))
        self.next_level_button.clicked.connect(self.next_level)

        self.try_again_button = QtWidgets.QPushButton("Try Again", self)
        self.try_again_button.setFont(QtGui.QFont("Arial", 30))
        self.try_again_button.clicked.connect(self.try_again)

        self.main_menu_button = QtWidgets.QPushButton("Return to Main Menu", self)
        self.main_menu_button.setFont(QtGui.QFont("Arial", 30))
        self.main_menu_button.clicked.connect(self.return_to_main_menu)

        # Set up the layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.won_label)

        # Add a new horizontal layout for the time label and new record stamp
        time_layout = QtWidgets.QHBoxLayout()
        time_layout.addWidget(self.time_label)
        if new_record:
            time_layout.addWidget(self.new_record_stamp)
        time_layout.setSpacing(0)

        layout.addLayout(time_layout) # Add the new horizontal layout

        # Add some vertical space between the time layout and the buttons
        layout.addSpacing(50)

        # Add a new widget to hold the buttons
        button_widget = QtWidgets.QWidget(self)
        button_widget_layout = QtWidgets.QHBoxLayout(button_widget)
        button_widget_layout.addWidget(self.next_level_button)
        button_widget_layout.addWidget(self.try_again_button)
        button_widget_layout.addWidget(self.main_menu_button)
        #button_widget_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        layout.addWidget(button_widget)  # Add the button widget to the main layout

    def start_animation(self):
        # Start the new record stamp animation
        if self.new_record_stamp.isVisible():
            animation = QPropertyAnimation(self.new_record_stamp, b"pos")
            # Set the duration of the animation
            animation.setDuration(1000)
            # Set the start and end values for the animation
            start_pos = QtCore.QPoint(self.width(), self.new_record_stamp.y())
            end_pos = QtCore.QPoint(self.width() - self.new_record_stamp.width(), self.new_record_stamp.y())
            animation.setStartValue(start_pos)
            animation.setEndValue(end_pos)
            # Start the animation
            animation.start()

    def exec(self):
        # Center the dialog on the parent widget or the screen
        if self.parent():
            parent_rect = self.parent().geometry()
            self.setGeometry(
                parent_rect.x() + (parent_rect.width() - self.width()) // 2,
                parent_rect.y() + (parent_rect.height() - self.height()) // 2,
                self.width(),
                self.height(),
            )
        else:
            screen_rect = QtWidgets.QApplication.primaryScreen().availableGeometry()
            self.setGeometry(
                screen_rect.width() // 2 - self.width() // 2,
                screen_rect.height() // 2 - self.height() // 2,
                self.width(),
                self.height(),
            )
        #self.start_animation()
        #return "try_again"

        return super().exec()


    def next_level(self):
        self.result = "next_level"
        self.close()
        #self.accept()
        # Do something to proceed to the next level

    def try_again(self):
        self.result = "try_again"
        self.close()

        #self.accept()
        # Do something to restart the current level

    def return_to_main_menu(self):
        self.result = "main_menu"
        self.close()
        #self.reject()
        # Do something to return to the main menu
