from PyQt6 import QtWidgets, QtGui, QtCore
from pet import Pet
from coordinates import Coordinates

class PetGraphicsItem(QtWidgets.QGraphicsPolygonItem):
    """
    The class PetGraphicsItem extends QGraphicsPolygonItem to link it together to the physical
    representation of a Pet. The QGraphicsPolygonItem handles the drawing, while the
    Pet knows its own location and status.

    NOTE: unfortunately the PyQt6 uses different naming conventions than the rest
    of this project. We are also overriding the mousePressEvent()-method, whose
    name cannot be changed. Therefore, this class has a different style of naming the
    method names. (for example: updatePosition() vs update_position())
    """

    def __init__(self, pet, square_size):
        # Call init of the parent object
        super(PetGraphicsItem, self).__init__()

        # Do other stuff
        self.pet = pet
        self.square_size = square_size
        brush = QtGui.QBrush(1) # 1 for even fill
        self.setBrush(brush)
        self.constructTriangleVertices()
        self.health_bar_proxy = self.makeHealthBar()
        self.name_tag_proxy = self.makeNameTag()
        self.updateAll()


        # create a progress bar widget to show health

        #self.health_bar_proxy.update()

    def makeNameTag(self):
        self.name_tag = QtWidgets.QLabel()
        self.name_tag.setText(self.pet.get_name())

        # make the font size larger
        font = self.name_tag.font()
        font.setPointSize(font.pointSize() + 5)
        self.name_tag.setFont(font)

        # create a proxy widget for the name tag
        name_tag_proxy = QtWidgets.QGraphicsProxyWidget(self)
        name_tag_proxy.setWidget(self.name_tag)

        return name_tag_proxy

    def updateNameTag(self):
        """
        Updates the name tag to follow the location of the parent pet.
        """
        # get the rotation of this item and set the rotation of the proxy widget
        rotation = self.rotation()
        self.name_tag_proxy.setRotation(-rotation)

        # calculate the center point of the triangle
        center_x = self.square_size / 2
        center_y = self.square_size / 2

        # calculate the offset for the name tag proxy widget
        offset_x = center_x - 50
        offset_y = -self.name_tag.height() - 65

        # set the position of the proxy widget
        self.name_tag_proxy.setPos(offset_x, offset_y)

        # calculate the rotated offset using a transformation matrix
        transformation = QtGui.QTransform()
        transformation.rotate(-rotation)
        offset = transformation.map(QtCore.QPointF(offset_x, offset_y))

        # set the position of the health bar proxy widget relative to the center point
        self.name_tag_proxy.setPos(center_x + offset.x(), center_y + offset.y())


    def makeHealthBar(self):
        self.health_bar = QtWidgets.QProgressBar()
        self.health_bar.setMaximum(100)
        self.health_bar.setMinimum(0)
        self.health_bar.setValue(self.pet.get_health())

        # create a proxy widget for the progress bar
        self.health_bar_proxy = QtWidgets.QGraphicsProxyWidget(self)
        self.health_bar_proxy.setWidget(self.health_bar)

        #self.health_bar_proxy.setRotation(-self.rotation())

        return self.health_bar_proxy

    def updateHealthBar(self):
        """
        Updates the health bar to match the health of the parent pet.
        """
        self.health_bar.setValue(self.pet.get_health())

        # get the rotation of this item and set the rotation of the proxy widget
        rotation = self.rotation()
        self.health_bar_proxy.setRotation(
            -rotation)  # set the rotation of the proxy widget to the negative of this item's rotation
        # calculate the center point of the triangle
        center_x = self.square_size / 2
        center_y = self.square_size / 2

        # calculate the offset for the health bar proxy widget
        offset_x = center_x - 100
        offset_y = - 50 - self.health_bar_proxy.size().height() / 2

        # calculate the rotated offset using a transformation matrix
        transformation = QtGui.QTransform()
        transformation.rotate(-rotation)
        offset = transformation.map(QtCore.QPointF(offset_x, offset_y))

        # set the position of the health bar proxy widget relative to the center point
        self.health_bar_proxy.setPos(center_x + offset.x(), center_y + offset.y())

    def constructTriangleVertices(self):
        """
        This method sets the shape of this item into a triangle.

        The QGraphicsPolygonItem can be in the shape of any polygon.
        We use triangles to represent pets, as it makes it easy to
        show the current facing of the pet.
        """
        # Create a new QPolygon object
        triangle = QtGui.QPolygonF()

        # Add the corners of a triangle to the the polygon object
        triangle.append(QtCore.QPointF(self.square_size/2, 0)) # Tip
        triangle.append(QtCore.QPointF(0, self.square_size)) # Bottom-left
        triangle.append(QtCore.QPointF(self.square_size, self.square_size)) # Bottom-right
        triangle.append(QtCore.QPointF(self.square_size/2, 0)) # Tip

        # Set this newly created polygon as this Item's polygon.
        self.setPolygon(triangle)

        # Set the origin of transformations to the center of the triangle.
        # This makes it easier to rotate this Item.
        self.setTransformOriginPoint(self.square_size/2, self.square_size/2)


    def updateAll(self):
        """
        Updates the visual representation to correctly resemble the current
        location, direction and status of the parent pet.
        """
        self.updatePosition()
        self.updateRotation()
        self.updateColor()
        self.updateHealthBar()
        self.updateNameTag()
        #self.health_bar_proxy.setWidget(self.health_bar)

    def updatePosition(self):
        """
        Implement me!

        Update the coordinates of this item to match the attached pet.
        Remember to take in to account the size of the squares.

        A pet in the first (0, 0) square should be drawn at (0, 0).

        See: For setting the position of this GraphicsItem, see
        QGraphicsPolygonItem at https://doc.qt.io/qtforpython/PySide6/QtWidgets/QGraphicsPolygonItem.html
        and its parent class QGraphicsItem at https://doc.qt.io/qtforpython/PySide6/QtWidgets/QGraphicsItem.html

        For getting the location of the parent pet, look at the Pet-class
        in pet.py.
        """

        location = self.pet.get_location()
        x = Coordinates.get_x(location)
        y = Coordinates.get_y(location)
        self.setPos(x * self.square_size, y * self.square_size)


    def updateRotation(self):
        """
        Implement me!

        Rotates this item to match the rotation of parent pet.
        A method for rotating can be found from QGraphicsItem at https://doc.qt.io/qtforpython/PySide6/QtWidgets/QGraphicsItem.html

        """
        print(self.pet.get_facing())
        print(self.pet.get_location())
        print(self.pet.get_location_square())

        facing = self.pet.get_facing()
        up = (0, 1)
        down = (0, -1)
        left = (-1, 0)
        right = (1, 0)

        if facing == up:
            self.setRotation(180)
        elif facing == down:
            self.setRotation(0)
        elif facing == left:
            self.setRotation(270)
        elif facing == right:
            self.setRotation(90)



    def updateColor(self):
        """
        Implement me!

        Draw broken pets in red, stuck pets in yellow and working pets in green.

        The rgb values of the colors must be the following:
        - red: (255, 0, 0)
        - yellow: (255, 255, 0)
        - green: (0, 255, 0)

        See: setBrush() at https://doc.qt.io/qtforpython/PySide6/QtWidgets/QAbstractGraphicsShapeItem.html
        and QBrush at https://doc.qt.io/qtforpython/PySide6/QtGui/QBrush.html
        and QColor at https://doc.qt.io/qtforpython/PySide6/QtGui/QColor.html

        Look at pet.py for checking the status of the pet.
        """
        state = ""
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 0))
        self.setBrush(brush)



        if self.pet.is_broken():
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
            state = "broken"
            self.setBrush(brush)

        elif not self.pet.is_broken():
            brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))


        if self.pet.is_stuck():
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 0))
            state = "stuck"

        self.setBrush(brush)

    #def updateHealthBar(self):
        #self.health_bar_proxy.setWidget(self.health_bar)



    def mousePressEvent(self, event, *args, **kwargs):

        #Check if attacking
        if not self.pet.get_attack_state() and self.pet.get_world().attacking:
            menu = QtWidgets.QMenu()
            # make the font size larger
            font = menu.font()
            font.setPointSize(font.pointSize() + 5)
            menu.setFont(font)
            # Create the menu items and add them to the menu
            rows = ["Choose Target", "Cancel"]
            for row in rows:
                action = QtWidgets.QWidgetAction(menu)
                label = QtWidgets.QLabel(row)
                action.setDefaultWidget(label)
                menu.addAction(action)
                # Connect the action to a method that handles it
                action.triggered.connect(lambda checked, row=row: self.handleContextMenuAction(row))
            # Show the menu at the position of the event
            menu.exec(event.screenPos())

        elif not self.pet.get_attack_state():
            menu = QtWidgets.QMenu()
            # make the font size larger
            font = menu.font()
            font.setPointSize(font.pointSize() + 5)
            menu.setFont(font)
            # Create the menu items and add them to the menu
            rows = ["Move", "Attack", "Heal"]
            for row in rows:
                action = QtWidgets.QWidgetAction(menu)
                label = QtWidgets.QLabel(row)
                action.setDefaultWidget(label)
                menu.addAction(action)
                # Connect the action to a method that handles it
                action.triggered.connect(lambda checked, row=row: self.handleContextMenuAction(row))
            # Show the menu at the position of the event
            menu.exec(event.screenPos())
        else:
            pass

    def handleContextMenuAction(self, row):
        if row == "Heal" and self.pet.is_broken:
            self.pet.fix()

        elif row == "Attack":
            self.pet.attacking = True
            self.pet.get_world().attacking = True

        elif row == "Choose Target":
            self.attack(self)

        elif row == "Cancel":
            self.pet.attacking = False
            self.pet.get_world().reset_attacking()

        elif row == "Move":
            self.pet.moving = True
            self.pet.get_world().moving = True


    def attack(self, target):
        """

        Attacks the target pet.

        """
        target.pet.set_health(target.pet.get_health() - self.pet.strength)
        if target.pet.get_health() < 0:
            target.pet.set_health(0)
        self.pet.attacking = False
        self.pet.get_world().reset_attacking()

