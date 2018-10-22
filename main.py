import pygame, random, math
import structures, entities, levels

#Copyright Orion Williams 2018

pygame.font.init()
window = pygame.display.set_mode([800, 600])
window.fill([88, 198, 73])
running = True
show_me = False
screen = "game"
font = pygame.font.Font("./resources/Danger on the Motorway.otf", 16)
bkg = pygame.image.load("./images/bkg.png")
arrow = pygame.image.load("./images/arrow.png")
night_ = pygame.surface.Surface([800, 600])
night_setting = [200, 166, 133, 100, 66, 33, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 17, 33, 66, 100, 133, 166, 200, 217]
accidentpos = [0, 0]
cargroup = pygame.sprite.Group()
roadgroup = pygame.sprite.Group()
lightgroup = pygame.sprite.Group()
intersectiongroup = pygame.sprite.Group()
pygame.time.set_timer(pygame.USEREVENT, 100) #Acceleration
pygame.time.set_timer(pygame.USEREVENT + 1, 1250) #Car Spawn
pygame.time.set_timer(pygame.USEREVENT + 2, 1000) #Countdown
pygame.time.set_timer(pygame.USEREVENT + 3, 60000) #Time of Day change

class mouseclass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.surface.Surface([1, 1])
        self.rect = self.rect.get_rect()
        self.rect.centerx, self.rect.centery = 0, 0
        self.objective = {}
        self.accident = False
        self.collidepoint = [0, 0]
        self.collide = False
    def move(self, x, y):
        self.rect.centerx, self.rect.centery = x, y

class button(pygame.sprite.Sprite):
    def __init__(self, text, pos, centered):
        global font
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.image = font.render(self.text, 1, [255, 255, 255])
        self.rect = self.image.get_rect()
        if centered:
            self.rect.left, self.rect.top = 400 - self.rect.width/2, pos[1]
        else:
            self.rect.left, self.rect.top = pos
        self.clicked = False
    def click(self):
        global mouse
        if self.rect.collidepoint([mouse.rect.centerx, mouse.rect.centery]):
            self.clicked = True
    def draw(self):
        global window
        window.blit(self.image, [self.rect.left, self.rect.top])

mouse = mouseclass()
menuButton = button("[m] menu", [400, 280], True)
closeButton = button("[c] close", [20, 45], False)
showButton = button("[s] show me", [180, 45], False)

def gameOverScreen():
    global window
    rect = pygame.surface.Surface([800, 600])
    rect.fill([0, 0, 0])
    rect.set_alpha(200)
    window.blit(rect, [0, 0])
    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 32)
    text = font.render(
        "game over!", 1,
        [255, 255, 255])
    rect = 400 - text.get_rect().width / 2
    window.blit(text, [rect, 180])
    menuButton.draw()

def winScreen():
    global window
    rect = pygame.surface.Surface([800, 600])
    rect.fill([0, 0, 0])
    rect.set_alpha(200)
    window.blit(rect, [0, 0])
    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 32)
    text = font.render(
        "you win!", 1,
        [255, 255, 255])
    rect = 400 - text.get_rect().width / 2
    window.blit(text, [rect, 180])
    menuButton.draw()

def accidentNotification():
    global mouse, window, show_me, arrow, accidentpos
    rect = pygame.surface.Surface([320, 60])
    rect.fill([0, 0, 0])
    rect.set_alpha(200)
    window.blit(rect, [10, 10])
    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 16)
    text = font.render(
        "there's been an accident!", 1,
        [255, 255, 255])
    window.blit(text, [20, 20])
    closeButton.draw()
    showButton.draw()
    if show_me:
        window.blit(pygame.transform.scale2x(arrow), [accidentpos[0], accidentpos[1]])

def displayinfo():
    global mouse, window
    rect = pygame.surface.Surface([350, 80])
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
    if str(mouse.objective["objective"]) == "cars":
        text = font.render("level objective:", 1, [255, 255, 255])
        window.blit(text, [20, 510])
        text = font.render("get " + str(mouse.objective["amount"]) + " cars out of the level", 1, [255, 255, 255])
        window.blit(text, [20, 535])
    if str(mouse.objective["objective"]) == "crashes":
        text = font.render("level objective:", 1, [255, 255, 255])
        window.blit(text, [20, 510])
        text = font.render("have less than " + str(int(math.floor(mouse.objective["amount"]))) + " accidents", 1, [255, 255, 255])
        window.blit(text, [20, 535])

def night(a):
    # A night time overdrop to make it seem dark
    global night_
    night_.fill([29, 66, 124])
    night_.set_alpha(a)
    window.blit(night_, [0, 0])

def background():
    window.blit(bkg, [0, 0])

def update(group, action):
    global cargroup, roadgroup, lightgroup, mouse, window

    if group == cargroup:
        group.update(action, cargroup, mouse, lightgroup, window)
    elif group == lightgroup:
        group.update(action, window, mouse)
    else:
        group.update(action)

roadgroup, cargroup, lightgroup, intersectiongroup, mouse.objective = levels.level(0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if mouse.accident:
                if event.key == pygame.K_c:
                    mouse.accident = False
                    show_me = False
                if event.key == pygame.K_s:
                    show_me = True
                    accidentpos = [mouse.accidentinfo[0] - 30, mouse.accidentinfo[1] - 80]
        if event.type == pygame.MOUSEBUTTONDOWN:
            if screen == "game":
                mouse.move(event.pos[0], event.pos[1])
                update(cargroup, "kill")
                update(lightgroup, "toggle")
                if mouse.accident:
                    closeButton.click()
                    if closeButton.clicked:
                        mouse.accident = False
                        closeButton.clicked = False
                    showButton.click()
                    if showButton.clicked:
                        show_me = True
                        accidentpos = [mouse.accidentinfo[0] - 30, mouse.accidentinfo[1] - 80]
                        showButton.clicked = False
            if screen == "game over":
                menuButton.click()
                if menuButton.clicked:
                    running = False
                    menuButton.clicked = False
        if event.type == pygame.USEREVENT:
            update(cargroup, "accel")
        if event.type == pygame.USEREVENT + 1 and screen == "game":
            for i in roadgroup:
                orientation = i.orientation
                direction = random.choice([0, 1])
                if i.orientation == "vertical":
                    pos = i.rect.left + [4, 36][direction], i.rect.top + [20, 540][direction]
                    dir = [1, -1][direction]
                elif i.orientation == "horizontal":
                    pos = i.rect.left + [20, 740][direction], i.rect.top + [4, 36][direction]
                    dir = [1, -1][direction]
                mouse.collide = False
                mouse.collidepoint = pos
                update(cargroup, "collidepoint")
                if not mouse.collide:
                    cargroup.add(entities.car(pos, i.orientation, dir, cargroup))
        if event.type == pygame.USEREVENT + 2:
            if mouse.objective["time"] > 0:
                mouse.objective["time"] -= 1
            else:
                if mouse.objective["objective"] == "cars":
                    screen = "game over"
                    update(cargroup, "stop")
                if mouse.objective["objective"] == "crashes":
                    screen = "you win"
                    update(cargroup, "stop")
        if event.type == pygame.USEREVENT + 3:
            if mouse.objective["tod"] < 23:
                mouse.objective["tod"] += 1
            elif mouse.objective["tod"] >= 23:
                mouse.objective["tod"] = 0

    if screen == "game":
        background()
        roadgroup.draw(window)
        intersectiongroup.draw(window)
        update(cargroup, "traffic")
        update(cargroup, "crash")
        update(cargroup, "drive")
        update(cargroup, "draw")
        update(lightgroup, "draw")
        night(night_setting[mouse.objective["tod"]])
        displayinfo()
        if mouse.objective["objective"] == "cars" and mouse.objective["amount"] <= 0:
            screen = "you win"
            update(cargroup, "stop")
        if mouse.objective["objective"] == "crashes" and mouse.objective["amount"] <= 0:
            screen = "game over"
            update(cargroup, "stop")
        if mouse.accident:
            accidentNotification()

    if screen == "game over":
        background()
        roadgroup.draw(window)
        intersectiongroup.draw(window)
        update(cargroup, "draw")
        update(lightgroup, "draw")
        night(night_setting[mouse.objective["tod"]])
        gameOverScreen()

    if screen == "you win":
        background()
        roadgroup.draw(window)
        intersectiongroup.draw(window)
        update(cargroup, "draw")
        update(lightgroup, "draw")
        night(night_setting[mouse.objective["tod"]])
        winScreen()

    pygame.display.flip()

pygame.quit()