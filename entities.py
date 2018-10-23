import pygame, random

class car(pygame.sprite.Sprite):
    def __init__(self, pos, orientation, direction, group):
        pygame.sprite.Sprite.__init__(self)
        self.color = random.choice(["red", "blue", "van", "taxi", "police"])
        imagefiles = ["./images/cars/" + self.color + "/car-left.png", None, "./images/cars/" + self.color + "/car-right.png"]
        imagefiles2 = ["./images/cars/" + self.color + "/car-up.png", None, "./images/cars/" + self.color + "/car-down.png"]
        self.headlightfiles = ["./images/cars/headlights/h1.png", "./images/cars/headlights/h2.png", "./images/cars/headlights/h3.png", "./images/cars/headlights/h4.png"]
        self.imagev = pygame.surface.Surface([20, 40])
        self.imageh = pygame.surface.Surface([40, 20])
        self.imagevc = pygame.surface.Surface([20, 50])
        self.imagehc = pygame.surface.Surface([50, 20])
        self.imagev.fill([255, 0, 0])
        self.imageh.fill([255, 0, 0])
        self.rectv = self.imagev.get_rect()
        self.recth = self.imageh.get_rect()
        self.rectvc = self.imagevc.get_rect()
        self.recthc = self.imagehc.get_rect()
        self.rectc = None
        self.image = None
        self.rect = None
        self.speed = 1
        self.acceleration = 0
        self.stopped = False
        self.crashed = False
        self.route = []
        self.direction = direction
        if orientation == "vertical":
            self.image = pygame.image.load(imagefiles2[direction + 1])
            self.rect = self.rectv
            self.orientation = "v"
        elif orientation == "horizontal":
            self.image = pygame.image.load(imagefiles[direction + 1])
            self.rect = self.recth
            self.orientation = "h"
        self.rect.left, self.rect.top = list(pos)
        if direction == 1:
            self.rectvc.left, self.rectvc.top = pos[0], pos[1] - 10
            self.recthc.left, self.recthc.top = pos[0] - 10, pos[1]
        elif direction == -1:
            self.rectvc.left, self.rectvc.top = pos[0], pos[1]
            self.recthc.left, self.recthc.top = pos[0], pos[1]
        else:
            self.rectvc.left, self.rectvc.top = pos[0], pos[1] - 10
            self.recthc.left, self.recthc.top = pos[0] - 10, pos[1]
        if orientation == "vertical":
            self.rectc = self.rectvc
        elif orientation == "horizontal":
            self.rectc = self.recthc

        if self.orientation == "h":
            if self.direction == 1:
                self.headlight = pygame.image.load(self.headlightfiles[1])
                self.headlight.set_alpha(00)
            elif self.direction == -1:
                self.headlight = pygame.image.load(self.headlightfiles[3])
                self.headlight.set_alpha(00)
        elif self.orientation == "v":
            if self.direction == 1:
                self.headlight = pygame.image.load(self.headlightfiles[2])
                self.headlight.set_alpha(00)
            elif self.direction == -1:
                self.headlight = pygame.image.load(self.headlightfiles[0])
                self.headlight.set_alpha(00)

    def stop(self):
        self.acceleration = 0
        self.speed = 0

    def drive(self, accel):
        #determine the directon

        if self.direction == 0:
            self.direction = random.choice([-1, 1])

        #accelerate

        if accel:

            if self.acceleration < 2 and self.acceleration != 0:
                self.acceleration = self.acceleration * 2

            if self.acceleration == 0:
                self.acceleration = 1

        #speed = direction(speed + acceleration)

        if self.speed < 6 and self.speed > -6:
            self.speed = (self.speed + self.acceleration)
            self.speed = self.speed * self.direction
        if self.speed > 6:
            self.speed = 6
        if self.speed < -6:
            self.speed = -6

        #move car + speed

        if self.orientation == "h":
            self.rect.centerx += self.speed
            self.rectc.centerx += self.speed
        elif self.orientation == "v":
            self.rect.centery += self.speed
            self.rectc.centery += self.speed

    def checkcrash(self, group, mouse):
        if not self.crashed:
            self.kill()

            for i in group:
                if self.orientation == i.orientation and self.rect.colliderect(i.rectc):
                    self.stopped = True
                    self.stop()

            if pygame.sprite.spritecollide(self, group, False) and self.rect.centerx > 0 and self.rect.centerx < 800 and self.rect.centery > 0 and self.rect.centery < 600:
                self.stopped = True
                self.crashed = True
                self.stop()
                mouse.accident = True
                mouse.accidentinfo = [self.rect.centerx, self.rect.centery]
                mouse.accidents += 0.5
                if mouse.objective["objective"] == "crashes" and mouse.objective["amount"] > 0:
                    mouse.objective["amount"] -= 0.5

            group.add(self)

    def checktraffic(self, light):

        self.stopped = False

        if pygame.sprite.spritecollide(self, light, False):
            for l in light:
                if not l.light and self.rect.colliderect(l.rect) and l.lightpos == self.direction:
                    self.stopped = True
                    self.stop()

    def update(self, action, cars, mouse, lights, screen):
        if self.rect.bottom < 0 or self.rect.top > 600 or self.rect.left < 0 or self.rect.right > 800:
            self.kill()
            mouse.score += 1
            if mouse.objective["objective"] == "cars" and mouse.objective["amount"] > 0:
                mouse.objective["amount"] -= 1
        if self.stopped == False:
            if action == "drive":
                self.drive(False)
            if action == "accel":
                self.drive(True)
        if action == "crash":
            self.checkcrash(cars, mouse)
        if action == "traffic" and not self.crashed:
            self.checktraffic(lights)
        if action == "kill" and self.rect.collidepoint([mouse.rect.centerx, mouse.rect.centery]):
            print "eh"
            self.kill()
        if action == "draw":
            if mouse.objective["tod"] < 6 or mouse.objective["tod"] > 15 and not self.crashed:
                if self.orientation == "h":
                    if self.direction == 1:
                        screen.blit(self.headlight, [self.rect.left + 35, self.rect.top])
                    elif self.direction == -1:
                        screen.blit(self.headlight, [self.rect.left - 15 , self.rect.top])
                elif self.orientation == "v":
                    if self.direction == 1:
                        screen.blit(self.headlight, [self.rect.left, self.rect.top + 35])
                    elif self.direction == -1:
                        screen.blit(self.headlight, [self.rect.left, self.rect.top - 15])
            screen.blit(self.image, [self.rect.left, self.rect.top])
        if action == "stop":
            self.stop()
            self.stopped = True
        if action == "collidepoint":
            if (self.rect.left < 60 and self.rect.top == mouse.collidepoint[1]) or (self.rect.right > 740 and self.rect.top == mouse.collidepoint[1]) or (self.rect.top < 60 and self.rect.left == mouse.collidepoint[0]) or (self.rect.bottom > 540 and self.rect.left == mouse.collidepoint[0]):
                mouse.collide = True