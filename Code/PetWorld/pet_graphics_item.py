from PyQt6 import QtWidgets, QtGui, QtCore
from pet import Pet
from coordinates import Coordinates

class PetGraphicsItem(QtWidgets.QGraphicsPolygonItem):
    """
    The class PetGraphicsItem extends QGraphicsPolygonItem to link it together to the physical
    representation of a Pet. The QGraphicsPolygonItem handles the drawing, while the
    Pet knows its own location and status.
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
        self.image_label = self.loadCharacterImage()
        self.updateAll()
        self.health_bar_proxy.setVisible(False)
        self.mana_bar_proxy.setVisible(False)
        self.name_tag_proxy.setVisible(False)
        self.char_sheet_proxy.setVisible(False)
        self.setZValue(5)


    def hide_pet(self):
        """
        Hides the pet.
        """
        self.hide()

    def hoverEnterEvent(self, event):
        """
        Sets various UI elements of the pet as visible upon hovering over it.
        """
        if not self.pet.world.moving:
            self.updateAll()
            #self.setZValue(5)
            self.char_sheet_proxy.setVisible(True)
            #self.char_sheet_proxy.setZValue(10)
            self.health_bar_proxy.setVisible(True)
            #self.health_bar_proxy.setZValue(10)
            self.mana_bar_proxy.setVisible(True)
            #self.mana_bar_proxy.setZValue(10)
            self.name_tag_proxy.setVisible(True)
            #self.name_tag_proxy.setZValue(10)

    def hoverLeaveEvent(self, event):
        """
        Sets various UI elements of the pet as hidden upon moving the mouse away from it.
        """
        self.char_sheet_proxy.setVisible(False)
        self.health_bar_proxy.setVisible(False)
        self.mana_bar_proxy.setVisible(False)
        self.name_tag_proxy.setVisible(False)


    def makeNameTag(self):
        """
        Draws a name tag that shows the pet's name.
        """
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
        offset_y = -self.health_bar_proxy.size().height() - 110

        # raise to front
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
        """
        Draws a character sheet that shows critical information about the pet and it's status.
        """
        # create the character sheet
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

    def loadCharacterImage(self):
        """
        Draws the character image of the pet over its triangle.
        """
        # create a label widget to display the image
        self.image_label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(f"assets/{str(self.pet.class_name).lower()}.png")
        pixmap = pixmap.scaled(100, 100, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAutoFillBackground(False)
        self.image_label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # create a proxy widget for the image label
        self.image_label_proxy = QtWidgets.QGraphicsProxyWidget(self)
        self.image_label_proxy.setAutoFillBackground(False)
        self.image_label_proxy.setWidget(self.image_label)

    def updateCharacterImage(self):
        """
        Updates the character image to follow the location of the parent pet.
        """
        # calculate the center point of the triangle
        center_x = self.square_size / 2
        center_y = self.square_size / 2

        # calculate the offset for the character image proxy widget
        offset_x = center_x - 75
        offset_y = center_y - 90

        # get the rotation of this item and set the rotation of the proxy widget
        rotation = self.rotation()
        self.image_label_proxy.setRotation(
            -rotation)  # set the rotation of the proxy widget to the negative of this item's rotation
        # calculate the rotated offset using a transformation matrix
        transformation = QtGui.QTransform()
        transformation.rotate(-rotation)
        offset = transformation.map(QtCore.QPointF(offset_x, offset_y))

        # set the position of the image label proxy widget relative to the center point
        self.image_label_proxy.setPos(center_x + offset.x(), center_y + offset.y())
        #self.image_label.setAutoFillBackground(False)
        self.image_label_proxy.setAutoFillBackground(False)


    def makeHealthBar(self):
        """
        Draws a health bar that shows the current and maximum health of yhe parent pet.
        """
        # create the health bar
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

        return self.health_bar_proxy

    def updateHealthBar(self):
        """
        Updates the health bar to match the health of the parent pet.
        """
        # set the current health to reflect the parent pet's health value
        self.health_bar.setValue(self.pet.get_health())
        self.health_bar.setFormat(f"{self.pet.get_health()}/{self.pet.max_health} HP")
        percentage_left = self.pet.get_health() / self.pet.max_health

        # set the health bar color to reflect the amount of health left
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
        offset_y = - 80 - self.health_bar_proxy.size().height()

        # calculate the rotated offset using a transformation matrix
        transformation = QtGui.QTransform()
        transformation.rotate(-rotation)
        offset = transformation.map(QtCore.QPointF(offset_x, offset_y))

        # set the position of the health bar proxy widget relative to the center point
        self.health_bar_proxy.setPos(center_x + offset.x(), center_y + offset.y())

    def makeManaBar(self):
        """
        Draws a mana bar that shows the current and maximum mana of yhe parent pet.
        """
        # create the mana bar
        self.mana_bar = QtWidgets.QProgressBar()
        self.mana_bar.setMaximum(self.pet.max_mana)
        self.mana_bar.setMinimum(0)
        self.mana_bar.setValue(self.pet.get_mana())
        self.mana_bar.setFormat("%v/%m MP")
        self.mana_bar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mana_bar.setStyleSheet(
            "QProgressBar::chunk { background-color: lightskyblue } QProgressBar { font-size: 16px; font-weight: bold; border: 2px solid black; }")

        # create a proxy widget for the mana bar
        self.mana_bar_proxy = QtWidgets.QGraphicsProxyWidget(self)
        self.mana_bar_proxy.setWidget(self.mana_bar)

        return self.mana_bar_proxy
    def updateManaBar(self):
        """
        Updates the mana bar to reflect the current mana of the parent pet.
        """
        # set the current mana to reflect the parent pet's mana value
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
        offset_y = -self.health_bar_proxy.size().height() - 50

        # calculate the rotated offset using a transformation matrix
        transformation = QtGui.QTransform()
        transformation.rotate(-rotation)
        offset = transformation.map(QtCore.QPointF(offset_x, offset_y))

        # set the position of the health bar proxy widget relative to the center point
        self.mana_bar_proxy.setPos(center_x + offset.x(), center_y + offset.y())

    def constructTriangleVertices(self):
        """
        This method sets the shape of this item into a triangle.
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
        location, direction and status of the parent pet and it's widgets.
        """
        self.updatePosition()
        self.updateRotation()
        self.updateColor()
        self.updateHealthBar()
        self.updateNameTag()
        self.updateCharSheet()
        self.updateManaBar()
        self.updateCharacterImage()
        if self.pet.is_broken():
            self.hide_pet()

    def updatePosition(self):
        """
        Update the coordinates of this item to match the attached pet.
        """

        location = self.pet.get_location()
        x = Coordinates.get_x(location)
        y = Coordinates.get_y(location)
        self.setPos(x * self.square_size, y * self.square_size)


    def updateRotation(self):
        """
        Rotates this item to match the rotation of parent pet.
        """

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
        Draw AI pets in red and player pets in blue.
        """
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        self.setBrush(brush)

        if self.pet.team == "Red":
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
            self.setBrush(brush)

        elif not self.pet.team == "Blue":
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))

        self.setBrush(brush)

    def mousePressEvent(self, event, *args, **kwargs):
        """
        Handles various actions depending on the state of the world, such as drawing context menus.
        """

        # check if level editor
        if self.pet.get_world().active_team == "Level Editor":
            menu = QtWidgets.QMenu()
            # make the font size larger
            font = menu.font()
            font.setPointSize(font.pointSize() + 5)
            menu.setFont(font)
            # create the menu items and add them to the menu
            rows = ["Change Team", "Remove Pet"]
            for row in rows:
                action = QtWidgets.QWidgetAction(menu)
                label = QtWidgets.QLabel(row)
                action.setDefaultWidget(label)
                menu.addAction(action)
                # connect the action to a method that handles it
                action.triggered.connect(lambda checked, row=row: self.handleContextMenuAction(row))
            # show the menu at the position of the event
            menu.exec(event.screenPos())

        # check if attacking
        elif not self.pet.team == self.pet.get_world().active_team and self.pet.get_world().attacking:
            target = self.pet
            attacker = None
            for i in self.pet.get_world().get_robots():
                if i.attacking:
                    attacker = i
            distance = self.pet.distance_count(attacker.get_location())    # Calculate distance between the pets
            percentage_left = target.get_health() / target.max_health

            if attacker.breaking:
                if distance > 1:
                    menu = QtWidgets.QMenu()
                    # make the font size larger
                    font = menu.font()
                    font.setPointSize(font.pointSize() + 5)
                    menu.setFont(font)
                    # create the menu items and add them to the menu
                    rows = ["Target out of Range. Cancel"]
                    for row in rows:
                        action = QtWidgets.QWidgetAction(menu)
                        label = QtWidgets.QLabel(row)
                        action.setDefaultWidget(label)
                        menu.addAction(action)
                        # connect the action to a method that handles it
                        action.triggered.connect(lambda checked, row=row: self.handleContextMenuAction(row))
                    # show the menu at the position of the event
                    menu.exec(event.screenPos())
                elif percentage_left > 0.5:
                    menu = QtWidgets.QMenu()
                    # make the font size larger
                    font = menu.font()
                    font.setPointSize(font.pointSize() + 5)
                    menu.setFont(font)
                    # create the menu items and add them to the menu
                    rows = ["Target not weak enough. Cancel"]
                    for row in rows:
                        action = QtWidgets.QWidgetAction(menu)
                        label = QtWidgets.QLabel(row)
                        action.setDefaultWidget(label)
                        menu.addAction(action)
                        # connect the action to a method that handles it
                        action.triggered.connect(lambda checked, row=row: self.handleContextMenuAction(row))
                    # show the menu at the position of the event
                    menu.exec(event.screenPos())

                else:
                    menu = QtWidgets.QMenu()
                    # make the font size larger
                    font = menu.font()
                    font.setPointSize(font.pointSize() + 5)
                    menu.setFont(font)
                    # create the menu items and add them to the menu
                    rows = ["Free Pet", "Cancel"]
                    for row in rows:
                        action = QtWidgets.QWidgetAction(menu)
                        label = QtWidgets.QLabel(row)
                        action.setDefaultWidget(label)
                        menu.addAction(action)
                        # connect the action to a method that handles it
                        action.triggered.connect(lambda checked, row=row: self.handleContextMenuAction(row))
                    # show the menu at the position of the event
                    menu.exec(event.screenPos())

            elif attacker.att_range >= distance:  # Checks if target in range
                menu = QtWidgets.QMenu()
                # make the font size larger
                font = menu.font()
                font.setPointSize(font.pointSize() + 5)
                menu.setFont(font)
                # create the menu items and add them to the menu
                rows = ["Choose Target", "Cancel"]
                for row in rows:
                    action = QtWidgets.QWidgetAction(menu)
                    label = QtWidgets.QLabel(row)
                    action.setDefaultWidget(label)
                    menu.addAction(action)
                    # connect the action to a method that handles it
                    action.triggered.connect(lambda checked, row=row: self.handleContextMenuAction(row))
                # show the menu at the position of the event
                menu.exec(event.screenPos())

        elif not self.pet.get_attack_state() and self.pet.team == self.pet.get_world().active_team:
            menu = QtWidgets.QMenu()
            # make the font size larger
            font = menu.font()
            font.setPointSize(font.pointSize() + 5)
            menu.setFont(font)
            # create the menu items based on pet status and add them to the menu
            if not self.pet.attacked and not self.pet.moved:
                if self.pet.mana >= 20:
                    rows = ["Move", "Heavy Attack (10 MP)", "Light Attack (5 MP)", "Break Mind Control (20 MP)",
                            "Rest (Restore MP)", "Heal (10 MP)"]
                elif self.pet.get_mana() >= 10:
                    rows = ["Move", "Heavy Attack (10 MP)", "Light Attack (5 MP)", "Rest (Restore MP)", "Heal (10 MP)"]
                elif self.pet.get_mana() >= 5:
                    rows = ["Move", "Light Attack (5 MP)", "Rest (Restore MP)"]
                else:
                    rows = ["Move", "Rest (Restore MP)"]
            elif not self.pet.attacked and self.pet.moved:
                if self.pet.get_mana() >= 10:
                    rows = ["Heavy Attack (10 MP)", "Light Attack (5 MP)", "Heal (10 MP)"]
                elif self.pet.get_mana() >= 5:
                    rows = ["Light Attack (5 MP)"]
                else:
                    rows = []

            elif not self.pet.moved:
                rows = ["Move"]
            else:
                rows = []

            for row in rows:
                action = QtWidgets.QWidgetAction(menu)
                label = QtWidgets.QLabel(row)
                action.setDefaultWidget(label)
                menu.addAction(action)
                # connect the action to a method that handles it
                action.triggered.connect(lambda checked, row=row: self.handleContextMenuAction(row))
            # show the menu at the position of the event
            menu.exec(event.screenPos())
        else:
            self.pet.attacking = False
            self.pet.get_world().reset_attacking()
            self.pet.moving = False
            self.pet.get_world().moving = False

    def handleContextMenuAction(self, row):
        """
        Handles various context menu actions fed to it.
        """
        if row == "Change Team":
            self.pet.change_team()

        elif row == "Remove Pet":
            self.pet.set_health(0)

        elif row == "Heal (10 MP)" and self.pet.is_broken:
            self.pet.fix()
            self.pet.attacked = True
            self.pet.mana -= 10

        elif row == "Light Attack (5 MP)":
            self.pet.attacking = True
            self.pet.get_world().attacking = True

        elif row == "Heavy Attack (10 MP)":
            self.pet.attacking = True
            self.pet.get_world().attacking = True
            self.pet.heavy_attacking = True

        elif row == "Choose Target":
            self.attack()
            self.pet.get_world().reset_attacking()
            self.check_if_won()

        elif row == "Cancel" or row == "Target out of Range. Cancel" or row == "Target not weak enough. Cancel":
            self.pet.attacking = False
            self.pet.get_world().reset_attacking()

        elif row == "Move":
            self.pet.moving = True
            self.pet.get_world().moving = True

        elif row == "Rest (Restore MP)":
            self.pet.attacked = True
            self.pet.moved = True
            self.pet.mana = self.pet.max_mana

        elif row == "Break Mind Control (20 MP)":
            self.pet.attacking = True
            self.pet.get_world().attacking = True
            self.pet.breaking = True

        elif row == "Free Pet":
            self.pet.change_team()
            self.check_if_won()
    def attack(self):
        """
        Attacks the target pet.
        """

        for i in self.pet.get_world().get_robots():
            if i.attacking == True:
                attacker = i
        if attacker.heavy_attacking:
            self.pet.set_health(self.pet.get_health() - int(attacker.strength * 1.5))
            attacker.mana -= 10
        else:
            self.pet.set_health(self.pet.get_health() - attacker.strength)
            attacker.mana -= 5
        if self.pet.get_health() < 0:
            self.pet.set_health(0)
        for i in self.pet.get_world().get_robots():
            if i.attacking == True:
                i.attacked = True
        attacker.attacking = False
        attacker.heavy_attacking = False
        attacker.attacked = True
        attacker.get_world().attacking = False
        self.pet.get_world().reset_attacking()

    def break_control(self):
        """
        Frees the target pet and makes it friendly.
        """
        self.pet.change_team()
        self.pet.get_world().reset_attacking()
        for i in self.pet.world.get_robots():
            if i.breaking:
                i.mana -= 20
                i.moved = True
                i.attacked = True

    def check_if_won(self):
        """
        Checks to see if the game has ended, by iterating through all pets and seeing if there are no friendly or NPC pets left.
        """

        blue_found = False
        red_found = False
        for i in self.pet.world.get_robots():
            if i.team == "Blue":
                blue_found = True
            else:
                red_found = True
        if blue_found == False:
            self.pet.world.won = "Red"
            return True

        elif red_found == False:
            self.pet.world.won = "Blue"
            return True
        else:
            return False







