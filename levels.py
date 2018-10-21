import pygame, random
from structures import *
from entities import *

#ROAD PARAMATERS: Position and Orientation

#CAR PARAMETERS: Position and Orientation

def level(level):
    roads = pygame.sprite.Group()
    cars = pygame.sprite.Group()
    lights = pygame.sprite.Group()
    if level == 0:
        roads.add(road([370, 0], "vertical"))
        roads.add(road([0, 270], "horizontal"))
        lights.add(light([370, 210], "vertical", True, 1))
        lights.add(light([370, 330], "vertical", True, -1))
        lights.add(light([310, 270], "horizontal", True, 1))
        lights.add(light([430, 270], "horizontal", True, -1))
        cars.add(car([376, 0], "vertical", -1, cars))
        cars.add(car([0, 276], "horizontal", 1, cars))
    return roads, cars, lights