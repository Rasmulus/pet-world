from direction import Direction
import sys
sys.setrecursionlimit(10000) # or some other large value

class Pet():
    """
    The class Pet represents pets which inhabit two
    dimensional grid worlds.
    """

    def __init__(self, name):
        """
        Creates a new pet with the given name.
        """
        self.name = name
        self.world = None        # fixed value
        self.location = None     # most-recent holder
        self.destroyed = False   # flag
        self.brain = None        # most-recent holder
        self.facing = None       # most-recent holder
        self.max_health = 100
        self.health = self.max_health
        self.max_mana = 20
        self.mana = self.max_mana
        self.strength = 50
        self.armour = 0
        self.attacking = False
        self.heavy_attacking = False
        self.moving = False
        self.range = 3
        self.att_range = 1
        self.team = "Blue"
        self.moved = False
        self.attacked = False
        self.flying = False
        self.breaking = False
        self.class_name = "Pet"


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
        current_square = self.get_location_square()
        current_square.remove_robot()

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
        Places the pet in the given pet world at the specified
        coordinates.
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
        Turns the robot in the specified direction.
        """
        self.facing = new_facing

    def move_to(self, target):
        current_square = self.get_location_square()
        target_square = self.get_world().get_square(target)

        tuple_result = tuple(map(int, str(target).strip("()").split(",")))
        if tuple_result in self.get_possible_moves():
            current_square.remove_robot()
            self.location = target
            target_square.set_robot(self)
            self.moved = True
            return True



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
            current_square = self.get_location_square()
            current_square.remove_robot()
            self.get_world().robots.remove(self)

    def get_mana(self):
        return self.mana
    def get_attack_state(self):
        return self.attacking

    def get_moving_state(self):
        return self.moving

    def get_possible_moves(self, x=None, y=None, r=None, obstacles=None):
        if x is None:
            x = self.get_location().get_x()
        if y is None:
            y = self.get_location().get_y()
        if r is None:
            r = self.range
        if obstacles is None:
            obstacles = self.get_world().obstacles

        # Base case: character can't move
        if r == 0:
            return [(x, y)]

        if self.flying:
            # Generate all possible moves based on directions and range
            moves = []
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    # Check if new position is within range
                    if abs(dx) + abs(dy) <= r:
                        new_x, new_y = x + dx, y + dy
                        # Add new position to possible moves if inside game bounds
                        if 0 <= new_x < self.world.width and 0 <= new_y < self.world.height:
                            moves.append((new_x, new_y))

        else:
            # Generate all possible moves based on directions
            moves = []
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for d in directions:
                new_x, new_y = min(max(0, x + d[0]), self.world.width - 1), min(max(0, y + d[1]), self.world.height - 1)
                distance = abs(d[0]) + abs(d[1])
                # Check if new position is not an obstacle
                if (new_x, new_y) not in obstacles:
                    # Recursively find possible moves from new position
                    possible_moves = self.get_possible_moves(new_x, new_y, r - distance, obstacles)
                    # Check if new position is within range
                    if distance <= r:
                        moves += possible_moves

        # Add the current position if it is within range and inside game bounds
        if r >= 0:
            moves.append((x, y))

        # Remove duplicates
        moves = list(set(moves))

        return moves

    def distance_count(self, target):
        """
        Calculates the distance between a pet and a target.
        """


        current_square = self.get_location()
        current_x = current_square.get_x()
        current_y = current_square.get_y()
        target_x = target.get_x()
        target_y = target.get_y()

        x_difference = current_x - target_x
        if x_difference < 0:
            x_difference = x_difference / -1

        y_difference = current_y - target_y
        if y_difference < 0:
            y_difference = y_difference / -1

        return x_difference + y_difference

    def change_team(self):
        if self.team == "Blue":
            self.team = "Red"
            self.spin((0, 1))
        else:
            self.team = "Blue"
            self.spin((0, -1))


    def __str__(self):
        return self.get_name() + ' at location ' + str(self.get_location())
