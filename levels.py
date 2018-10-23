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
    if level == "freeplay":
        objectives = {"objective": "freeplay", "amount": "freeplay", "time": "freeplay", "tod": 6}
        roads.add(road([170, 0], "vertical"))
        roads.add(road([570, 0], "vertical"))
        roads.add(road([0, 170], "horizontal"))
        roads.add(road([0, 370], "horizontal"))
        intersections.add(intersection([170, 170]))
        intersections.add(intersection([570, 170]))
        intersections.add(intersection([170, 370]))
        intersections.add(intersection([570, 370]))
        lights.add(light([170, 310], "vertical", False, 1))
        lights.add(light([170, 430], "vertical", False, -1))
        lights.add(light([110, 370], "horizontal", False, 1))
        lights.add(light([230, 370], "horizontal", False, -1))
        lights.add(light([570, 310], "vertical", False, 1))
        lights.add(light([570, 430], "vertical", False, -1))
        lights.add(light([510, 370], "horizontal", False, 1))
        lights.add(light([630, 370], "horizontal", False, -1))
        #up
        lights.add(light([170, 110], "vertical", False, 1))
        lights.add(light([170, 230], "vertical", False, -1))
        lights.add(light([110, 170], "horizontal", False, 1))
        lights.add(light([230, 170], "horizontal", False, -1))
        lights.add(light([570, 110], "vertical", False, 1))
        lights.add(light([570, 230], "vertical", False, -1))
        lights.add(light([510, 170], "horizontal", False, 1))
        lights.add(light([630, 170], "horizontal", False, -1))
    if level == "survival":
        objectives = {"objective": "survival", "amount": "survival", "time": 0, "tod": 6}
        roads.add(road([170, 0], "vertical"))
        roads.add(road([570, 0], "vertical"))
        roads.add(road([0, 170], "horizontal"))
        roads.add(road([0, 370], "horizontal"))
        intersections.add(intersection([170, 170]))
        intersections.add(intersection([570, 170]))
        intersections.add(intersection([170, 370]))
        intersections.add(intersection([570, 370]))
        lights.add(light([170, 310], "vertical", False, 1))
        lights.add(light([170, 430], "vertical", False, -1))
        lights.add(light([110, 370], "horizontal", False, 1))
        lights.add(light([230, 370], "horizontal", False, -1))
        lights.add(light([570, 310], "vertical", False, 1))
        lights.add(light([570, 430], "vertical", False, -1))
        lights.add(light([510, 370], "horizontal", False, 1))
        lights.add(light([630, 370], "horizontal", False, -1))
        # up
        lights.add(light([170, 110], "vertical", False, 1))
        lights.add(light([170, 230], "vertical", False, -1))
        lights.add(light([110, 170], "horizontal", False, 1))
        lights.add(light([230, 170], "horizontal", False, -1))
        lights.add(light([570, 110], "vertical", False, 1))
        lights.add(light([570, 230], "vertical", False, -1))
        lights.add(light([510, 170], "horizontal", False, 1))
        lights.add(light([630, 170], "horizontal", False, -1))
    if level == 0:
        objectives = {"objective": "cars", "amount": 99, "time": 10, "tod": 14}
        roads.add(road([470, 0], "vertical"))
    if level == 1:
        objectives = {"objective": "cars", "amount": 10, "time": 60, "tod": 10}
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