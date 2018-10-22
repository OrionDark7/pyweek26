import pygame, random
from structures import *
from entities import *

#ROAD PARAMATERS: Position and Orientation

#CAR PARAMETERS: Position and Orientation

def level(level):
    roads = pygame.sprite.Group()
    cars = pygame.sprite.Group()
    lights = pygame.sprite.Group()
    intersections = pygame.sprite.Group()
    buildings = pygame.sprite.Group()
    objectives = {}
    if level == 0:
        objectives = {"objective": "cars", "amount": 99, "time": 10, "tod": 14}
        roads.add(road([470, 0], "vertical"))
    if level == 1:
        objectives = {"objective": "cars", "amount": 10, "time": 180, "tod": 10}
        roads.add(road([370, 0], "vertical"))
        roads.add(road([0, 370], "horizontal"))
        lights.add(light([370, 310], "vertical", True, 1))
        lights.add(light([370, 430], "vertical", True, -1))
        lights.add(light([310, 370], "horizontal", True, 1))
        lights.add(light([430, 370], "horizontal", True, -1))
        roads.add(road([0, 170], "horizontal"))
        lights.add(light([370, 110], "vertical", True, 1))
        lights.add(light([370, 230], "vertical", True, -1))
        lights.add(light([310, 170], "horizontal", True, 1))
        lights.add(light([430, 170], "horizontal", True, -1))
        intersections.add(intersection([370, 370]))
        intersections.add(intersection([370, 170]))

    return roads, cars, lights, intersections, buildings, objectives