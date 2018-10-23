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
buildinggroup = pygame.sprite.Group()
pygame.time.set_timer(pygame.USEREVENT, 100) #Acceleration
pygame.time.set_timer(pygame.USEREVENT + 1, 2250) #Car Spawn
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
        self.accidents = 0.0
        self.score = 0
    def move(self, x, y):
        self.rect.centerx, self.rect.centery = x, y
    def reset_stats(self):
        self.objective = {}
        self.accident = False
        self.collidepoint = [0, 0]
        self.collide = False
        self.accidents = 0.0
        self.score = 0

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
classic = imagebutton("./images/ui/buttons/freeplay.png", [80, 240], False)
survival = imagebutton("./images/ui/buttons/freeplay.png", [320, 240], False)
freeplay = imagebutton("./images/ui/buttons/freeplay.png", [560, 240], False)

def selectScreen():
    global window
    rect = pygame.surface.Surface([800, 200])
    rect.fill([0, 0, 0])
    rect.set_alpha(200)
    window.blit(rect, [0, 200])
    classic.draw()
    survival.draw()
    freeplay.draw()
    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 16)
    text = font.render(
        "classic", 1,
        [255, 255, 255])
    rect = text.get_rect().width / 2
    window.blit(text, [160 - rect, 210])
    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 16)
    text = font.render(
        "survival", 1,
        [255, 255, 255])
    rect = text.get_rect().width / 2
    window.blit(text, [400 - rect, 210])
    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 16)
    text = font.render(
        "freeplay", 1,
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
        if len(str(mouse.objective["time"] % 60)) == 1:
            text = font.render("time survived: " + str(int(math.floor(mouse.objective["time"] / 60))) + ":0" + str(
                mouse.objective["time"] % 60), 1, [255, 255, 255])
        else:
            text = font.render("time survived: " + str(int(math.floor(mouse.objective["time"] / 60))) + ":" + str(mouse.objective["time"] % 60), 1, [255, 255, 255])
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
    elif mouse.objective["objective"] == "survival":
        text = font.render("cars passed: " + str(int(math.floor(mouse.score))), 1,
                           [255, 255, 255])
        window.blit(text, [20, 535])
        text = font.render("accidents: " + str(int(math.floor(mouse.accidents))), 1, [255, 255, 255])
        window.blit(text, [20, 560])
        if len(str(mouse.objective["time"] % 60)) == 1:
            text = font.render("time: " + str(int(math.floor(mouse.objective["time"] / 60))) + ":0" + str(
                mouse.objective["time"] % 60), 1, [255, 255, 255])
        else:
            text = font.render("time: " + str(int(math.floor(mouse.objective["time"] / 60))) + ":" + str(mouse.objective["time"] % 60), 1, [255, 255, 255])
        window.blit(text, [20, 510])
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

def getLevel(level):
    global roadgroup, cargroup, lightgroup, intersectiongroup, buildinggroup, mouse
    roadgroup, cargroup, lightgroup, intersectiongroup, buildinggroup, mouse.objective = levels.level(level)

getLevel(0)

while running:
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
                if event.key == pygame.K_r:
                    getLevel(level)
                    screen = "game"
            if screen == "you win":
                if event.key == pygame.K_m:
                    screen = "menu"
                    level = 0
                    getLevel(level)
                if event.key == pygame.K_r:
                    getLevel(level)
                    screen = "game"
                if event.key == pygame.K_n:
                    screen = "game"
                    level += 1
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse.move(event.pos[0], event.pos[1])
            if screen == "game":
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
                    getLevel(level)
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
                    screen = "menu"
                    level = 0
                    getLevel(level)
                    menuButton.clicked = False
                    mouse.reset_stats()
                replayButton.click()
                if replayButton.clicked:
                    mouse.reset_stats()
                    getLevel(level)
                    screen = "game"
                    replayButton.clicked = False
            if screen == "you win":
                menuButton.click()
                if menuButton.clicked:
                    screen = "menu"
                    level = 0
                    getLevel(level)
                    menuButton.clicked = False
                    mouse.reset_stats()
                replayButton.click()
                if replayButton.clicked:
                    mouse.reset_stats()
                    getLevel(level)
                    screen = "game"
                    replayButton.clicked = False
                nextLevelButton.click()
                if nextLevelButton.clicked:
                    level += 1
                    getLevel(level)
                    screen = "game"
                    nextLevelButton.clicked = False
                    mouse.reset_stats()
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
            if screen == "select":
                classic.click()
                if classic.clicked:
                    level = 1
                    getLevel(level)
                    screen = "game"
                survival.click()
                if survival.clicked:
                    level = "survival"
                    getLevel(level)
                    screen = "game"
                freeplay.click()
                if freeplay.clicked:
                    level = "freeplay"
                    getLevel(level)
                    screen = "game"

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
                    pos = i.rect.left + [20, 740][direction], i.rect.top + [4, 36][direction]
                    dir = [1, -1][direction]
                mouse.collide = False
                mouse.collidepoint = pos
                update(cargroup, "collidepoint")
                if not mouse.collide:
                    cargroup.add(entities.car(pos, i.orientation, dir, cargroup))
        if event.type == pygame.USEREVENT + 2:
            if screen == "game" and mouse.objective["time"] != "freeplay":
                if mouse.objective["objective"] == "survival":
                    mouse.objective["time"] += 1
                elif mouse.objective["objective"] != "survival":
                    if mouse.objective["time"] > 0:
                        mouse.objective["time"] -= 1
                if mouse.objective["time"] <= 0:
                    if mouse.objective["objective"] == "cars":
                        screen = "game over"
                        update(cargroup, "stop")
                    if mouse.objective["objective"] == "crashes":
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
        displayinfo()
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

    pygame.display.flip()

pygame.quit()