import pygame, random, math
import structures, entities, levels

#Copyright Orion Williams 2018

pygame.font.init()
window = pygame.display.set_mode([800, 600])
window.fill([88, 198, 73])
running = True
bkg = pygame.image.load("./images/bkg.png")
night_ = pygame.surface.Surface([800, 600])
night_setting = [200, 166, 133, 100, 66, 33, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 17, 33, 66, 100, 133, 166, 200]
cargroup = pygame.sprite.Group()
roadgroup = pygame.sprite.Group()
lightgroup = pygame.sprite.Group()
intersectiongroup = pygame.sprite.Group()
pygame.time.set_timer(pygame.USEREVENT, 100) #Acceleration
pygame.time.set_timer(pygame.USEREVENT + 1, 750) #Car Spawn
pygame.time.set_timer(pygame.USEREVENT + 2, 1000) #Countdown
pygame.time.set_timer(pygame.USEREVENT + 3, 60000) #Time of Day change

class mouseclass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.surface.Surface([1, 1])
        self.rect = self.rect.get_rect()
        self.rect.centerx, self.rect.centery = 0, 0
        self.objective = {}
    def move(self, x, y):
        self.rect.centerx, self.rect.centery = x, y

mouse = mouseclass()

def displayinfo():
    global mouse, window
    rect = pygame.surface.Surface([275, 80])
    rect.fill([0, 0, 0])
    rect.set_alpha(200)
    window.blit(rect, [10, 502])
    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 16)
    if len(str(mouse.objective["time"] % 60)) == 1:
        text = font.render("time left: " + str(int(math.floor(mouse.objective["time"] / 60))) + ":0" + str(
            mouse.objective["time"] % 60), 1, [255, 255, 255])
    else:
        text = font.render("time left: " + str(int(math.floor(mouse.objective["time"] / 60))) + ":" + str(mouse.objective["time"] % 60), 1, [255, 255, 255])
    window.blit(text, [20, 560])
    text = font.render("amount remaining: " + str(mouse.objective["amount"]), 1, [255, 255, 255])
    window.blit(text, [20, 535])
    text = font.render("objective: " + str(mouse.objective["objective"]), 1, [255, 255, 255])
    window.blit(text, [20, 510])

def night(a):
    # A nighttime overdrop to make it seem dark
    global night_
    night_.fill([29, 66, 124])
    night_.set_alpha(a)
    window.blit(night_, [0, 0])

def background():
    window.blit(bkg, [0, 0])

def update(group, action):
    global cargroup, roadgroup, lightgroup, mouse, window

    if group == cargroup:
        group.update(action, cargroup, mouse, lightgroup)
    elif group == lightgroup:
        group.update(action, window, mouse)
    else:
        group.update(action)

roadgroup, cargroup, lightgroup, intersectiongroup, mouse.objective = levels.level(0)

while running:
    print mouse.objective
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse.move(event.pos[0], event.pos[1])
            update(cargroup, "kill")
            update(lightgroup, "toggle")
        if event.type == pygame.USEREVENT:
            update(cargroup, "accel")
        if event.type == pygame.USEREVENT + 1:
            for i in roadgroup:
                orientation = i.orientation
                direction = random.choice([0, 1])
                if i.orientation == "vertical":
                    pos = i.rect.left + [4, 36][direction], i.rect.top + [20, 540][direction]
                    dir = [1, -1][direction]
                elif i.orientation == "horizontal":
                    pos = i.rect.left + [20, 740][direction], i.rect.top + [4, 36][direction]
                    dir = [1, -1][direction]
                cargroup.add(entities.car(pos, i.orientation, dir, cargroup))
        if event.type == pygame.USEREVENT + 2:
            if mouse.objective["time"] > 0:
                mouse.objective["time"] -= 1
            else:
                running = False
        if event.type == pygame.USEREVENT + 3:
            if mouse.objective["tod"] < 23:
                mouse.objective["tod"] += 1
            elif mouse.objective["tod"] >= 23:
                mouse.objective["tod"] = 0

    background()
    roadgroup.draw(window)
    intersectiongroup.draw(window)
    update(cargroup, "traffic")
    update(cargroup, "crash")
    update(cargroup, "drive")
    cargroup.draw(window)
    update(lightgroup, "draw")
    night(night_setting[mouse.objective["tod"]])
    displayinfo()

    pygame.display.flip()

pygame.quit()