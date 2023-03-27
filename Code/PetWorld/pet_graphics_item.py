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

        self.setAcceptHoverEvents(True)

        # Do other stuff
        self.pet = pet
        self.square_size = square_size
        brush = QtGui.QBrush(1) # 1 for even fill
        self.setBrush(brush)
        self.constructTriangleVertices()
        self.health_bar_proxy = self.makeHealthBar()
        self.mana_bar_proxy = self.makeManaBar()
        self.name_tag_proxy = self.makeNameTag()
        self.char_sheet_proxy = self.makeCharSheet()
        self.updateAll()
        self.health_bar_proxy.setVisible(False)
        self.mana_bar_proxy.setVisible(False)
        self.name_tag_proxy.setVisible(False)
        self.char_sheet_proxy.setVisible(False)

    def hide_pet(self):
        self.hide()

    def hoverEnterEvent(self, event):
        self.updateAll()
        self.char_sheet_proxy.setVisible(True)
        self.health_bar_proxy.setVisible(True)
        self.mana_bar_proxy.setVisible(True)
        self.name_tag_proxy.setVisible(True)

    def hoverLeaveEvent(self, event):
        self.char_sheet_proxy.setVisible(False)
        self.health_bar_proxy.setVisible(False)
        self.mana_bar_proxy.setVisible(False)
        self.name_tag_proxy.setVisible(False)


    def makeNameTag(self):
        self.name_tag = QtWidgets.QLabel()
        self.name_tag.setText(f"{self.pet.get_name()}")
        self.name_tag.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.name_tag.setStyleSheet(
            "QLabel { font-size: 16px; font-weight: bold; border: 2px solid black; background-color: beige }")
        self.name_tag.setFixedWidth(self.health_bar.width())
        self.name_tag.setFixedHeight(self.health_bar.height())

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
        offset_x = center_x - self.health_bar_proxy.size().width() / 2
        offset_y = -self.health_bar_proxy.size().height() - 80

        #raise to front
        self.name_tag.raise_()

        # set the position of the proxy widget
        self.name_tag_proxy.setPos(offset_x, offset_y)

        # calculate the rotated offset using a transformation matrix
        transformation = QtGui.QTransform()
        transformation.rotate(-rotation)
        offset = transformation.map(QtCore.QPointF(offset_x, offset_y))

        # set the position of the proxy widget relative to the center point
        self.name_tag_proxy.setPos(center_x + offset.x(), center_y + offset.y())


    def makeCharSheet(self):
        self.char_sheet = QtWidgets.QLabel()
        self.char_sheet.setStyleSheet(
            "QLabel { font-size: 16px; font-weight: bold; border: 2px solid black; background-color: ghostwhite }")
        # raise to front
        self.char_sheet.raise_()

        # make the font size larger
        font = self.char_sheet.font()
        font.setPointSize(font.pointSize() + 5)
        self.char_sheet.setFont(font)

        # create a proxy widget for the character sheet
        char_sheet_proxy = QtWidgets.QGraphicsProxyWidget(self)
        char_sheet_proxy.setWidget(self.char_sheet)

        return char_sheet_proxy

    def updateCharSheet(self):
        """
        Updates the character sheet to follow the location of the parent pet.
        """
        # get the rotation of this item and set the rotation of the proxy widget
        rotation = self.rotation()
        self.char_sheet_proxy.setRotation(-rotation)
        self.char_sheet.setText(f"Name: {self.pet.get_name()}\nTeam: {self.pet.team}\nHealth: {self.pet.health}/{self.pet.max_health}\nMana: {self.pet.mana}/{self.pet.max_mana}\n"
                                f"Movement range: {self.pet.range}\nAttack range: {self.pet.att_range}\nStrength: {self.pet.strength}\nArmour: {self.pet.armour}")
        # calculate the center point of the triangle
        center_x = self.square_size / 2
        center_y = self.square_size / 2

        # calculate the offset for the name tag proxy widget
        offset_x = center_x - 225
        offset_y = -self.char_sheet.height() + 200

        # raise to front
        self.char_sheet.raise_()

        # set the position of the proxy widget
        self.char_sheet_proxy.setPos(offset_x, offset_y)

        # calculate the rotated offset using a transformation matrix
        transformation = QtGui.QTransform()
        transformation.rotate(-rotation)
        offset = transformation.map(QtCore.QPointF(offset_x, offset_y))

        # set the position of the proxy widget relative to the center point
        self.char_sheet_proxy.setPos(center_x + offset.x(), center_y + offset.y())

    def makeHealthBar(self):
        self.health_bar = QtWidgets.QProgressBar()
        self.health_bar.setMaximum(self.pet.max_health)
        self.health_bar.setMinimum(0)
        self.health_bar.setValue(self.pet.get_health())
        self.health_bar.setFormat("%v/%m HP")
        self.health_bar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.health_bar.setStyleSheet(
            "QProgressBar::chunk { background-color: lawngreen } QProgressBar { font-size: 16px; font-weight: bold; border: 2px solid black; }")
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
        self.health_bar.setFormat(f"{self.pet.get_health()}/{self.pet.max_health} HP")
        percentage_left = self.pet.get_health() / self.pet.max_health
        if percentage_left > 0.5:
            self.health_bar.setStyleSheet(
                "QProgressBar::chunk { background-color: lawngreen } QProgressBar { font-size: 16px; font-weight: bold; border: 2px solid black; }")
        elif percentage_left > 0.2:
            self.health_bar.setStyleSheet(
                "QProgressBar::chunk { background-color: orange } QProgressBar { font-size: 16px; font-weight: bold; border: 2px solid black; }")
        else:
            self.health_bar.setStyleSheet(
                "QProgressBar::chunk { background-color: red } QProgressBar { font-size: 16px; font-weight: bold; border: 2px solid black; }")

        # get the rotation of this item and set the rotation of the proxy widget
        rotation = self.rotation()
        self.health_bar_proxy.setRotation(
            -rotation)  # set the rotation of the proxy widget to the negative of this item's rotation
        # calculate the center point of the triangle
        center_x = self.square_size / 2
        center_y = self.square_size / 2

        # raise to front
        self.health_bar.raise_()

        # calculate the offset for the health bar proxy widget
        offset_x = center_x - 100
        offset_y = - 50 - self.health_bar_proxy.size().height()

        # calculate the rotated offset using a transformation matrix
        transformation = QtGui.QTransform()
        transformation.rotate(-rotation)
        offset = transformation.map(QtCore.QPointF(offset_x, offset_y))

        # set the position of the health bar proxy widget relative to the center point
        self.health_bar_proxy.setPos(center_x + offset.x(), center_y + offset.y())

    def makeManaBar(self):
        self.mana_bar = QtWidgets.QProgressBar()
        self.mana_bar.setMaximum(self.pet.max_mana)
        self.mana_bar.setMinimum(0)
        self.mana_bar.setValue(self.pet.get_mana())
        self.mana_bar.setFormat("%v/%m MP")
        self.mana_bar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mana_bar.setStyleSheet(
            "QProgressBar::chunk { background-color: lightskyblue } QProgressBar { font-size: 16px; font-weight: bold; border: 2px solid black; }")

        # create a proxy widget for the progress bar
        self.mana_bar_proxy = QtWidgets.QGraphicsProxyWidget(self)
        self.mana_bar_proxy.setWidget(self.mana_bar)

        #self.health_bar_proxy.setRotation(-self.rotation())

        return self.mana_bar_proxy
    def updateManaBar(self):
        """
        Updates the mana bar to reflect the current mana of the parent pet.
        """
        self.mana_bar.setValue(self.pet.get_mana())
        self.mana_bar.setFormat(f"{self.pet.get_mana()}/{self.pet.max_mana} MP")

        # get the rotation of this item and set the rotation of the proxy widget
        rotation = self.rotation()
        self.mana_bar_proxy.setRotation(
            -rotation)  # set the rotation of the proxy widget to the negative of this item's rotation
        # calculate the center point of the triangle
        center_x = self.square_size / 2
        center_y = self.square_size / 2

        # raise to front
        self.mana_bar.raise_()

        # calculate the offset for the health bar proxy widget
        offset_x = center_x - self.health_bar_proxy.size().width() / 2
        offset_y = -self.health_bar_proxy.size().height() - 20

        # calculate the rotated offset using a transformation matrix
        transformation = QtGui.QTransform()
        transformation.rotate(-rotation)
        offset = transformation.map(QtCore.QPointF(offset_x, offset_y))

        # set the position of the health bar proxy widget relative to the center point
        self.mana_bar_proxy.setPos(center_x + offset.x(), center_y + offset.y())

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
        self.updateCharSheet()
        self.updateManaBar()
        if self.pet.is_broken():
            self.hide_pet()
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
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        self.setBrush(brush)



        if self.pet.team == "Red":
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
            self.setBrush(brush)

        elif not self.pet.team == "Blue":
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))


        if self.pet.is_stuck():
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 0))
            state = "stuck"

        self.setBrush(brush)

    #def updateHealthBar(self):
        #self.health_bar_proxy.setWidget(self.health_bar)




    def mousePressEvent(self, event, *args, **kwargs):
            #Check if attacking
            if not self.pet.team == self.pet.get_world().active_team and self.pet.get_world().attacking:
                target = self.pet
                attacker = None
                print("debug")
                for i in self.pet.get_world().get_robots():
                    print("debug")
                    if i.attacking:
                        attacker = i
                print("debug")
                print("attacker.get_location()")
                distance = self.pet.distance_count(attacker.get_location())    # Calculate distance between the pets

                if attacker.att_range >= distance:  # Checks if target in range
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

            elif not self.pet.get_attack_state() and self.pet.team == self.pet.get_world().active_team:
                menu = QtWidgets.QMenu()
                # make the font size larger
                font = menu.font()
                font.setPointSize(font.pointSize() + 5)
                menu.setFont(font)
                # Create the menu items based on pet status and add them to the menu
                if not self.pet.attacked and not self.pet.moved:
                    if self.pet.get_mana() >= 10:
                        rows = ["Move", "Heavy Attack (10 MP)", "Light Attack (5 MP)", "Rest (Restore MP)", "Heal"]
                    elif self.pet.get_mana() >= 5:
                        rows = ["Move", "Light Attack (5 MP)", "Rest (Restore MP)", "Heal"]
                    else:
                        rows = ["Move", "Rest (Restore MP)", "Heal"]
                elif not self.pet.attacked and self.pet.moved:
                    if self.pet.get_mana() >= 10:
                        rows = ["Heavy Attack (10 MP)", "Light Attack (5 MP)", "Heal"]
                    elif self.pet.get_mana() >= 5:
                        rows = ["Light Attack (5 MP)", "Heal"]
                    else:
                        rows = ["Heal"]

                elif not self.pet.moved:
                    rows = ["Move"]
                else:
                    rows = []

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
                self.pet.attacking = False
                self.pet.get_world().reset_attacking()
                self.pet.moving = False
                self.pet.get_world().moving = False

    def handleContextMenuAction(self, row):
        if row == "Heal" and self.pet.is_broken:
            self.pet.fix()
            self.pet.attacked = True

        elif row == "Light Attack (5 MP)":
            self.pet.attacking = True
            self.pet.get_world().attacking = True
            self.pet.mana -= 5

        elif row == "Heavy Attack (10 MP)":
            self.pet.attacking = True
            self.pet.get_world().attacking = True
            self.pet.heavy_attacking = True
            self.pet.mana -= 10

        elif row == "Choose Target":
            self.attack()
            self.pet.get_world().reset_attacking()

        elif row == "Cancel":
            self.pet.attacking = False
            self.pet.get_world().reset_attacking()

        elif row == "Move":
            self.pet.moving = True
            self.pet.get_world().moving = True

        elif row == "Rest (Restore MP)":
            self.pet.attacked = True
            self.pet.moved = True
            self.pet.mana = self.pet.max_mana
    def attack(self):
        """

        Attacks the target pet.

        """

        for i in self.pet.get_world().get_robots():
            if i.attacking == True:
                attacker = i
        if attacker.heavy_attacking:
            self.pet.set_health(self.pet.get_health() - int(attacker.strength * 1.5))
        else:
            self.pet.set_health(self.pet.get_health() - attacker.strength)
        if self.pet.get_health() < 0:
            self.pet.set_health(0)
        for i in self.pet.get_world().get_robots():
            if i.attacking == True:
                i.attacked = True
        print("debug")
        attacker.attacking = False
        attacker.heavy_attacking = False
        attacker.attacked = True
        attacker.get_world().attacking = False
        self.pet.get_world().reset_attacking()




