import pygame, random
import entities

class road(pygame.sprite.Sprite):
    def __init__(self, pos, orientation):
        pygame.sprite.Sprite.__init__(self)
        self.orientation = orientation
        if orientation == "vertical":
            self.image = pygame.surface.Surface([60, 600])
            print self.image, pos
        elif orientation == "horizontal":
            self.image = pygame.surface.Surface([800, 60])
            print self.image, pos
        self.image.fill([0, 0, 0])
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(pos)
        print self.rect.left, self.rect.top

def generate_roads(roads):
    roadg = pygame.sprite.Group()
    carg  = pygame.sprite.Group()
    for i in range(roads):
        orientation = random.choice(["vertical", "horizontal"])
        if orientation == "vertical":
            pos = ((random.randint(0, 11) * 60) + 10, 0)
            newroad = road(pos, "vertical")
            newcar = entities.car((pos[0] + 6, pos[1]), "vertical")
        elif orientation == "horizontal":
            pos = (0, (random.randint(0, 8) * 60) + 10)
            newroad = road(pos, "horizontal")
            newcar = entities.car((pos[0], pos[1] + 6), "horizontal")
        roadg.add(newroad)
        carg.add(newcar)
    return roadg, carg