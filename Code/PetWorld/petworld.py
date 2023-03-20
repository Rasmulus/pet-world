from square import Square


class PetWorld():
    """
    The class PetWorld describes a two dimensional world made up
    of squares that different kinds of robots can inhabit. The squares are
    identified by unique coordinates which range from 0...width-1 and
    0...height-1. Each square is represented by a Square object.

    Robots can be added to the robot world, and the robot world
    maintains a robot listing which allows robots to take their turns in
    a round-robin fashion, in the order in which they were added.
    Each robot is represented by a Pet object.

    See the documentation Pet, Square, Coordinates
    """

    def __init__ (self, width, height):
        """
        Creates a new robot world with the specified dimensions.
        Initially all the squares of the new world are empty.

        Parameter width is the width of the world in squares: int

        Parameter height is the height of the world in squares: int
        """
        self.squares = [None] * width
        for x in range(self.get_width()):      # stepper
            self.squares[x] = [None] * height
            for y in range(self.get_height()):    # stepper
                self.squares[x][y] = Square()    # fixed value
        self.robots = []                        # container
        self.turn = 0                         # kinda like stepper (but not quite) index to robots list
        self.attacking = False
        self.moving = False

    def get_width(self):
        """
        Returns width of the world in squares: int
        """
        return len(self.squares)


    def get_height(self):
        """
        Returns the height of the world in squares: int
        """
        return len(self.squares[0])


    def add_robot(self, robot, location, facing):
        """
        Adds a new robot in the robot world. (Note! This method also
        takes care that the robot is aware if its new position.
        This is done by calling robot's set_world method.)

        Parameter robot is the robot to be added: Pet

        Parameter location is the coordinates of the robot: Coordinates

        Parameter facing is the direction the robot is facing initially : tuple

        Returns False if the square at the given location is not empty or the given robot is already located in some world (this or some other world), True otherwise: boolean

        See Pet.set_world(PetWorld, Coordinates, Direction)
        """
        if robot.set_world(self, location, facing):
            self.robots.append(robot)
            self.get_square(location).set_robot(robot)
            return True
        else:
            return False


    def add_wall(self, location):
        """
        Adds a wall at the given location in the robot world, if
        possible. If the square is not empty, the method fails to
        do anything.

        Parameter location is the location of the wall: Coordinates

        Returns a boolean value indicating if the operation succeeded: boolean
        """
        return self.get_square(location).set_wall()


    def get_square(self, coordinates):
        """
        Parameter coordinates is a location in the world: Coordinates

        Returns the square that is located at the given location. If the given coordinates point outside of the world,
        this method returns a square that contains a wall and is not located in any robot world: Square
        """
        if self.contains(coordinates):
            return self.squares[coordinates.get_x()][coordinates.get_y()]
        else:
            return Square(True)


    def get_number_of_robots(self):
        """
        Returns the number of robots added to this world: int
        """
        return len(self.robots)


    def get_robot(self, turn_number):
        """
        Returns the robot which has the given "turn number".
        The turn numbers of the robots in a world are determined by
        the order in which they were added. I.e., the first robot has
        a turn number of 0, the second one's number is 1, etc.

        Parameter turn_number is the turn number of a robot. Must be on the interval [0, (number of robots minus 1)].: int

        Returns the robot with the given turn number: robot object
        """
        if 0 <= turn_number < self.get_number_of_robots():
            return self.robots[turn_number]
        else:
            return None


    def get_next_robot(self):
        """
        Returns the robot to act next in this world's round-robin turn system, or None if there aren't any robots in the world: Pet

        See next_robot_turn()
        """
        if self.get_number_of_robots() < 1:
            return None
        else:
            return self.robots[self.turn]


    def next_robot_turn(self):
        """
        Lets the next robot take its turn. That is, calls the
        take_turn method of the robot whose turn it is,
        and passes the turn to the next robot. The turn is passed
        to the robot with the next highest turn number (i.e. the one
        that was added to the world after the current robot), or wraps
        back to the first robot (turn number 0) if the last turn number
        was reached. That is to say: the robot which was added first,
        moves first, followed by the one that was added second, etc.,
        until all robots have moved and the cycle starts over.
        If there are no robots in the world, the method does nothing.

        See get_next_robot()
        """
        current = self.get_next_robot()
        if current is not None:
            self.turn = (self.turn + 1) % self.get_number_of_robots()
            current.take_turn()


    def next_full_turn(self):
        """
        Lets each robot take its next turn. That is, calls the next_robot_turn
        a number of times equal to the number of robots in the world.
        """
        for count in range(self.get_number_of_robots()):      # stepper
            self.next_robot_turn()


    def contains(self, coordinates):
        """
        Determines if this world contains the given coordinates.

        Parameter coordinates is a coordinate pair: Coordinates

        Returns a boolean value indicating if this world contains the given coordinates: boolean
        """
        x_coordinate = coordinates.get_x()
        y_coordinate = coordinates.get_y()
        return 0 <= x_coordinate < self.get_width() and 0 <= y_coordinate < self.get_height()


    def get_robots(self):
        """
        Returns an array containing all the robots currently located in this world: list
        """
        return self.robots[:]

    def reset_attacking(self):
        self.attacking = False
        for i in self.get_robots():
            i.attacking = False

    def reset_moving(self):
        self.moving = False
        for i in self.get_robots():
            i.moving = False
