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
        lights.add(light([170, 150], "vertical", False, 1))
        lights.add(light([570, 150], "vertical", False, 2))
        lights.add(light([150, 170], "horizontal", False, 3))
        lights.add(light([550, 170], "horizontal", False, 4))
        #up
        lights.add(light([170, 350], "vertical", False, 5))
        lights.add(light([570, 350], "vertical", False, 6))
        lights.add(light([150, 370], "horizontal", False, 7))
        lights.add(light([550, 370], "horizontal", False, 8))
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
        lights.add(light([170, 150], "vertical", False, 1))
        lights.add(light([570, 150], "vertical", False, 2))
        lights.add(light([150, 170], "horizontal", False, 3))
        lights.add(light([550, 170], "horizontal", False, 4))
        # up
        lights.add(light([170, 350], "vertical", False, 5))
        lights.add(light([570, 350], "vertical", False, 6))
        lights.add(light([150, 370], "horizontal", False, 7))
        lights.add(light([550, 370], "horizontal", False, 8))
    if level == 0:
        objectives = {"objective": "cars", "amount": 99, "time": 10, "tod": 14}
        roads.add(road([470, 0], "vertical"))
    if level == 1:
        objectives = {"objective": "anger", "amount": 10, "time": 10, "tod": 10}
        roads.add(road([370, 0], "vertical"))
        roads.add(road([0, 370], "horizontal"))
        lights.add(light([370, 350], "vertical", True, 1))
        lights.add(light([370, 150], "vertical", True, 2))
        lights.add(light([350, 370], "horizontal", True, 3))
        lights.add(light([350, 170], "horizontal", True, 4))
        roads.add(road([0, 170], "horizontal"))
        intersections.add(intersection([370, 370]))
        intersections.add(intersection([370, 170]))
    if level == 2:
        objectives = {"objective": "anger", "amount": 10, "time": 180, "tod": 10}

    return roads, cars, lights, intersections, buildings, objectives