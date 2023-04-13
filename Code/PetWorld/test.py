import unittest
from PyQt6.QtWidgets import QApplication
from PyQt6 import QtCore

from petworld import PetWorld
from pet import Pet
from coordinates import Coordinates
from direction import Direction
from dog import *
from bird import *
from rodent import *
from cat import *
from reptile import *



class TestLoadGame(unittest.TestCase):

    def test_load_game_obstacles(self):
        game_file = "level_2.ptwrld"
        world = PetWorld(15, 15, "Name", QtCore.QTime(0, 0, 0))
        world.load_game(game_file)
        self.assertEqual(world.obstacles,
                         [(0, 6), (1, 6), (2, 6), (4, 6), (5, 6), (9, 6), (10, 6),
                           (12, 6), (13, 6), (14, 6), (15, 6), (0, 7), (1, 7), (2, 7),
                           (4, 7), (5, 7), (9, 7), (10, 7), (12, 7), (13, 7), (14, 7),
                           (15, 7), (7, 6), (7, 7), (6, 9), (8, 9), (7, 8), (7, 9),
                           (4, 5), (4, 3), (5, 3), (6, 3), (8, 3), (10, 3), (9, 3),
                           (10, 4), (12, 5), (12, 4), (12, 3), (2, 5), (2, 4), (2, 3),
                           (3, 9), (4, 9), (1, 9), (10, 9), (11, 9), (10, 5), (4, 4),
                           (4, 10), (4, 11), (5, 11), (6, 11), (7, 12), (8, 11), (7, 11),
                           (9, 11), (10, 11), (10, 10), (13, 9), (7, 1), (6, 1), (8, 1)])

    def test_load_game_team(self):
        game_file = "level_2.ptwrld"
        world = PetWorld(15, 15, "Name", QtCore.QTime(0, 3, 12))
        world.load_game(game_file)
        self.assertEqual(world.active_team, "Blue")

if __name__ == "__main__":
    unittest.main()
