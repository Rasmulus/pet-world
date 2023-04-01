class Square():
    """
    The class Square represents a single square in a robot world.
    A square can contain either a wall or a robot or it can be empty.
    """

    def __init__(self, is_wall=False):
        """
        Creates a new square. Initially there is no robot in the square.

        Parameter is_wall_square is a boolean value stating whether there is a wall in the square or not: boolean
        """
        self.robot = None     # most-recent holder (None if no robot in square)
        self.is_wall = is_wall  # flag (one-way currently, since walls can not be removed)


    def get_robot(self):
        """
        Returns the robot in the square or None if there is no robot in the square: Pet
        """
        return self.robot


    def is_wall_square(self):
        """
        Returns a boolean value stating whether there is a wall in the square or not: boolean
        """
        return self.is_wall


    def is_empty(self):
        """
        Returns a boolean value stating whether the square is empty (A square is empty if it does not contain a wall or a robot) or not: boolean
        """
        return not self.is_wall_square() and self.robot is None


    def set_robot(self, robot):
        """
        Marks the square as containing a robot, if possible.
        If the square was not empty, the method fails to do anything.

        Parameter robot is the robot to be placed in this square: Pet

        Returns a boolean value indicating if the operation succeeded: boolean
        """
        if self.is_empty():
            self.robot = robot
            return True
        else:
            return False


    def remove_robot(self):
        """
        Removes the robot in this square.

        Returns the robot removed from the square or None, if there was no robot: Pet
        """
        removed_robot = self.get_robot()
        self.robot = None
        return removed_robot


    def set_wall(self):
        """
        Sets a wall in this square, if possible.
        If the square was not empty, the method fails to do anything.

        Returns a boolean value indicating if the operation succeeded: boolean
        """
        if self.is_empty():
            self.is_wall = True
            return True
        else:
            return False

    def remove_wall(self):
        """
        Removes a wall in this square, if possible.
        If the square was empty, the method fails to do anything.

        Returns a boolean value indicating if the operation succeeded: boolean
        """
        if not self.is_empty():
            self.is_wall = False
            return True
        else:
            return False