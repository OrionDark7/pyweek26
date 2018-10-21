import pygame, random

class car(pygame.sprite.Sprite):
    def __init__(self, pos, orientation, direction, group):
        pygame.sprite.Sprite.__init__(self)
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
            self.image = self.imagev
            self.rect = self.rectv
            self.orientation = "v"
        elif orientation == "horizontal":
            self.image = self.imageh
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

        if pygame.sprite.spritecollide(self, group, False):
            self.kill()

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
                self.acceleration = self.acceleration + 0.1

            if self.acceleration == 0:
                self.acceleration = 1

        #speed = direction(speed + acceleration)

        if self.speed < 3:
            self.speed = self.direction * (self.speed + self.acceleration)

        #move car + speed

        if self.orientation == "h":
            self.rect.centerx += self.speed
            self.rectc.centerx += self.speed
        elif self.orientation == "v":
            self.rect.centery += self.speed
            self.rectc.centery += self.speed

    def checkcrash(self, group):
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
                print "Car Crashed!" + str([self.rect.centerx, self.rect.centery])

            group.add(self)

    def checktraffic(self, light):

        self.stopped = False

        if pygame.sprite.spritecollide(self, light, False):
            for l in light:
                if not l.light and self.rect.colliderect(l.rect) and l.lightpos == self.direction:
                    self.stopped = True
                    self.stop()

    def update(self, action, cars, mouse, lights):
        if self.rect.bottom < 0 or self.rect.top > 600 or self.rect.left < 0 or self.rect.right > 800:
            self.kill()
        if self.stopped == False:
            if action == "drive":
                self.drive(False)
            if action == "accel":
                self.drive(True)
        if action == "crash":
            self.checkcrash(cars)
        if action == "traffic" and not self.crashed:
            self.checktraffic(lights)
        if action == "kill" and self.rect.collidepoint(mouse):
            print "eh"
            self.kill()
