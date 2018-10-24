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
    def __init__(self, pos, orientation, light, id):
        pygame.sprite.Sprite.__init__(self)
        self.orientation = orientation
        self.id = id
        if orientation == "vertical":
            self.image = pygame.surface.Surface([60, 10])
            self.rect = pygame.surface.Surface([60, 100])
        if orientation == "horizontal":
            self.image = pygame.surface.Surface([10, 60])
            self.rect = pygame.surface.Surface([100, 60])
        self.rect = self.rect.get_rect()
        self.rect.left, self.rect.top = list(pos)
        self.irect = self.image.get_rect()
        self.light = light
        if self.light:
            self.image1 = self.image
            self.image1.fill([0, 255, 0])
            self.image2 = self.image
            self.image2.fill([0, 255, 0])
        elif not self.light:
            self.image1 = self.image
            self.image1.fill([255, 0, 0])
            self.image2 = self.image
            self.image2.fill([255, 0, 0])
    def update(self, action, screen, mouse):
        if action == "toggle" and self.rect.collidepoint([mouse.rect.centerx, mouse.rect.centery]):
            self.light = not self.light
            print self.light
            if self.light:
                self.image1 = self.image
                self.image1.fill([0, 255, 0])
                self.image2 = self.image
                self.image2.fill([0, 255, 0])
            elif not self.light:
                self.image1 = self.image
                self.image1.fill([255, 0, 0])
                self.image2 = self.image
                self.image2.fill([255, 0, 0])
        if action == "toggle-id" and self.id == mouse.id:
            self.light = not self.light
            print self.light
            if self.light:
                self.image1 = self.image
                self.image1.fill([0, 255, 0])
                self.image2 = self.image
                self.image2.fill([0, 255, 0])
            elif not self.light:
                self.image1 = self.image
                self.image1.fill([255, 0, 0])
                self.image2 = self.image
                self.image2.fill([255, 0, 0])
        if action == "draw":
            if self.orientation == "vertical":
                screen.blit(self.image1, [self.rect.left, self.rect.top + 10])
                screen.blit(self.image2, [self.rect.left, self.rect.top + 80])
            elif self.orientation == "horizontal":
                screen.blit(self.image1, [self.rect.left + 10, self.rect.top])
                screen.blit(self.image2, [self.rect.left + 80, self.rect.top])

class building(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./images/buildings/" + image + ".png")
        #self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos

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