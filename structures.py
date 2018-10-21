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

class light(pygame.sprite.Sprite):
    def __init__(self, pos, orientation, light, lpos):
        pygame.sprite.Sprite.__init__(self)
        self.orientation = orientation
        if orientation == "vertical":
            self.image = pygame.surface.Surface([60, 10])
            self.rect = pygame.surface.Surface([60, 60])
        if orientation == "horizontal":
            self.image = pygame.surface.Surface([10, 60])
            self.rect = pygame.surface.Surface([60, 60])
        self.rect = self.rect.get_rect()
        self.rect.left, self.rect.top = list(pos)
        self.irect = self.image.get_rect()
        self.lightpos = lpos
        if light:
            self.light = light
            self.image.fill([0, 255, 0])
        elif not light:
            self.light = light
            self.image.fill([255, 0, 0])
    def update(self, action, screen, mouse):
        if action == "toggle" and self.irect.collidepoint(mouse):
            self.light = not self.light
            print self.light
            if self.light:
                self.image.fill([0, 255, 0])
            elif not self.light:
                self.image.fill([255, 0, 0])
        if action == "draw":
            if self.orientation == "vertical":
                if self.lightpos == 1: #bottom
                    screen.blit(self.image, [self.rect.left, self.rect.top + 120])
                    self.irect.left, self.irect.top = self.rect.left, self.rect.top + 120
                else: #top
                    screen.blit(self.image, [self.rect.left, self.rect.top - 70])
                    self.irect.left, self.irect.top = self.rect.left, self.rect.top - 70
            elif self.orientation == "horizontal":
                if self.lightpos == 1: #right
                    screen.blit(self.image, [self.rect.left + 120, self.rect.top])
                    self.irect.left, self.irect.top = self.rect.left + 120, self.rect.top
                else: #left
                    screen.blit(self.image, [self.rect.left - 70, self.rect.top])
                    self.irect.left, self.irect.top = self.rect.left - 70, self.rect.top


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