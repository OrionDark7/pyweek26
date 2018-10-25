import pygame, random, math
import structures, entities, levels

#Copyright Orion Williams 2018

pygame.font.init()
window = pygame.display.set_mode([800, 600])
window.fill([88, 198, 73])
running = True
show_me = False
screen = "menu"
previous = "menu"
font = pygame.font.Font("./resources/Danger on the Motorway.otf", 16)
bkg = pygame.image.load("./images/bkg.png")
arrow = pygame.image.load("./images/arrow.png")
night_ = pygame.surface.Surface([800, 600])
night_setting = [200, 166, 133, 100, 66, 33, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 17, 33, 66, 100, 133, 166, 200, 217]
accidentpos = [0, 0]
level = 0
cargroup = pygame.sprite.Group()
roadgroup = pygame.sprite.Group()
lightgroup = pygame.sprite.Group()
intersectiongroup = pygame.sprite.Group()
intersectiongroup = pygame.sprite.Group()
buttongroup = pygame.sprite.Group()
buildinggroup = pygame.sprite.Group()
pygame.time.set_timer(pygame.USEREVENT, 100) #Acceleration
pygame.time.set_timer(pygame.USEREVENT + 1, 2250) #Car Spawn
pygame.time.set_timer(pygame.USEREVENT + 2, 1000) #Countdown
pygame.time.set_timer(pygame.USEREVENT + 3, 60000) #Time of Day change

class trafficbutton(pygame.sprite.Sprite):
    def __init__(self, pos, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface([20, 20])
        self.image.fill([0, 0, 0])
        self.image.set_alpha(200)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(pos)
        self.clicked = False
    def click(self):
        global mouse, lightgroup
        if self.rect.colliderect(mouse.rect):
            self.clicked = True
            mouse.id = self.id
            update(lightgroup, "toggle-id")
            #YOU WERE WORKING ON THIS AND PUTTING ID'S ON TRAFFIC LIGHTS


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
        self.accidents = 0.0
        self.score = 0
        self.id = None
        self.light = False
        self.angry = pygame.sprite.Group()
    def move(self, x, y):
        self.rect.centerx, self.rect.centery = x, y
    def reset_stats(self):
        self.score = 0
        self.angry = pygame.sprite.Group()
        self.objective = {}
        self.accident = False
        self.collidepoint = [0, 0]
        self.collide = False
        self.accidents = 0.0
        self.score = 0
        self.id = None

class imagebutton(pygame.sprite.Sprite):
    def __init__(self, image, pos, centered):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(str(image))
        self.rect = self.image.get_rect()
        if centered:
            self.rect.left, self.rect.top = 400 - self.rect.width/2, pos[1]
        else:
            self.rect.left, self.rect.top = pos
        self.clicked = False
    def click(self):
        global mouse
        if self.rect.colliderect(mouse.rect):
            self.clicked = True
    def draw(self):
        global window
        window.blit(self.image, [self.rect.left, self.rect.top])

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
        if self.rect.colliderect(mouse.rect):
            self.clicked = True
    def draw(self):
        global window
        window.blit(self.image, [self.rect.left, self.rect.top])

class switch(pygame.sprite.Sprite):
    def __init__(self, pos, toggle):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load("./images/ui/switch/switch-on.png"), pygame.image.load("./images/ui/switch/switch-off.png")]
        self.state = bool(toggle)
        self.clicked = False
        if self.state:
            self.image = self.images[0]
        else:
            self.image = self.images[1]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(pos)
    def toggle(self):
        global mouse
        if self.rect.colliderect(mouse.rect):
            self.clicked = True
            self.state = not self.state
            if self.state:
                self.image = self.images[0]
            else:
                self.image = self.images[1]
    def draw(self):
        global window
        window.blit(self.image, [self.rect.left, self.rect.top])

mouse = mouseclass()
menuButton = button("[m] menu", [400, 280], True)
replayButton = button("[r] replay", [400, 300], True)
nextLevelButton = button("[n] next level", [400, 320], True)
closeButton = button("[c] close", [20, 45], False)
showButton = button("[s] show me", [180, 45], False)
playButton = button("[p] play game", [20, 70], False)
howButton = button("[h] how to play", [20, 100], False)
settingsButton = button("[s] settings", [20, 130], False)
quitButton = button("[q] quit game", [20, 160], False)
backButton = button("[b] back", [10, 10], False)
resumeButton = button("[r] resume game", [20, 70], False)
fullSwitch = switch([140, 58], False)
classic = imagebutton("./images/ui/buttons/classic.png", [80, 240], False)
survival = imagebutton("./images/ui/buttons/freeplay.png", [320, 240], False)
freeplay = imagebutton("./images/ui/buttons/freeplay.png", [560, 240], False)
level1 = imagebutton("./images/ui/buttons/level1.png", [32, 60], False)
level2 = imagebutton("./images/ui/buttons/level2.png", [224, 60], False)
level3 = imagebutton("./images/ui/buttons/level1.png", [416, 60], False)
level4 = imagebutton("./images/ui/buttons/level2.png", [608, 60], False)
level5 = imagebutton("./images/ui/buttons/level1.png", [32, 240], False)
level6 = imagebutton("./images/ui/buttons/level2.png", [224, 240], False)
level7 = imagebutton("./images/ui/buttons/level1.png", [416, 240], False)
level8 = imagebutton("./images/ui/buttons/level2.png", [608, 240], False)
level9 = imagebutton("./images/ui/buttons/level1.png", [32, 420], False)
level10 = imagebutton("./images/ui/buttons/level2.png", [224, 420], False)
level11 = imagebutton("./images/ui/buttons/level1.png", [416, 420], False)
level12 = imagebutton("./images/ui/buttons/level2.png", [608, 420], False)

def selectLevel():
    global window
    image = pygame.image.load("./images/ui/buttons/freeplay.png")
    rect = pygame.surface.Surface([800, 600])
    rect.fill([0, 0, 0])
    rect.set_alpha(200)
    window.blit(rect, [0, 0])
    backButton.draw()
    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 16)
    text = font.render(
        "level 1", 1,
        [255, 255, 255])
    rect = text.get_rect().width / 2
    window.blit(text, [112 - rect, 185])
    text = font.render(
        "level 2", 1,
        [255, 255, 255])
    rect = text.get_rect().width / 2
    window.blit(text, [304 - rect, 185])
    text = font.render(
        "level 3", 1,
        [255, 255, 255])
    rect = text.get_rect().width / 2
    window.blit(text, [496 - rect, 185])
    text = font.render(
        "level 4", 1,
        [255, 255, 255])
    rect = text.get_rect().width / 2
    window.blit(text, [688 - rect, 185])

    text = font.render(
        "level 5", 1,
        [255, 255, 255])
    rect = text.get_rect().width / 2
    window.blit(text, [112 - rect, 365])
    text = font.render(
        "level 6", 1,
        [255, 255, 255])
    rect = text.get_rect().width / 2
    window.blit(text, [304 - rect, 365])
    text = font.render(
        "level 7", 1,
        [255, 255, 255])
    rect = text.get_rect().width / 2
    window.blit(text, [496 - rect, 365])
    text = font.render(
        "level 8", 1,
        [255, 255, 255])
    rect = text.get_rect().width / 2
    window.blit(text, [688 - rect, 365])

    text = font.render(
        "level 9", 1,
        [255, 255, 255])
    rect = text.get_rect().width / 2
    window.blit(text, [112 - rect, 545])
    text = font.render(
        "level 10", 1,
        [255, 255, 255])
    rect = text.get_rect().width / 2
    window.blit(text, [304 - rect, 545])
    text = font.render(
        "level 11", 1,
        [255, 255, 255])
    rect = text.get_rect().width / 2
    window.blit(text, [496 - rect, 545])
    text = font.render(
        "level 12", 1,
        [255, 255, 255])
    rect = text.get_rect().width / 2
    window.blit(text, [688 - rect, 545])

    level1.draw()
    level2.draw()
    level3.draw()
    level4.draw()
    level5.draw()
    level6.draw()
    level7.draw()
    level8.draw()
    level9.draw()
    level10.draw()
    level11.draw()
    level12.draw()

def selectScreen():
    global window
    rect = pygame.surface.Surface([800, 200])
    rect.fill([0, 0, 0])
    rect.set_alpha(200)
    window.blit(rect, [0, 200])
    rect = pygame.surface.Surface([107, 27])
    rect.fill([0, 0, 0])
    rect.set_alpha(200)
    window.blit(rect, [5, 5])
    backButton.draw()
    classic.draw()
    survival.draw()
    freeplay.draw()
    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 16)
    text = font.render(
        "[c] classic", 1,
        [255, 255, 255])
    rect = text.get_rect().width / 2
    window.blit(text, [160 - rect, 210])
    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 16)
    text = font.render(
        "[s] survival", 1,
        [255, 255, 255])
    rect = text.get_rect().width / 2
    window.blit(text, [400 - rect, 210])
    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 16)
    text = font.render(
        "[f] freeplay", 1,
        [255, 255, 255])
    rect = text.get_rect().width / 2
    window.blit(text, [640 - rect, 210])

def pauseScreen():
    global window
    rect = pygame.surface.Surface([195, 180])
    rect.fill([0, 0, 0])
    rect.set_alpha(200)
    window.blit(rect, [10, 10])
    resumeButton.draw()
    howButton.draw()
    settingsButton.draw()
    quitButton.draw()
    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 32)
    text = font.render(
        "paused", 1,
        [255, 255, 255])
    window.blit(text, [20, 22])

def howScreen():
    global window
    rect = pygame.surface.Surface([800, 600])
    rect.fill([0, 0, 0])
    rect.set_alpha(200)
    window.blit(rect, [0, 0])
    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 32)
    text = font.render(
        "how to play", 1,
        [255, 255, 255])
    rect = 400 - text.get_rect().width / 2
    window.blit(text, [rect, 10])
    backButton.draw()

def settingsScreen():
    global window
    rect = pygame.surface.Surface([800, 600])
    rect.fill([0, 0, 0])
    rect.set_alpha(200)
    window.blit(rect, [0, 0])
    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 32)
    text = font.render(
        "settings", 1,
        [255, 255, 255])
    rect = 400 - text.get_rect().width / 2
    window.blit(text, [rect, 10])
    backButton.draw()
    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 16)
    text = font.render(
        "fullscreen", 1,
        [255, 255, 255])
    window.blit(text, [10, 60])
    fullSwitch.draw()

def menuScreen():
    global window
    rect = pygame.surface.Surface([195, 180])
    rect.fill([0, 0, 0])
    rect.set_alpha(200)
    window.blit(rect, [10, 10])
    playButton.draw()
    howButton.draw()
    settingsButton.draw()
    quitButton.draw()
    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 32)
    text = font.render(
        "title", 1,
        [255, 255, 255])
    window.blit(text, [20, 22])

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
    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 16)
    text = font.render(
        "cars passed: " + str(mouse.score), 1,
        [255, 255, 255])
    rect = 400 - text.get_rect().width / 2
    window.blit(text, [rect, 220])
    if mouse.objective["objective"] == "survival":
        if len(str(int(math.floor(mouse.objective["time"] % 60)))) == 1:
            text = font.render("time survived: " + str(int(math.floor(mouse.objective["time"] / 60))) + ":0" + str(int(math.floor(
                mouse.objective["time"] % 60))), 1, [255, 255, 255])
        else:
            text = font.render("time survived: " + str(int(math.floor(mouse.objective["time"] / 60))) + ":" + str(int(math.floor(mouse.objective["time"] % 60))), 1, [255, 255, 255])
        rect = 400 - text.get_rect().width / 2
        window.blit(text, [rect, 240])
        menuButton.draw()
        replayButton.draw()
    else:
        text = font.render(
            "accidents: " + str(int(math.floor(mouse.accidents))), 1,
            [255, 255, 255])
        rect = 400 - text.get_rect().width / 2
        window.blit(text, [rect, 240])
        menuButton.draw()
        replayButton.draw()

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
    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 16)
    text = font.render(
        "cars passed: " + str(mouse.score), 1,
        [255, 255, 255])
    rect = 400 - text.get_rect().width / 2
    window.blit(text, [rect, 220])
    text = font.render(
        "accidents: " + str(int(math.floor(mouse.accidents))), 1,
        [255, 255, 255])
    rect = 400 - text.get_rect().width / 2
    window.blit(text, [rect, 240])
    menuButton.draw()
    replayButton.draw()
    nextLevelButton.draw()

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
    if mouse.objective["objective"] != "freeplay" and mouse.objective["objective"] != "survival":
        if len(str(int(math.floor(mouse.objective["time"] % 60)))) == 1:
            text = font.render("time left: " + str(int(math.floor(mouse.objective["time"] / 60))) + ":0" + str(int(math.floor(
                mouse.objective["time"] % 60))), 1, [255, 255, 255])
        else:
            text = font.render("time left: " + str(int(math.floor(mouse.objective["time"] / 60))) + ":" + str(int(math.floor(mouse.objective["time"] % 60))), 1, [255, 255, 255])
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
        if str(mouse.objective["objective"]) == "anger":
            text = font.render("level objective:", 1, [255, 255, 255])
            window.blit(text, [20, 510])
            text = font.render("don't make " + str(int(math.floor(mouse.objective["amount"])) - len(mouse.angry)) + " drivers angry", 1,
                               [255, 255, 255])
            window.blit(text, [20, 535])
    elif mouse.objective["objective"] == "survival":
        text = font.render("cars passed: " + str(int(math.floor(mouse.score))), 1,
                           [255, 255, 255])
        window.blit(text, [20, 535])
        text = font.render("survival mode", 1, [255, 255, 255])
        window.blit(text, [20, 510])
        if len(str(mouse.objective["time"] % 60)) == 1:
            text = font.render("time: " + str(int(math.floor(mouse.objective["time"] / 60))) + ":0" + str(
                mouse.objective["time"] % 60), 1, [255, 255, 255])
        else:
            text = font.render("time: " + str(int(math.floor(mouse.objective["time"] / 60))) + ":" + str(mouse.objective["time"] % 60), 1, [255, 255, 255])
        window.blit(text, [20, 560])
    elif mouse.objective["objective"] == "freeplay":
        text = font.render("freeplay mode", 1, [255, 255, 255])
        window.blit(text, [20, 510])
        text = font.render("cars passed: " + str(int(math.floor(mouse.score))), 1,
                           [255, 255, 255])
        window.blit(text, [20, 535])
        text = font.render("accidents: " + str(int(math.floor(mouse.accidents))), 1, [255, 255, 255])
        window.blit(text, [20, 560])

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

def getButtons(level):
    buttons = pygame.sprite.Group()
    if level == "freeplay":
        buttons.add(trafficbutton([140, 140], 1))
        buttons.add(trafficbutton([540, 140], 2))
        buttons.add(trafficbutton([140, 340], 3))
        buttons.add(trafficbutton([540, 340], 4))
    return buttons

def getLevel(level):
    global roadgroup, cargroup, lightgroup, intersectiongroup, buildinggroup, mouse
    roadgroup, cargroup, lightgroup, intersectiongroup, buildinggroup, mouse.objective = levels.level(level)
    buttongroup = getButtons("freeplay")

getLevel(0)

while running:
    print len(mouse.angry)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if screen == "settings":
                if event.key == pygame.K_b:
                    screen = previous
            if screen == "how":
                if event.key == pygame.K_b:
                    screen = previous
            if screen == "game over":
                if event.key == pygame.K_m:
                    screen = "menu"
                    level = 0
                    getLevel(level)
                    mouse.score = 0
                if event.key == pygame.K_r:
                    getLevel(level)
                    screen = "game"
                    mouse.score = 0
            if screen == "you win":
                if event.key == pygame.K_m:
                    screen = "menu"
                    level = 0
                    getLevel(level)
                    mouse.score = 0
                if event.key == pygame.K_r:
                    getLevel(level)
                    screen = "game"
                    mouse.score = 0
                if event.key == pygame.K_n:
                    screen = "game"
                    level += 1
                    getLevel(level)
                    mouse.score = 0
            if screen == "select level":
                if event.key == pygame.K_b:
                    screen = "select"
            elif screen == "select":
                if event.key == pygame.K_c:
                    screen = "select level"
                    #screen = "game"
                    #level = 1
                    #getLevel(level)
                if event.key == pygame.K_s:
                    screen = "game"
                    level = "survival"
                    getLevel(level)
                if event.key == pygame.K_f:
                    screen = "game"
                    level = "freeplay"
                    getLevel(level)
                if event.key == pygame.K_b:
                    screen = "menu"
                    level = 0
                    getLevel(level)
            if screen == "menu":
                if event.key == pygame.K_p:
                    screen = "select"
                    # level = 1
                    # getLevel(level)
                if event.key == pygame.K_s:
                    screen = "settings"
                if event.key == pygame.K_h:
                    screen = "how"
                if event.key == pygame.K_q:
                    running = False
            if screen == "game":
                if event.key == pygame.K_ESCAPE:
                    screen = "pause"
                    update(cargroup, "stop")
                if mouse.accident and screen == "game":
                    if event.key == pygame.K_c:
                        mouse.accident = False
                        show_me = False
                    if event.key == pygame.K_s:
                        show_me = True
                        accidentpos = [mouse.accidentinfo[0] - 30, mouse.accidentinfo[1] - 80]
            elif screen == "pause":
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_r:
                    screen = "game"
                if event.key == pygame.K_h:
                    screen = "how"
                    previous = "pause"
                if event.key == pygame.K_s:
                    screen = "settings"
                    previous = "pause"
                if event.key == pygame.K_q:
                    screen = "menu"
                    level = 0
                    getLevel(level)
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = pygame.mouse.get_pressed()
            mouse.move(event.pos[0], event.pos[1])
            if clicked[0] == 1:
                if screen == "game":
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
                if screen == "menu":
                    playButton.click()
                    if playButton.clicked:
                        screen = "select"
                        playButton.clicked = False
                    howButton.click()
                    if howButton.clicked:
                        screen = "how"
                        previous = "menu"
                        howButton.clicked = False
                    settingsButton.click()
                    if settingsButton.clicked:
                        screen = "settings"
                        previous = "menu"
                        settingsButton.clicked = False
                    quitButton.click()
                    if quitButton.clicked:
                        running = False
                        quitButton.clicked = False
                if screen == "pause":
                    resumeButton.click()
                    if resumeButton.clicked:
                        screen = "game"
                        resumeButton.clicked = False
                    howButton.click()
                    if howButton.clicked:
                        screen = "how"
                        previous = "pause"
                        howButton.clicked = False
                    settingsButton.click()
                    if settingsButton.clicked:
                        screen = "settings"
                        previous = "pause"
                        settingsButton.clicked = False
                    quitButton.click()
                    if quitButton.clicked:
                        screen = "menu"
                        level = 0
                        getLevel(0)
                        quitButton.clicked = False
                if screen == "game over":
                    menuButton.click()
                    if menuButton.clicked:
                        mouse.reset_stats()
                        screen = "menu"
                        level = 0
                        getLevel(level)
                        menuButton.clicked = False
                        mouse.score = 0
                    replayButton.click()
                    if replayButton.clicked:
                        mouse.reset_stats()
                        getLevel(level)
                        screen = "game"
                        replayButton.clicked = False
                        mouse.score = 0
                if screen == "you win":
                    menuButton.click()
                    if menuButton.clicked:
                        mouse.reset_stats()
                        screen = "menu"
                        level = 0
                        getLevel(level)
                        menuButton.clicked = False
                        mouse.score = 0
                    replayButton.click()
                    if replayButton.clicked:
                        mouse.reset_stats()
                        getLevel(level)
                        screen = "game"
                        replayButton.clicked = False
                        mouse.score = 0
                    nextLevelButton.click()
                    if nextLevelButton.clicked:
                        level += 1
                        getLevel(level)
                        screen = "game"
                        nextLevelButton.clicked = False
                        mouse.score = 0
                if screen == "settings":
                    backButton.click()
                    if backButton.clicked:
                        screen = previous
                        backButton.clicked = False
                    fullSwitch.toggle()
                    if fullSwitch.clicked:
                        if fullSwitch.state:
                            window = pygame.display.set_mode([800, 600], pygame.FULLSCREEN)
                        else:
                            window = pygame.display.set_mode([800, 600])
                        fullSwitch.clicked = False
                if screen == "how":
                    backButton.click()
                    if backButton.clicked:
                        screen = previous
                        backButton.clicked = False
                if screen == "select level":
                    backButton.click()
                    if backButton.clicked:
                        screen = "select"
                        backButton.clicked = False
                if screen == "select":
                    classic.click()
                    if classic.clicked:
                        screen = "select level"
                        #screen = "game"
                        #level = 1
                        #getLevel(level)
                        classic.clicked = False
                    survival.click()
                    if survival.clicked:
                        mouse.reset_stats()
                        level = "survival"
                        getLevel(level)
                        screen = "game"
                        survival.clicked = False
                    freeplay.click()
                    if freeplay.clicked:
                        mouse.reset_stats()
                        level = "freeplay"
                        getLevel(level)
                        screen = "game"
                        freeplay.clicked = False
                    backButton.click()
                    if backButton.clicked:
                        mouse.reset_stats()
                        level = 0
                        getLevel(level)
                        screen = "menu"
                        backButton.clicked = False
                elif screen == "select level":
                    level1.click()
                    if level1.clicked:
                        level = 1
                        screen = "game"
                        getLevel(level)
                        level1.clicked = False
                    level2.click()
                    if level2.clicked:
                        level = 2
                        screen = "game"
                        getLevel(level)
                        level2.clicked = False
                    level3.click()
                    if level3.clicked:
                        level = 3
                        screen = "game"
                        getLevel(level)
                        level3.clicked = False
                    level4.click()
                    if level4.clicked:
                        level = 4
                        screen = "game"
                        getLevel(level)
                        level4.clicked = False
                    level5.click()
                    if level5.clicked:
                        level = 5
                        screen = "game"
                        getLevel(level)
                        level5.clicked = False
                    level6.click()
                    if level6.clicked:
                        level = 6
                        screen = "game"
                        getLevel(level)
                        level6.clicked = False
                    level7.click()
                    if level7.clicked:
                        level = 7
                        screen = "game"
                        getLevel(level)
                        level7.clicked = False
                    level8.click()
                    if level8.clicked:
                        level = 8
                        screen = "game"
                        getLevel(level)
                        level8.clicked = False
                    level9.click()
                    if level9.clicked:
                        level = 9
                        screen = "game"
                        getLevel(level)
                        level9.clicked = False
                    level10.click()
                    if level10.clicked:
                        level = 10
                        screen = "game"
                        getLevel(level)
                        level10.clicked = False
                    level11.click()
                    if level11.clicked:
                        level = 11
                        screen = "game"
                        getLevel(level)
                        level11.clicked = False
                    level12.click()
                    if level12.clicked:
                        level = 12
                        screen = "game"
                        getLevel(level)
                        level12.clicked = False
            elif clicked[2] == 1:
                if screen == "game":
                    update(cargroup, "kill")

        if event.type == pygame.USEREVENT:
            update(cargroup, "accel")
        if event.type == pygame.USEREVENT + 1 and screen == "game" or screen == "menu":
            for i in roadgroup:
                orientation = i.orientation
                direction = random.choice([0, 1])
                if i.orientation == "vertical":
                    pos = i.rect.left + [4, 36][direction], i.rect.top + [20, 540][direction]
                    dir = [1, -1][direction]
                elif i.orientation == "horizontal":
                    pos = i.rect.left + [20, 740][direction], i.rect.top + [36, 4][direction]
                    dir = [1, -1][direction]
                mouse.collide = False
                mouse.collidepoint = pos
                update(cargroup, "collidepoint")
                type = random.randint(0, 7)
                if not mouse.collide:
                    if type == 0:
                        cargroup.add(entities.bus(pos, i.orientation, dir, cargroup))
                    if type == 1:
                        cargroup.add(entities.motorcycle(pos, i.orientation, dir, cargroup))
                    elif type != 0 and type != 1:
                        cargroup.add(entities.car(pos, i.orientation, dir, cargroup))
        if event.type == pygame.USEREVENT + 2:
            update(cargroup, "wait")
            if screen == "game" and mouse.objective["time"] != "freeplay":
                if mouse.objective["objective"] == "survival":
                    mouse.objective["time"] += 1
                elif mouse.objective["objective"] != "survival":
                    if mouse.objective["objective"] == "cars":
                        if mouse.objective["time"] > 0:
                            if len(mouse.angry) > 20:
                                mouse.objective["time"] -= 4
                            elif len(mouse.angry) > 10:
                                mouse.objective["time"] -= 2
                            else:
                                mouse.objective["time"] -= 1
                    if mouse.objective["objective"] == "crashes" or mouse.objective["objective"] == "anger":
                        if mouse.objective["time"] > 0:
                            if len(mouse.angry) > 20:
                                mouse.objective["time"] -= 0.25
                            elif len(mouse.angry) > 10:
                                mouse.objective["time"] -= 0.5
                            else:
                                mouse.objective["time"] -= 1
                if mouse.objective["time"] <= 0:
                    if mouse.objective["objective"] == "cars":
                        screen = "game over"
                        update(cargroup, "stop")
                    if mouse.objective["objective"] == "crashes" or mouse.objective["objective"] == "anger":
                        screen = "you win"
                        update(cargroup, "stop")
        if event.type == pygame.USEREVENT + 3 and screen == "game":
            if mouse.objective["tod"] < 23:
                mouse.objective["tod"] += 1
            elif mouse.objective["tod"] >= 23:
                mouse.objective["tod"] = 0

    if screen == "game":
        background()
        roadgroup.draw(window)
        intersectiongroup.draw(window)
        buildinggroup.draw(window)
        update(cargroup, "traffic")
        update(cargroup, "crash")
        update(cargroup, "drive")
        update(cargroup, "draw")
        update(lightgroup, "draw")
        night(night_setting[mouse.objective["tod"]])
        buttongroup.draw(window)
        displayinfo()
        if mouse.objective["objective"] == "anger" and mouse.objective["amount"] - len(mouse.angry) <= 0:
            screen = "game over"
            update(cargroup, "stop")
        if mouse.objective["objective"] == "cars" and mouse.objective["amount"] <= 0:
            screen = "you win"
            update(cargroup, "stop")
        if mouse.objective["objective"] == "crashes" and mouse.objective["amount"] <= 0:
            screen = "game over"
            update(cargroup, "stop")
        if mouse.accident:
            if mouse.objective["objective"] == "survival":
                screen = "game over"
                update(cargroup, "stop")
            else:
                accidentNotification()

    if screen == "game over":
        background()
        roadgroup.draw(window)
        intersectiongroup.draw(window)
        buildinggroup.draw(window)
        update(cargroup, "draw")
        update(lightgroup, "draw")
        night(night_setting[mouse.objective["tod"]])
        gameOverScreen()

    if screen == "you win":
        background()
        roadgroup.draw(window)
        intersectiongroup.draw(window)
        buildinggroup.draw(window)
        update(cargroup, "draw")
        update(lightgroup, "draw")
        night(night_setting[mouse.objective["tod"]])
        winScreen()

    if screen == "menu":
        background()
        roadgroup.draw(window)
        intersectiongroup.draw(window)
        buildinggroup.draw(window)
        update(cargroup, "traffic")
        update(cargroup, "crash")
        update(cargroup, "drive")
        update(cargroup, "draw")
        update(lightgroup, "draw")
        menuScreen()

    if screen == "how":
        background()
        howScreen()

    if screen == "settings":
        background()
        settingsScreen()

    if screen == "pause":
        background()
        roadgroup.draw(window)
        intersectiongroup.draw(window)
        buildinggroup.draw(window)
        update(cargroup, "draw")
        update(lightgroup, "draw")
        pauseScreen()

    if screen == "select":
        background()
        roadgroup.draw(window)
        intersectiongroup.draw(window)
        buildinggroup.draw(window)
        update(cargroup, "traffic")
        update(cargroup, "crash")
        update(cargroup, "drive")
        update(cargroup, "draw")
        update(lightgroup, "draw")
        selectScreen()

    if screen == "select level":
        background()
        selectLevel()

    pygame.display.flip()

pygame.quit()