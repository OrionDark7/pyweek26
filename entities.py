import pygame, random

pygame.init()
pygame.mixer.init()

class car(pygame.sprite.Sprite):
    def __init__(self, pos, orientation, direction, group):
        pygame.sprite.Sprite.__init__(self)
        self.color = random.choice(["red", "blue", "van", "taxi", "police", "green", "hummer"])
        imagefiles = ["./images/cars/" + self.color + "/car-left.png", None, "./images/cars/" + self.color + "/car-right.png"]
        imagefiles2 = ["./images/cars/" + self.color + "/car-up.png", None, "./images/cars/" + self.color + "/car-down.png"]
        self.headlightfiles = ["./images/cars/headlights/h1.png", "./images/cars/headlights/h2.png", "./images/cars/headlights/h3.png", "./images/cars/headlights/h4.png"]
        self.frown = pygame.image.load("./images/frowny.png")
        self.accident = pygame.image.load("./images/accident.png")
        self.horn = pygame.mixer.Sound("./sfx/horn.wav")
        self.crash = pygame.mixer.Sound("./sfx/collision.wav")
        self.imagev = pygame.surface.Surface([20, 40])
        self.imageh = pygame.surface.Surface([40, 20])
        self.imagevc = pygame.surface.Surface([20, 50])
        self.imagehc = pygame.surface.Surface([50, 20])
        self.imagev.fill([255, 0, 0])
        self.imageh.fill([255, 0, 0])
        self.rectv = self.imagev.get_rect()
        self.soundplayed = False
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
        self.time = 0
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

        if self.speed < 4 and self.speed > -4:
            self.speed = (self.speed + self.acceleration)
        if self.speed > 4:
            self.speed = 4
        if self.speed < -4:
            self.speed = -4

        #move car + speed

        if self.orientation == "h":
            if self.direction == -1:
                self.rect.centerx -= self.speed
                self.rectc.centerx -= self.speed
            else:
                self.rect.centerx += self.speed
                self.rectc.centerx += self.speed
        elif self.orientation == "v":
            if self.direction == -1:
                self.rect.centery -= self.speed
                self.rectc.centery -= self.speed
            else:
                self.rect.centery += self.speed
                self.rectc.centery += self.speed

    def checkcrash(self, group, mouse, volume):
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
                self.crash.set_volume(float(volume * 0.1))
                self.crash.play()
                if mouse.objective["objective"] == "crashes" and mouse.objective["amount"] > 0:
                    mouse.objective["amount"] -= 0.5

            group.add(self)

    def checktraffic(self, light):

        self.stopped = False

        if pygame.sprite.spritecollide(self, light, False):
            for l in light:
                if not l.light and self.rect.colliderect(l.rect) and l.orientation.startswith(self.orientation):
                    self.stopped = True
                    self.stop()

    def update(self, action, cars, mouse, lights, screen, volume):
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
            self.checkcrash(cars, mouse, volume)
        if action == "traffic" and not self.crashed:
            self.checktraffic(lights)
        if action == "kill" and self.rect.collidepoint([mouse.rect.centerx, mouse.rect.centery]) and self.crashed:
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
            if self.crashed:
                screen.blit(self.accident, [self.rect.centerx - 10, self.rect.centery - 10])
            if self.stopped and not self.crashed:
                if self.time > 30:
                    screen.blit(self.frown, [self.rect.centerx - 7, self.rect.centery - 7])
                    if not self in mouse.angry:
                        mouse.angry.add(self)
                        if not self.soundplayed:
                            self.horn.set_volume(float(volume * 0.1))
                            self.horn.play()
                            self.soundplayed = True
        if action == "stop":
            self.stop()
            self.stopped = True
        if action == "collidepoint":
            if (self.rect.left < 100 and self.rect.top == mouse.collidepoint[1]) or (self.rect.right > 700 and self.rect.top == mouse.collidepoint[1]) or (self.rect.top < 100 and self.rect.left == mouse.collidepoint[0]) or (self.rect.bottom > 500 and self.rect.left == mouse.collidepoint[0]):
                mouse.collide = True
        if action == "wait":
            if self.stopped:
                self.time += 1
            if not self.stopped:
                self.time = 0
                mouse.angry.remove(self)

class motorcycle(pygame.sprite.Sprite):
    def __init__(self, pos, orientation, direction, group):
        pygame.sprite.Sprite.__init__(self)
        self.color = random.choice(["motorcycle-black", "motorcycle-red"])
        imagefiles = ["./images/cars/" + self.color + "/bike-left.png", None, "./images/cars/" + self.color + "/bike-right.png"]
        imagefiles2 = ["./images/cars/" + self.color + "/bike-up.png", None, "./images/cars/" + self.color + "/bike-down.png"]
        self.headlightfiles = ["./images/cars/headlights/h1m.png", "./images/cars/headlights/h2m.png", "./images/cars/headlights/h3m.png", "./images/cars/headlights/h4m.png"]
        self.frown = pygame.image.load("./images/frowny.png")
        self.accident = pygame.image.load("./images/accident.png")
        self.horn = pygame.mixer.Sound("./sfx/horn.wav")
        self.crash = pygame.mixer.Sound("./sfx/collision.wav")
        self.soundplayed = False
        self.imagev = pygame.surface.Surface([10, 30])
        self.imageh = pygame.surface.Surface([30, 10])
        self.imagevc = pygame.surface.Surface([10, 40])
        self.imagehc = pygame.surface.Surface([40, 10])
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
        self.time = 0
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
                self.acceleration = 0.5

        #speed = direction(speed + acceleration)

        if self.speed < 5 and self.speed > -5:
            self.speed = (self.speed + self.acceleration)
        if self.speed > 5:
            self.speed = 5
        if self.speed < -5:
            self.speed = -5

        #move car + speed

        if self.orientation == "h":
            if self.direction == -1:
                self.rect.centerx -= self.speed
                self.rectc.centerx -= self.speed
            else:
                self.rect.centerx += self.speed
                self.rectc.centerx += self.speed
        elif self.orientation == "v":
            if self.direction == -1:
                self.rect.centery -= self.speed
                self.rectc.centery -= self.speed
            else:
                self.rect.centery += self.speed
                self.rectc.centery += self.speed

    def checkcrash(self, group, mouse, volume):
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
                self.crash.set_volume(float(volume * 0.1))
                self.crash.play()
                if mouse.objective["objective"] == "crashes" and mouse.objective["amount"] > 0:
                    mouse.objective["amount"] -= 0.5

            group.add(self)

    def checktraffic(self, light):

        self.stopped = False

        if pygame.sprite.spritecollide(self, light, False):
            for l in light:
                if not l.light and self.rect.colliderect(l.rect) and l.orientation.startswith(self.orientation):
                    self.stopped = True
                    self.stop()

    def update(self, action, cars, mouse, lights, screen, volume):
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
            self.checkcrash(cars, mouse, volume)
        if action == "traffic" and not self.crashed:
            self.checktraffic(lights)
        if action == "kill" and self.rect.collidepoint([mouse.rect.centerx, mouse.rect.centery]) and self.crashed:
            self.kill()
        if action == "draw":
            if mouse.objective["tod"] < 6 or mouse.objective["tod"] > 15 and not self.crashed:
                if self.orientation == "h":
                    if self.direction == 1:
                        screen.blit(self.headlight, [self.rect.left + 25, self.rect.top - 5])
                    elif self.direction == -1:
                        screen.blit(self.headlight, [self.rect.left - 15 , self.rect.top - 5])
                elif self.orientation == "v":
                    if self.direction == 1:
                        screen.blit(self.headlight, [self.rect.left, self.rect.top + 25])
                    elif self.direction == -1:
                        screen.blit(self.headlight, [self.rect.left, self.rect.top - 15])
            screen.blit(self.image, [self.rect.left, self.rect.top])
            if self.crashed:
                screen.blit(self.accident, [self.rect.centerx - 10, self.rect.centery - 10])
            if self.stopped and not self.crashed:
                if self.time > 30:
                    screen.blit(self.frown, [self.rect.centerx - 7, self.rect.centery - 7])
                    if not self in mouse.angry:
                        mouse.angry.add(self)
                        if not self.soundplayed:
                            self.horn.set_volume(float(volume * 0.1))
                            self.horn.play()
                            self.soundplayed = True
        if action == "stop":
            self.stop()
            self.stopped = True
        if action == "collidepoint":
            if (self.rect.left < 100 and self.rect.top == mouse.collidepoint[1]) or (self.rect.right > 700 and self.rect.top == mouse.collidepoint[1]) or (self.rect.top < 100 and self.rect.left == mouse.collidepoint[0]) or (self.rect.bottom > 500 and self.rect.left == mouse.collidepoint[0]):
                mouse.collide = True
        if action == "wait":
            if self.stopped:
                self.time += 1
            if not self.stopped:
                self.time = 0
                mouse.angry.remove(self)

class bus(pygame.sprite.Sprite):
    def __init__(self, pos, orientation, direction, group):
        pygame.sprite.Sprite.__init__(self)
        self.color = random.choice(["transit", "school"])
        imagefiles = ["./images/cars/" + self.color + "/car-left.png", None, "./images/cars/" + self.color + "/car-right.png"]
        imagefiles2 = ["./images/cars/" + self.color + "/car-up.png", None, "./images/cars/" + self.color + "/car-down.png"]
        self.headlightfiles = ["./images/cars/headlights/h1.png", "./images/cars/headlights/h2.png", "./images/cars/headlights/h3.png", "./images/cars/headlights/h4.png"]
        self.frown = pygame.image.load("./images/frowny.png")
        self.accident = pygame.image.load("./images/accident.png")
        self.horn = pygame.mixer.Sound("./sfx/horn.wav")
        self.crash = pygame.mixer.Sound("./sfx/collision.wav")
        self.soundplayed = False
        self.imagev = pygame.surface.Surface([20, 80])
        self.imageh = pygame.surface.Surface([80, 20])
        self.imagevc = pygame.surface.Surface([20, 90])
        self.imagehc = pygame.surface.Surface([90, 20])
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
        self.time = 0
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
                self.acceleration = self.acceleration + 0.1

            if self.acceleration == 0:
                self.acceleration = 1

        #speed = direction(speed + acceleration)

        if self.speed < 2 and self.speed > -2:
            self.speed = (self.speed + self.acceleration)
        if self.speed > 2:
            self.speed = 2
        if self.speed < -2:
            self.speed = -2

        #move car + speed

        if self.orientation == "h":
            if self.direction == -1:
                self.rect.centerx -= self.speed
                self.rectc.centerx -= self.speed
            else:
                self.rect.centerx += self.speed
                self.rectc.centerx += self.speed
        elif self.orientation == "v":
            if self.direction == -1:
                self.rect.centery -= self.speed
                self.rectc.centery -= self.speed
            else:
                self.rect.centery += self.speed
                self.rectc.centery += self.speed

    def checkcrash(self, group, mouse, volume):
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
                self.crash.set_volume(float(volume * 0.1))
                self.crash.play()
                if mouse.objective["objective"] == "crashes" and mouse.objective["amount"] > 0:
                    mouse.objective["amount"] -= 0.5

            group.add(self)

    def checktraffic(self, light):

        self.stopped = False

        if pygame.sprite.spritecollide(self, light, False):
            for l in light:
                if not l.light and self.rect.colliderect(l.rect) and l.orientation.startswith(self.orientation):
                    self.stopped = True
                    self.stop()

    def update(self, action, cars, mouse, lights, screen, volume):
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
            self.checkcrash(cars, mouse, volume)
        if action == "traffic" and not self.crashed:
            self.checktraffic(lights)
        if action == "kill" and self.rect.collidepoint([mouse.rect.centerx, mouse.rect.centery]) and self.crashed:
            self.kill()
        if action == "draw":
            if mouse.objective["tod"] < 6 or mouse.objective["tod"] > 15 and not self.crashed:
                if self.orientation == "h":
                    if self.direction == 1:
                        screen.blit(self.headlight, [self.rect.left + 75, self.rect.top])
                    elif self.direction == -1:
                        screen.blit(self.headlight, [self.rect.left - 15 , self.rect.top])
                elif self.orientation == "v":
                    if self.direction == 1:
                        screen.blit(self.headlight, [self.rect.left, self.rect.top + 75])
                    elif self.direction == -1:
                        screen.blit(self.headlight, [self.rect.left, self.rect.top - 15])
            screen.blit(self.image, [self.rect.left, self.rect.top])
            if self.crashed:
                screen.blit(self.accident, [self.rect.centerx - 10, self.rect.centery - 10])
            if self.stopped and not self.crashed:
                if self.time > 30:
                    screen.blit(self.frown, [self.rect.centerx - 7, self.rect.centery - 7])
                    if not self in mouse.angry:
                        mouse.angry.add(self)
                        if not self.soundplayed:
                            self.horn.set_volume(float(volume * 0.1))
                            self.horn.play()
                            self.soundplayed = True
        if action == "stop":
            self.stop()
            self.stopped = True
        if action == "collidepoint":
            if (self.rect.left < 100 and self.rect.top == mouse.collidepoint[1]) or (self.rect.right > 700 and self.rect.top == mouse.collidepoint[1]) or (self.rect.top < 100 and self.rect.left == mouse.collidepoint[0]) or (self.rect.bottom > 500 and self.rect.left == mouse.collidepoint[0]):
                mouse.collide = True
        if action == "wait":
            if self.stopped:
                self.time += 1
            if not self.stopped:
                self.time = 0
                mouse.angry.remove(self)
