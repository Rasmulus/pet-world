from direction import Direction


class Pet():
    """
    The class Pet represents robots (or "bots") which inhabit two
    dimensional grid worlds. More specifically, each instance of the class represents
    a "robot body" (or "chassis" or "hardware") and basic functionality of such a robot.
    Each "robot body" is associated with a "robot brain" that controls the body
    and determines what functionality is activated and when.

    A robot is equipped with the various capabilities:

     - It can sense its own surroundings (location, facing, the world that it is in).

     - It can move forward.

     - It can spin around in any one of the four main compass directions.

     - It can sense whether it is broken or not, and whether it is "stuck" in a square
        between four walls.

    When a robot's take_turn() method is called, it uses its "brain" to figure
    out what to do (move, turn about, etc.). Robots with different kinds of brains behave
    differently.

    See the documentation of PetWorld and PetBrain.
    """

    def __init__(self, name):
        """
        Creates a new robot with the given name. The newly
        created robot is initially just a "dumb shell" until
        it's given a brain later using the method
        set_brain().

        If the given name is None or an empty
        string, the name is set to "Incognito".

        Parameter name is the name of the bot: string

        See set_brain(PetBrain)
        """
        self.set_name(name)
        self.world = None        # fixed value
        self.location = None     # most-recent holder
        self.destroyed = False   # flag
        self.brain = None        # most-recent holder
        self.facing = None       # most-recent holder
        self.health = 100
        self.strength = 10
        self.attacking = False


    def set_name(self, name):
        """
        Sets the name of the robot.
        If the given name is None or an empty
        string, the name is set to "Incognito".

        Parameter name is the new name of the robot: string
        """
        if not name:
            self.name = "Incognito"   # most-recent holder
        else:
            self.name = name


    def get_name(self):
        """
        Returns the robot name : string
        """
        return self.name


    def set_brain(self, new_brain):
        """
        Sets a "brain" (or AI) for the robot (replacing any brain
        previously set, if any): spinbot, lovebot, drunkbot, ...

        Parameter new_brain is the artificial intelligence that controls the robot: spinbot/lovebot/drunkbot/... object
        """
        self.brain = new_brain


    def get_brain(self):
        """
        Returns the "brain" (or AI) of the robot: spinbot/lovebot/drunkbot/... object
        """
        return self.brain


    def get_world(self):
        """
        Returns the world in which the bot is, or None if the robot has not been placed in any robot world: PetWorld
        """
        return self.world


    def get_location(self):
        """
        Returns the current location of the robot in the robot world, or None if the robot has not been placed in any robot world: Coordinates

        See get_location_square()
        """
        return self.location


    def get_location_square(self):
        """
        Returns the square that the robot is in: Square

        See get_location()
        """
        return self.get_world().get_square(self.get_location())


    def get_facing(self):
        """
        Returns the direction the robot is facing: tuple

        """
        return self.facing


    def destroy(self):
        """
        Breaks the robot, rendering it unoperational.

        See fix() and take_turn()
        """
        self.destroyed = True
        self.health = 0


    def fix(self):
        """
        Fixes the robot.

        See destroy()
        """
        self.destroyed = False
        self.health = 100


    def is_broken(self):
        """
        Determines whether the robot is broken or not. A robot is broken
        if it has been broken with the method destroy() and
        not fixed since, or if it is lacking a brain.

        Returns the boolean value which states whether the bot is broken: boolean
        """
        return self.destroyed or self.get_brain() is None


    def is_stuck(self):
        """
        Determines whether the robot is stuck or not, i.e., are there any
        squares that the robot could move into.  This is done by
        examining the four adjacent squares (diagonally adjacent squares are
        not considered). If there is a wall in all directions, the robot is
        considered stuck. Also, if the robot has not yet been placed in any
        robot world, it is considered to be stuck.

        Returns a boolean value that states whether the bot is stuck or not: boolean

        See take_turn()
        """
        world = self.get_world()
        if world is None:
            return True

        for value in Direction.get_values():          # most-recent holder
            if not world.get_square(self.get_location().get_neighbor(value)).is_wall_square():
                return False
        return True


    def set_world(self, world,  location,  facing):
        """
        Places the robot in the given robot world at the specified
        coordinates.  Note! This method is supposed to be used from the
        addRobot method in the PetWorld class,
        which makes sure that the robot is appropriately recorded as
        being part of the robot world.

        Parameter world is the robot world in which the bot is placed: PetWorld

        Parameter location is the coordinates at which the bot is placed: Coordinates

        Parameter facing is the direction the robot is facing initially : tuple

        Returns False if the square at the given location is not empty or the robot is already located in some world (the given one or some other world), True otherwise: boolean

        See PetWorld.add_robot(Pet, Coordinates, Direction)
        """
        target_square = world.get_square(location)
        if not target_square.is_empty() or self.get_world() is not None:
            return False
        else:
            self.world = world
            self.location = location
            self.facing = facing
            return True


    def spin(self, new_facing):
        """
        Turns the robot in the specified direction, if the
        robot is intact. If the robot is broken, the method does nothing.

        Parameter new_facing is the new facing direction of the robot: tuple
        """
        if not self.is_broken():
            self.facing = new_facing


    def move(self, direction):
        """
        Changes the place of the robot within its current world
        from the current square to the square next to it in the
        given direction. The direction does not necessarily have
        to be the same one that the robot is originally facing in.
        This method changes the robot to face the direction it
        moves in. A broken robot can't move.

        Two robots can never be in the same square, neither can
        a robot and a wall. If the square at the given coordinates
        is not empty, a collision occurs instead and the robot
        does not move (but still turns to face whatever it collided
        with). If the moving robot collides with a wall,
        the robot itself breaks. If a moving robot collides with
        another robot, the other robot breaks and the moving robot
        stays intact.

        Parameter direction is the direction to move in: tuple

        Returns a boolean value indicating if the movement was successful (False means that either the robot was broken to begin with or that it collided with something instead of successfully moving): boolean
        """
        if self.is_broken():
            return False

        target = self.get_location().get_neighbor(direction)
        current_square = self.get_location_square()
        target_square = self.get_world().get_square(target)
        self.spin(direction)
        if target_square.is_empty():
            current_square.remove_robot()
            self.location = target
            target_square.set_robot(self)
            return True
        elif target_square.get_robot() is not None:
            target_square.get_robot().destroy()
            return False
        else:   # collided with wall
            self.destroy()
            return False


    def move_forward(self):
        """
        Moves the robot forward one square. This is equivalent to calling self.move(self.get_facing()).

        See move(Direction)

        Returns a boolean value indicating if the movement was successful (False means that either the robot was broken to begin with or that it collided with something instead of successfully moving): boolean
        """
        return self.move(self.get_facing())


    def take_turn(self):
        """
        Gives the robot a turn to act. An unstuck, unbroken robot, however, consults its brain to
        find out what to do. This is done by calling the brain's method move_body().
        Here is a general outline of what happens during a robot's turn:
         1. The robot checks its sensors to see if it is stuck or broken. (If it is, it doesn't do anything.)
         2. If not, it call's it's brain's move_body() method, leaving it up to the brain to decide
            what happens next.
         3. The move_body() method will then determine how the robot behaves, usually calling
            various methods of the robot's body (i.e., the Pet object whose turn it is),
            e.g. move, spin. However, it is not up to the Pet object
            to decide which of its methods get called - that depends on the implementation of the robot's brain.

        See is_broken()

        See is_stuck()

        See PetBrain.move_body()
        """
        if not self.is_stuck() and not self.is_broken():
            self.brain.move_body()

    def get_health(self):
        if self.is_broken():
            return 0
        return self.health

    def set_health(self, value):
        self.health = value
        if self.health < 0:
            self.health = 0
        if self.health == 0:
            self.destroy()
    def get_attack_state(self):
        return self.attacking


    def __str__(self):
        return self.get_name() + ' at location ' + str(self.get_location())
