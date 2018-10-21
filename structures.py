import pygame, random
import entities

class road(pygame.sprite.Sprite):
    def __init__(self, pos, orientation):
        pygame.sprite.Sprite.__init__(self)
        self.type = "road"
        self.orientation = orientation
        if orientation == "vertical":
            self.image = pygame.image.load("./images/roads/road-vertical.png")
        elif orientation == "horizontal":
            self.image = pygame.image.load("./images/roads/road-horizontal.png")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(pos)

class intersection(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.type = "intersection"
        self.image = pygame.image.load("./images/roads/intersection.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(pos)

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
        self.light = light
        if self.light:
            if self.orientation == "vertical":
                if self.lightpos == 1:  # bottom
                    self.image = pygame.image.load("./images/lights/down/light-down-green.png")
                else:  # top
                    self.image = pygame.image.load("./images/lights/down/light-down-green.png")
            elif self.orientation == "horizontal":
                if self.lightpos == 1:  # right
                    self.image = pygame.image.load("./images/lights/left/light-left-green.png")
                else:  # left
                    self.image = pygame.image.load("./images/lights/right/light-right-green.png")
        elif not self.light:
            if self.orientation == "vertical":
                if self.lightpos == 1:  # bottom
                    self.image = pygame.image.load("./images/lights/down/light-down-red.png")
                else:  # top
                    self.image = pygame.image.load("./images/lights/down/light-down-red.png")
            elif self.orientation == "horizontal":
                if self.lightpos == 1:  # right
                    self.image = pygame.image.load("./images/lights/left/light-left-red.png")
                else:  # left
                    self.image = pygame.image.load("./images/lights/right/light-right-red.png")
    def update(self, action, screen, mouse):
        if action == "toggle" and self.irect.collidepoint([mouse.rect.centerx, mouse.rect.centery]):
            self.light = not self.light
            print self.light
            if self.light:
                if self.orientation == "vertical":
                    if self.lightpos == 1:  # bottom
                        self.image = pygame.image.load("./images/lights/down/light-down-green.png")
                    else:  # top
                        self.image = pygame.image.load("./images/lights/down/light-down-green.png")
                elif self.orientation == "horizontal":
                    if self.lightpos == 1:  # right
                        self.image = pygame.image.load("./images/lights/left/light-left-green.png")
                    else:  # left
                        self.image = pygame.image.load("./images/lights/right/light-right-green.png")
            elif not self.light:
                if self.orientation == "vertical":
                    if self.lightpos == 1:  # bottom
                        self.image = pygame.image.load("./images/lights/down/light-down-red.png")
                    else:  # top
                        self.image = pygame.image.load("./images/lights/down/light-down-red.png")
                elif self.orientation == "horizontal":
                    if self.lightpos == 1:  # right
                        self.image = pygame.image.load("./images/lights/left/light-left-red.png")
                    else:  # left
                        self.image = pygame.image.load("./images/lights/right/light-right-red.png")
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