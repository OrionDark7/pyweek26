import pygame, random
from structures import *
from entities import *

#ROAD PARAMATERS: Position and Orientation

#CAR PARAMETERS: Position and Orientation

def level(level):
    roads = pygame.sprite.Group()
    cars = pygame.sprite.Group()
    if level == 0:
        roads.add(road([370, 0], "vertical"))
        roads.add(road([0, 270], "horizontal"))
        cars.add(car([376, 0], "vertical"))
        cars.add(car([0, 276], "horizontal"))
    return roads, cars