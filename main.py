import pygame, random, math, pickle
from time import sleep
import structures, entities, levels

#Copyright Orion Williams 2018

pygame.init()
pygame.font.init()
pygame.mixer.init()
window = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Road Rage")
window.fill([88, 198, 73])
running = True
show_me = False
setHighscore = False
sfx = True
enteringName = False
score = ""
screen = "menu"
previous = "menu"
placeSet = None
font = pygame.font.Font("./resources/Danger on the Motorway.otf", 16)
bkg = pygame.image.load("./images/bkg.png")
arrow = pygame.image.load("./images/arrow.png")
night_ = pygame.surface.Surface([800, 600])
night_setting = [200, 166, 133, 100, 66, 33, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 17, 33, 66, 100, 133, 166, 200, 217]
accidentpos = [0, 0]
tutorialindex = 0
dotutorial = False
lightswitch = pygame.mixer.Sound("./sfx/light-switch.wav")
motorcycle = pygame.mixer.Sound("./sfx/Motorcycle.wav")
car = pygame.mixer.Sound("./sfx/Car.wav")

scoreFile = open("./data/scores.dat", "rb")
try:
    highScores = pickle.load(scoreFile)
except:
    highScores = [[0, "player"], [0, "player"], [0, "player"], [0, "player"], [0, "player"]]
scoreFile.close()

volume = 5
oldvolume = 5
level = 0
page = 1
cargroup = pygame.sprite.Group()
roadgroup = pygame.sprite.Group()
lightgroup = pygame.sprite.Group()
intersectiongroup = pygame.sprite.Group()
buttongroup = pygame.sprite.Group()
buildinggroup = pygame.sprite.Group()
pygame.time.set_timer(pygame.USEREVENT, 100) #Acceleration
pygame.time.set_timer(pygame.USEREVENT + 1, 2250) #Car Spawn
pygame.time.set_timer(pygame.USEREVENT + 2, 1000) #Countdown
pygame.time.set_timer(pygame.USEREVENT + 3, 60000) #Time of Day change

class slider(pygame.sprite.Sprite):
    def __init__(self, pos, len, start):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface([10, 10])
        self.image.fill([255, 255, 255])
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(pos)
        self.pos = list(pos)
        self.length = len
        self.clicked = False
        self.boundaryrect = pygame.surface.Surface([self.length * 10, 15])
        self.boundaryrect = self.boundaryrect.get_rect()
        self.boundaryrect.left, self.boundaryrect.top = list(pos)
        self.where = start
        if start < len:
            self.rect.left += start * 10

    def draw(self):
        global window

        window.blit(self.image, [self.rect.left, self.rect.top + 3])

        pygame.draw.rect(window, [255, 255, 255], [self.pos[0], self.pos[1], (self.length * 10) + 6, 15], 2)

    def grab(self):
        global mouse
        if self.rect.collidepoint([mouse.rect.centerx, mouse.rect.centery]):
            self.clicked = True

    def drag(self):
        global mouse

        if self.clicked:
            if mouse.rect.left < self.boundaryrect.right - 6 and self.rect.left < self.boundaryrect.left + 3:
                self.rect.left = mouse.rect.centerx
            elif mouse.rect.left > self.boundaryrect.right - 6:
                self.rect.left = self.boundaryrect.right - 6
            elif mouse.rect.left > self.pos[0] + 3:
                self.rect.left = mouse.rect.centerx

            self.where = int(self.rect.left - self.pos[0]) / 10

class textbox(pygame.sprite.Sprite):
    def __init__(self, pos, text, len, max):
        global font
        pygame.sprite.Sprite.__init__(self)
        self.text = str(text)
        self.max = max
        self.image = font.render(str(self.text), 1, [255, 255, 255])
        self.underline = pygame.surface.Surface([len, 1])
        self.underline.fill([255, 255, 255])
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(pos)
    def draw(self):
        global window
        window.blit(self.image, [self.rect.left, self.rect.top])
        window.blit(self.underline, [self.rect.left, self.rect.top + 20])
    def write(self, char):
        allowed = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "[", "]", ";", "'", ",", ".", "/"]
        if len(self.text) < self.max:
            if str(char) in allowed:
                self.text = self.text + str(char)
            elif char == "space":
                self.text = self.text + " "
            elif char == "backspace":
                self.text = self.text[0 : len(self.text) - 1]
            self.image = font.render(str(self.text), 1, [255, 255, 255])

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
scoreButton = button("[v] view highscores", [400, 320], True)
enterButton = button("[e] enter name", [10, 290], False)
nextLevelButton = button("[n] next level", [400, 320], True)
closeButton = button("[c] close", [20, 45], False)
showButton = button("[s] show me", [180, 45], False)
playButton = button("[p] play game", [20, 70], False)
howButton = button("[h] how to play", [20, 100], False)
settingsButton = button("[s] settings", [20, 130], False)
quitButton = button("[q] quit game", [20, 160], False)
backButton = button("[b] back", [10, 10], False)
resumeButton = button("[r] resume game", [20, 70], False)
goalButton = button("[1] goal of the game", [10, 110], False)
exampleButton = button("[2] examples of level tasks", [10, 130], False)
controlButton = button("[3] controls", [10, 150], False)
mechanicsButton = button("[4] game mechanics", [10, 170], False)
carButton = button("[5] cars", [10, 190], False)
gamemodesButton = button("[6] gamemodes", [10, 210], False)
nextButton = button("[n] next", [20, 560], False)
skipButton = button("[x] skip tutorial", [140, 560], False)

name = textbox([10, 290], "player", 250, 20)

volumeSlider = slider([243, 188], 11, 5)

fullSwitch = switch([313, 98], False)
sfxSwitch = switch([313, 128], True)
keySwitch = switch([313, 158], True)

classic = imagebutton("./images/ui/buttons/classic.png", [80, 240], False)
survival = imagebutton("./images/ui/buttons/freeplay.png", [320, 240], False)
freeplay = imagebutton("./images/ui/buttons/freeplay.png", [560, 240], False)
level1 = imagebutton("./images/ui/buttons/level1.png", [32, 60], False)
level2 = imagebutton("./images/ui/buttons/level2.png", [224, 60], False)
level3 = imagebutton("./images/ui/buttons/level3.png", [416, 60], False)
level4 = imagebutton("./images/ui/buttons/level4.png", [608, 60], False)
level5 = imagebutton("./images/ui/buttons/level5.png", [32, 240], False)
level6 = imagebutton("./images/ui/buttons/level6.png", [224, 240], False)
level7 = imagebutton("./images/ui/buttons/level7.png", [416, 240], False)
level8 = imagebutton("./images/ui/buttons/level8.png", [608, 240], False)
level9 = imagebutton("./images/ui/buttons/level9.png", [32, 420], False)
level10 = imagebutton("./images/ui/buttons/level10.png", [224, 420], False)
level11 = imagebutton("./images/ui/buttons/level11.png", [416, 420], False)
level12 = imagebutton("./images/ui/buttons/level12.png", [608, 420], False)

def readableTime(time):
    if len(str(int(math.floor(time % 60)))) == 1:
        newtime = str(int(math.floor(time / 60))) + ":0" + str(int(math.floor(time % 60)))
    else:
        newtime = str(int(math.floor(time / 60))) + ":" + str(int(math.floor(time % 60)))
    return newtime

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

def intro():
    global mouse, level, sleep, volume
    window.fill([0, 0, 0])

    pygame.time.set_timer(pygame.USEREVENT + 1, 10000)
    pygame.time.set_timer(pygame.USEREVENT + 2, 10000)

    pygame.display.flip()
    sleep(2)

    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 32)

    if mouse.objective["objective"] != "freeplay" and mouse.objective["objective"] != "survival":
        text = font.render(
            "level " + str(level), 1,
            [255, 255, 255])
        rect = text.get_rect().width / 2
        window.blit(text, [400 - rect, 185])
    elif mouse.objective["objective"] == "freeplay":
        text = font.render(
            "freeplay mode", 1,
            [255, 255, 255])
        rect = text.get_rect().width / 2
        window.blit(text, [400 - rect, 185])
    elif mouse.objective["objective"] == "survival":
        text = font.render(
            "survival mode", 1,
            [255, 255, 255])
        rect = text.get_rect().width / 2
        window.blit(text, [400 - rect, 185])

    pygame.display.flip()

    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 16)

    sleep(2)

    if mouse.objective["objective"] == "cars":
        text = font.render(
            "level objective: get " + str(mouse.objective["amount"]) + " cars through the level", 1,
            [255, 255, 255])
        rect = text.get_rect().width / 2
        window.blit(text, [400 - rect, 230])
    elif mouse.objective["objective"] == "crashes":
        text = font.render(
            "level objective: avoid " + str(mouse.objective["amount"]) + " crashes until the time runs out", 1,
            [255, 255, 255])
        rect = text.get_rect().width / 2
        window.blit(text, [400 - rect, 230])
    elif mouse.objective["objective"] == "anger":
        text = font.render(
            "level objective: have less than " + str(mouse.objective["amount"]) + " angry drivers", 1,
            [255, 255, 255])
        rect = text.get_rect().width / 2
        window.blit(text, [400 - rect, 230])
        text = font.render(
            "until the time runs out", 1,
            [255, 255, 255])
        rect = text.get_rect().width / 2
        window.blit(text, [400 - rect, 250])
    elif mouse.objective["objective"] == "survival":
        text = font.render(
            "objective: survive for as long as you can without", 1,
            [255, 255, 255])
        rect = text.get_rect().width / 2
        window.blit(text, [400 - rect, 230])
        text = font.render(
            "any accidents", 1,
            [255, 255, 255])
        rect = text.get_rect().width / 2
        window.blit(text, [400 - rect, 250])
    elif mouse.objective["objective"] == "freeplay":
        text = font.render(
            "objective: have fun! it's freeplay mode!", 1,
            [255, 255, 255])
        rect = text.get_rect().width / 2
        window.blit(text, [400 - rect, 230])
    pygame.display.flip()


    sleep(3)
    
    for i in range(20):
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

        rect = pygame.surface.Surface([800 - (40 * i), 600 - (30 * i)])
        window.blit(rect, [0 + (i * 20), 0 + (i * 15)])
        pygame.display.flip()

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
    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 16)
    text = font.render(
        "click on a topic below to read about it:", 1,
        [255, 255, 255])
    window.blit(text, [10, 70])
    backButton.draw()
    goalButton.draw()
    exampleButton.draw()
    mechanicsButton.draw()
    controlButton.draw()
    carButton.draw()
    gamemodesButton.draw()

def howPageScreen(screen):
    rect = pygame.surface.Surface([800, 600])
    rect.fill([0, 0, 0])
    rect.set_alpha(200)
    window.blit(rect, [0, 0])
    backButton.draw()
    fontbig = pygame.font.Font("./resources/Danger on the Motorway.otf", 32)
    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 16)
    if screen == 1:
        text = fontbig.render(
            "goal of the game", 1,
            [255, 255, 255])
        rect = 400 - text.get_rect().width / 2
        window.blit(text, [rect, 10])

        text = font.render("the goal of the game is to clear all the levels by completing", 1, [255, 255, 255])
        window.blit(text, [10, 70])
        text = font.render("the different tasks defined for each level.", 1, [255, 255, 255])
        window.blit(text, [10, 90])

        text = font.render("all of these tasks will be mentioned in the next section.", 1, [255, 255, 255])
        window.blit(text, [10, 130])

    elif screen == 2:
        text = fontbig.render(
            "examples of level tasks", 1,
            [255, 255, 255])
        rect = 400 - text.get_rect().width / 2
        window.blit(text, [rect, 10])

        text = font.render("to complete each level, you have to complete a certain task.", 1, [255, 255, 255])
        window.blit(text, [10, 70])
        text = font.render("each task is defined below:", 1, [255, 255, 255])
        window.blit(text, [10, 90])

        text = font.render("1. Get a certain amount of cars to the exit before time runs out.", 1, [255, 255, 255])
        window.blit(text, [10, 130])

        text = font.render("2. survive a certain amount of accidents until the timer", 1, [255, 255, 255])
        window.blit(text, [10, 170])
        text = font.render("runs out.", 1, [255, 255, 255])
        window.blit(text, [10, 190])

        text = font.render("3. have less than a certain amount of angry drivers before the", 1, [255, 255, 255])
        window.blit(text, [10, 230])
        text = font.render("time runs out.", 1, [255, 255, 255])
        window.blit(text, [10, 250])

    elif screen == 3:
        text = fontbig.render(
            "controls", 1,
            [255, 255, 255])
        rect = 400 - text.get_rect().width / 2
        window.blit(text, [rect, 10])

        text = font.render("left click: toggle traffic lights [1]", 1, [255, 255, 255])
        window.blit(text, [10, 70])
        text = font.render("right click: clear crashed cars [2]", 1, [255, 255, 255])
        window.blit(text, [10, 110])
        text = font.render("escape key: pause game [3]", 1, [255, 255, 255])
        window.blit(text, [10, 150])

        image = pygame.image.load("./images/ui/how-to/controls.png")
        window.blit(image, [500, 70])

    elif screen == 4:
        text = fontbig.render(
            "game mechanics", 1,
            [255, 255, 255])
        rect = 400 - text.get_rect().width / 2
        window.blit(text, [rect, 10])

        text = font.render("traffic lights:  they control the flow of traffic. toggle them", 1, [255, 255, 255])
        window.blit(text, [10, 70])
        text = font.render("from red to green to red and vice versa, by left clicking them.", 1, [255, 255, 255])
        window.blit(text, [10, 90])
        text = font.render("one important note, clicking the intersection will switch both", 1, [255, 255, 255])
        window.blit(text, [10, 110])
        text = font.render("lights at that intersection, while just clicking one light", 1, [255, 255, 255])
        window.blit(text, [10, 130])
        text = font.render("individually will switch just that light.", 1,
                           [255, 255, 255])
        window.blit(text, [10, 150])

        text = font.render("car accidents:  car accidents happen when two cars collide,", 1, [255, 255, 255])
        window.blit(text, [10, 190])
        text = font.render("stopping all traffic behind them. cars that have been in", 1, [255, 255, 255])
        window.blit(text, [10, 210])
        text = font.render("accidents will be identified by a yellow warning sign above", 1, [255, 255, 255])
        window.blit(text, [10, 230])
        text = font.render("them. right click on those cars to clear an accident.", 1, [255, 255, 255])
        window.blit(text, [10, 250])

        text = font.render("angry drivers:  angry drivers happen when a driver is stopped", 1, [255, 255, 255])
        window.blit(text, [10, 290])
        text = font.render("for too long. cars with angry drivers will be identified by", 1, [255, 255, 255])
        window.blit(text, [10, 310])
        text = font.render("a red, frowny face above them. angry drivers penalize how", 1, [255, 255, 255])
        window.blit(text, [10, 330])
        text = font.render('much time is left on a level, but they can be "calmed down"', 1, [255, 255, 255])
        window.blit(text, [10, 350])
        text = font.render("by restoring the flow of traffic in front of them.", 1, [255, 255, 255])
        window.blit(text, [10, 370])

        image = pygame.image.load("./images/ui/how-to/traffic lights.png")
        window.blit(image, [80, 430])

        image = pygame.image.load("./images/ui/how-to/accident.png")
        window.blit(image, [320, 430])

        image = pygame.image.load("./images/ui/how-to/angry drivers.png")
        window.blit(image, [540, 430])
    elif screen == 5:
        text = fontbig.render(
            "cars", 1,
            [255, 255, 255])
        rect = 400 - text.get_rect().width / 2
        window.blit(text, [rect, 10])

        text = font.render("there are three main different types of cars in the game.", 1, [255, 255, 255])
        window.blit(text, [10, 70])

        text = font.render("normal cars: normal cars drive at average speeds and take", 1, [255, 255, 255])
        window.blit(text, [10, 110])
        text = font.render("up some space.", 1, [255, 255, 255])
        window.blit(text, [10, 130])

        image = pygame.image.load("./images/cars/red/car-right.png")
        window.blit(image, [10, 150])

        text = font.render("buses: buses drive at slow speeds and take up twice as much", 1, [255, 255, 255])
        window.blit(text, [10, 190])
        text = font.render("space as normal cars.", 1, [255, 255, 255])
        window.blit(text, [10, 210])

        image = pygame.image.load("./images/cars/transit/car-right.png")
        window.blit(image, [10, 230])

        text = font.render("motorcycles: motorcycles drive at relatively fast speeds and", 1, [255, 255, 255])
        window.blit(text, [10, 270])
        text = font.render("take up little space.", 1, [255, 255, 255])
        window.blit(text, [10, 290])

        image = pygame.image.load("./images/cars/motorcycle-red/bike-right.png")
        window.blit(image, [10, 310])

    elif screen == 6:
        text = fontbig.render(
            "gamemodes", 1,
            [255, 255, 255])
        rect = 400 - text.get_rect().width / 2
        window.blit(text, [rect, 10])

        text = font.render("there are three different playable gamemodes in the game.", 1, [255, 255, 255])
        window.blit(text, [10, 70])

        text = font.render("classic mode: classic mode is the original 12 game levels", 1, [255, 255, 255])
        window.blit(text, [10, 110])
        text = font.render("with different challenges.", 1, [255, 255, 255])
        window.blit(text, [10, 130])

        text = font.render("survival mode: survival mode is one level where players try", 1, [255, 255, 255])
        window.blit(text, [10, 170])
        text = font.render('to see how long they can "survive" before causing a', 1, [255, 255, 255])
        window.blit(text, [10, 190])
        text = font.render("car accident.", 1, [255, 255, 255])
        window.blit(text, [10, 210])

        text = font.render("freeplay mode: freeplay mode is a mode where you can practice", 1, [255, 255, 255])
        window.blit(text, [10, 250])
        text = font.render('playing the game or just mess around. you cannot lose in', 1, [255, 255, 255])
        window.blit(text, [10, 270])
        text = font.render("freeplay mode.", 1, [255, 255, 255])
        window.blit(text, [10, 290])

def highScore():
    global window
    rect = pygame.surface.Surface([800, 600])
    rect.fill([0, 0, 0])
    rect.set_alpha(200)
    window.blit(rect, [0, 0])

    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 32)
    text = font.render(
        "high score", 1,
        [255, 255, 255])
    rect = 400 - text.get_rect().width / 2
    window.blit(text, [rect, 10])

    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 16)
    text = font.render(
        "1. " + readableTime(highScores[0][0]) + " set by " + highScores[0][1], 1,
        [255, 255, 255])
    window.blit(text, [10, 70])
    text = font.render(
        "2. " + readableTime(highScores[1][0]) + " set by " + highScores[1][1], 1,
        [255, 255, 255])
    window.blit(text, [10, 100])
    text = font.render(
        "3. " + readableTime(highScores[2][0]) + " set by " + highScores[2][1], 1,
        [255, 255, 255])
    window.blit(text, [10, 130])
    text = font.render(
        "4. " + readableTime(highScores[3][0]) + " set by " + highScores[3][1], 1,
        [255, 255, 255])
    window.blit(text, [10, 160])
    text = font.render(
        "5. " + readableTime(highScores[4][0]) + " set by " + highScores[4][1], 1,
        [255, 255, 255])
    window.blit(text, [10, 190])
    backButton.draw()

    placeFollower = [None, "st", "nd", "rd", "th", "th"]

    if setHighscore and not enteringName:
        text = font.render(
            "congrats! you just set a new highscore for " + str(placeSet) + placeFollower[placeSet] + " place!", 1,
            [255, 255, 255])
        window.blit(text, [10, 230])
        text = font.render(
            "want to sign your name into the highscore board?", 1,
            [255, 255, 255])
        window.blit(text, [10, 250])
        enterButton.draw()

    if enteringName and setHighscore:
        text = font.render(
            "enter your name below, when you are finished press return.", 1,
            [255, 255, 255])
        window.blit(text, [10, 250])
        name.draw()

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

    pygame.draw.rect(window, [255, 255, 255], [33, 50, 333, 500], 2)

    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 16)

    text = font.render(
        "general", 1,
        [255, 255, 255])
    rect = text.get_rect().width / 2
    window.blit(text, [200 - rect, 60])

    text = font.render(
        "fullscreen", 1,
        [255, 255, 255])
    window.blit(text, [43, 100])
    fullSwitch.draw()

    text = font.render(
        "sfx", 1,
        [255, 255, 255])
    window.blit(text, [43, 130])
    sfxSwitch.draw()

    text = font.render(
        "keyboard shortcuts", 1,
        [255, 255, 255])
    window.blit(text, [43, 160])
    keySwitch.draw()

    text = font.render(
        "volume: " + str(volume), 1,
        [255, 255, 255])
    window.blit(text, [43, 190])
    volumeSlider.draw()

    pygame.draw.rect(window, [255, 255, 255], [433, 50, 333, 500], 2)

    text = font.render(
        "about", 1,
        [255, 255, 255])
    rect = text.get_rect().width / 2
    window.blit(text, [600 - rect, 60])

    text = font.render(
        "version 1.0, revised 10/27", 1,
        [255, 255, 255])
    window.blit(text, [443, 100])

    text = font.render(
        "copyright orion williams", 1,
        [255, 255, 255])
    window.blit(text, [443, 130])

    text = font.render(
        "created for pyweek 26", 1,
        [255, 255, 255])
    window.blit(text, [443, 160])

    text = font.render(
        "built in python and pygame", 1,
        [255, 255, 255])
    window.blit(text, [443, 220])

    text = font.render(
        "art made in photoshop", 1,
        [255, 255, 255])
    window.blit(text, [443, 250])

    text = font.render(
        "sound effects from:", 1,
        [255, 255, 255])
    window.blit(text, [443, 310])
    text = font.render(
        "- freesound.org", 1,
        [255, 255, 255])
    window.blit(text, [443, 340])
    text = font.render(
        "- created in bfxr", 1,
        [255, 255, 255])
    window.blit(text, [443, 370])
    text = font.render(
        "- earthcam outside wrigley", 1,
        [255, 255, 255])
    window.blit(text, [443, 400])
    text = font.render(
        "  field in chicago, il", 1,
        [255, 255, 255])
    window.blit(text, [443, 430])

    text = font.render(
        "http://pyweek.org/e/deep26", 1,
        [255, 255, 255])
    window.blit(text, [443, 490])
    text = font.render(
        "http://oriondark7.com/", 1,
        [255, 255, 255])
    window.blit(text, [443, 520])

def menuScreen():
    global window
    rect = pygame.surface.Surface([235, 180])
    rect.fill([0, 0, 0])
    rect.set_alpha(200)
    window.blit(rect, [10, 10])
    playButton.draw()
    howButton.draw()
    settingsButton.draw()
    quitButton.draw()
    font = pygame.font.Font("./resources/Danger on the Motorway.otf", 32)
    text = font.render(
        "road rage", 1,
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
    if mouse.objective["objective"] == "survival":
        scoreButton.draw()

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
    if level < 12:
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

def tutorial():
    global window, tutorialindex, dotutorial
    rect = pygame.surface.Surface([780, 80])
    rect.fill([0, 0, 0])
    rect.set_alpha(200)
    window.blit(rect, [10, 502])
    alltext = ["welcome to road rage! click next to begin.",
               "road rage is a game all about managing the flow of traffic.",
               "right now, the flow is stopped! let's fix that.",
               "click on any one of the red rectangles that you see.",
               "nice! we got one lane of traffic going now.",
               "now, we can get the other lane of traffic flowing as well!",
               "click on the intersection (except for the red rectangles).",
               "awesome! now the other lane is flowing smoothly now!",
               "it looks like, you've got the hang of it, so i'll be off.",
               "oh! i forgot, if you have an accident, right click to clear it.",
               "be sure to right click both of the crashed cars, not just one.",
               "you can also pause at any time by pressing the escape key.",
               "that's it! good luck!"]
    if tutorialindex >= len(alltext):
        dotutorial = False
    else:
        text = font.render(alltext[tutorialindex], 1, [255, 255, 255])
        window.blit(text, [20, 512])
        nextButton.draw()
        skipButton.draw()

def night(a):
    # A night time overdrop to make it seem dark
    global night_
    night_.fill([29, 66, 124])
    night_.set_alpha(a)
    window.blit(night_, [0, 0])

def background():
    window.blit(bkg, [0, 0])

def update(group, action):
    global cargroup, roadgroup, lightgroup, mouse, window, volume

    oldvolume = volume

    if not sfx:
        volume = 0.0

    if group == cargroup:
        group.update(action, cargroup, mouse, lightgroup, window, volume)
    elif group == lightgroup:
        group.update(action, window, mouse, volume)
    else:
        group.update(action)

    volume = oldvolume

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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if screen == "settings" and keySwitch.state:
                if event.key == pygame.K_b:
                    screen = previous
            if screen == "how" and keySwitch.state:
                if event.key == pygame.K_b:
                    screen = previous
                if event.key == pygame.K_1:
                    screen = "how page"
                    page = 1
                if event.key == pygame.K_2:
                    screen = "how page"
                    page = 2
                if event.key == pygame.K_3:
                    screen = "how page"
                    page = 3
                if event.key == pygame.K_4:
                    screen = "how page"
                    page = 4
                if event.key == pygame.K_5:
                    screen = "how page"
                    page = 5
                if event.key == pygame.K_6:
                    screen = "how page"
                    page = 6
            if screen == "how page" and keySwitch.state:
                if event.key == pygame.K_b:
                    screen = "how"
            if screen == "game over" and keySwitch.state:
                if event.key == pygame.K_m:
                    if mouse.objective["objective"] == "survival":
                        screen = "select"
                    else:
                        screen = "select level"
                    level = 0
                    getLevel(level)
                    mouse.score = 0
                    mouse.angry = pygame.sprite.Group()
                if event.key == pygame.K_r:
                    getLevel(level)
                    screen = "intro"
                    mouse.score = 0
                    mouse.angry = pygame.sprite.Group()
                if event.key == pygame.K_v and mouse.objective["objective"] == "survival":
                    screen = "high score"
            if screen == "high score":
                if enteringName:
                    name.write(pygame.key.name(event.key))
                if event.key == pygame.K_b and not enteringName and keySwitch.state:
                    screen = "game over"
                if event.key == pygame.K_e and not enteringName and keySwitch.state:
                    enteringName = True
                if event.key == pygame.K_RETURN and enteringName:
                    enteringName = False
                    highScores[placeSet - 1] = highScores[placeSet - 1][0], name.text
                    placeSet = 6
                    setHighscore = False
            if screen == "you win" and keySwitch.state:
                if event.key == pygame.K_m:
                    screen = "select level"
                    level = 0
                    getLevel(level)
                    mouse.score = 0
                    mouse.angry = pygame.sprite.Group()
                if event.key == pygame.K_r:
                    getLevel(level)
                    screen = "intro"
                    mouse.score = 0
                    mouse.angry = pygame.sprite.Group()
                if event.key == pygame.K_n and level < 12:
                    screen = "intro"
                    level += 1
                    getLevel(level)
                    mouse.score = 0
                    mouse.angry = pygame.sprite.Group()
            if screen == "select level" and keySwitch.state:
                if event.key == pygame.K_b:
                    screen = "select"
            elif screen == "select" and keySwitch.state:
                if event.key == pygame.K_c:
                    screen = "select level"
                    #screen = "intro"
                    #level = 1
                    #getLevel(level)
                if event.key == pygame.K_s:
                    screen = "intro"
                    level = "survival"
                    getLevel(level)
                if event.key == pygame.K_f:
                    screen = "intro"
                    level = "freeplay"
                    getLevel(level)
                if event.key == pygame.K_b:
                    screen = "menu"
                    level = 0
                    getLevel(level)
            if screen == "menu" and keySwitch.state:
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
                if mouse.accident and screen == "game" and keySwitch.state:
                    if event.key == pygame.K_c:
                        mouse.accident = False
                        show_me = False
                    if event.key == pygame.K_s:
                        show_me = True
                        accidentpos = [mouse.accidentinfo[0] - 30, mouse.accidentinfo[1] - 80]
                if dotutorial and keySwitch.state:
                    if event.key == pygame.K_n:
                        tutorialindex += 1
                    if event.key == pygame.K_x:
                        dotutorial = False
            elif screen == "pause" and keySwitch.state:
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
            elif screen == "pause" and not keySwitch.state:
                if event.key == pygame.K_ESCAPE:
                    screen = "game"
        if event.type == pygame.MOUSEBUTTONUP:
            if screen == "settings":
                volumeSlider.clicked = False
                volume = volumeSlider.where
                if mouse.rect.colliderect(volumeSlider.rect):
                    if sfx:
                        lightswitch.set_volume(float(volume * 0.1))
                        lightswitch.play()
        if event.type == pygame.MOUSEMOTION:
            mouse.move(event.pos[0], event.pos[1])
            if screen == "settings":
                volumeSlider.drag()
                volume = volumeSlider.where
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
                    if level == 1:
                        nextButton.click()
                        if nextButton.clicked:
                            tutorialindex += 1
                            nextButton.clicked = False
                        skipButton.click()
                        if skipButton.clicked:
                            dotutorial = False
                            skipButton.clicked = False
                elif screen == "menu":
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
                elif screen == "pause":
                    resumeButton.click()
                    if resumeButton.clicked:
                        screen = "pause"
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
                elif screen == "game over":
                    menuButton.click()
                    if menuButton.clicked:
                        mouse.reset_stats()
                        screen = "select level"
                        level = 0
                        getLevel(level)
                        menuButton.clicked = False
                        mouse.score = 0
                        mouse.angry = pygame.sprite.Group()
                    replayButton.click()
                    if replayButton.clicked:
                        mouse.reset_stats()
                        getLevel(level)
                        screen = "intro"
                        replayButton.clicked = False
                        mouse.score = 0
                        mouse.angry = pygame.sprite.Group()
                    scoreButton.click()
                    if scoreButton.clicked:
                        screen = "high score"
                        scoreButton.clicked = False
                elif screen == "you win":
                    menuButton.click()
                    if menuButton.clicked:
                        mouse.reset_stats()
                        screen = "select level"
                        level = 0
                        getLevel(level)
                        menuButton.clicked = False
                        mouse.score = 0
                        mouse.angry = pygame.sprite.Group()
                    replayButton.click()
                    if replayButton.clicked:
                        mouse.reset_stats()
                        getLevel(level)
                        screen = "intro"
                        replayButton.clicked = False
                        mouse.score = 0
                        mouse.angry = pygame.sprite.Group()
                    nextLevelButton.click()
                    if nextLevelButton.clicked and level < 12:
                        level += 1
                        getLevel(level)
                        screen = "intro"
                        nextLevelButton.clicked = False
                        mouse.score = 0
                        mouse.angry = pygame.sprite.Group()
                elif screen == "settings":
                    volumeSlider.grab()
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
                    sfxSwitch.toggle()
                    if sfxSwitch.clicked:
                        sfx = sfxSwitch.state
                        sfxSwitch.clicked = False
                    keySwitch.toggle()
                    if keySwitch.clicked:
                        keySwitch.clicked = False
                elif screen == "how":
                    backButton.click()
                    if backButton.clicked:
                        screen = previous
                        backButton.clicked = False
                    goalButton.click()
                    if goalButton.clicked:
                        screen = "how page"
                        page = 1
                        goalButton.clicked = False
                    exampleButton.click()
                    if exampleButton.clicked:
                        screen = "how page"
                        page = 2
                        exampleButton.clicked = False
                    controlButton.click()
                    if controlButton.clicked:
                        screen = "how page"
                        page = 3
                        controlButton.clicked = False
                    mechanicsButton.click()
                    if mechanicsButton.clicked:
                        screen = "how page"
                        page = 4
                        mechanicsButton.clicked = False
                    carButton.click()
                    if carButton.clicked:
                        screen = "how page"
                        page = 5
                        carButton.clicked = False
                    gamemodesButton.click()
                    if gamemodesButton.clicked:
                        screen = "how page"
                        page = 6
                        gamemodesButton.clicked = False
                elif screen == "how page":
                    backButton.click()
                    if backButton.clicked:
                        screen = "how"
                        backButton.clicked = False
                elif screen == "select level":
                    backButton.click()
                    if backButton.clicked:
                        screen = "select"
                        backButton.clicked = False
                elif screen == "high score":
                    backButton.click()
                    if backButton.clicked:
                        screen = "game over"
                        backButton.clicked = False
                    enterButton.click()
                    if enterButton.clicked:
                        enteringName = True
                        enterButton.clicked = False
                if screen == "select":
                    classic.click()
                    if classic.clicked:
                        screen = "select level"
                        #screen = "intro"
                        #level = 1
                        #getLevel(level)
                        classic.clicked = False
                    survival.click()
                    if survival.clicked:
                        mouse.reset_stats()
                        level = "survival"
                        getLevel(level)
                        screen = "intro"
                        survival.clicked = False
                    freeplay.click()
                    if freeplay.clicked:
                        mouse.reset_stats()
                        level = "freeplay"
                        getLevel(level)
                        screen = "intro"
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
                        screen = "intro"
                        getLevel(level)
                        level1.clicked = False
                        dotutorial = True
                        tutorialindex = True
                    level2.click()
                    if level2.clicked:
                        level = 2
                        screen = "intro"
                        getLevel(level)
                        level2.clicked = False
                    level3.click()
                    if level3.clicked:
                        level = 3
                        screen = "intro"
                        getLevel(level)
                        level3.clicked = False
                    level4.click()
                    if level4.clicked:
                        level = 4
                        screen = "intro"
                        getLevel(level)
                        level4.clicked = False
                    level5.click()
                    if level5.clicked:
                        level = 5
                        screen = "intro"
                        getLevel(level)
                        level5.clicked = False
                    level6.click()
                    if level6.clicked:
                        level = 6
                        screen = "intro"
                        getLevel(level)
                        level6.clicked = False
                    level7.click()
                    if level7.clicked:
                        level = 7
                        screen = "intro"
                        getLevel(level)
                        level7.clicked = False
                    level8.click()
                    if level8.clicked:
                        level = 8
                        screen = "intro"
                        getLevel(level)
                        level8.clicked = False
                    level9.click()
                    if level9.clicked:
                        level = 9
                        screen = "intro"
                        getLevel(level)
                        level9.clicked = False
                    level10.click()
                    if level10.clicked:
                        level = 10
                        screen = "intro"
                        getLevel(level)
                        level10.clicked = False
                    level11.click()
                    if level11.clicked:
                        level = 11
                        screen = "intro"
                        getLevel(level)
                        level11.clicked = False
                    level12.click()
                    if level12.clicked:
                        level = 12
                        screen = "intro"
                        getLevel(level)
                        level12.clicked = False
            elif clicked[2] == 1:
                if screen == "game":
                    update(cargroup, "kill")

        if event.type == pygame.USEREVENT:
            update(cargroup, "accel")
        if event.type == pygame.USEREVENT + 1 and screen == "game" or screen == "menu":
            pygame.time.set_timer(pygame.USEREVENT + 1, 2250)
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
            if screen == "game":
                update(cargroup, "wait")
            pygame.time.set_timer(pygame.USEREVENT + 2, 1000)
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
        if dotutorial and level == 1:
            tutorial()
        else:
            displayinfo()
        if mouse.objective["objective"] == "anger" and mouse.objective["amount"] - len(mouse.angry) <= 0:
            screen = "game over"
            update(cargroup, "stop")
        if mouse.objective["objective"] == "cars" and mouse.objective["amount"] <= 0:
            screen = "you win"
            update(cargroup, "stop")
        if mouse.objective["objective"] == "crashes" and mouse.objective["amount"] < 1:
            screen = "game over"
            update(cargroup, "stop")
        if mouse.accident:
            if mouse.objective["objective"] == "survival":
                screen = "game over"
                update(cargroup, "stop")
                score = mouse.objective["time"]
                if score > highScores[0][0]:
                    highScores[4] = highScores[3]
                    highScores[3] = highScores[2]
                    highScores[2] = highScores[1]
                    highScores[1] = highScores[0]
                    highScores[0] = score, "player"
                    setHighscore = True
                    placeSet = 1
                elif score > highScores[1][0]:
                    highScores[4] = highScores[3]
                    highScores[3] = highScores[2]
                    highScores[2] = highScores[1]
                    highScores[1] = score, "player"
                    setHighscore = True
                    placeSet = 2
                elif score > highScores[2][0]:
                    highScores[4] = highScores[3]
                    highScores[3] = highScores[2]
                    highScores[2] = score, "player"
                    setHighscore = True
                    placeSet = 3
                elif score > highScores[3][0]:
                    highScores[4] = highScores[3]
                    highScores[3] = score, "player"
                    setHighscore = True
                    placeSet = 4
                elif score > highScores[4][0]:
                    highScores[4] = score, "player"
                    setHighscore = True
                    placeSet = 5
                if len(str(int(math.floor(mouse.objective["time"] % 60)))) == 1:
                    score = str(int(math.floor(mouse.objective["time"] / 60))) + ":0" + str(int(math.floor(
                            mouse.objective["time"] % 60)))
                else:
                    score = str(int(math.floor(mouse.objective["time"] / 60))) + ":" + str(
                        int(math.floor(mouse.objective["time"] % 60)))
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
        update(cargroup, "stop")

    if screen == "how page":
        background()
        update(cargroup, "stop")
        howPageScreen(page)

    if screen == "settings":
        background()
        settingsScreen()
        update(cargroup, "stop")


    if screen == "pause":
        background()
        roadgroup.draw(window)
        intersectiongroup.draw(window)
        buildinggroup.draw(window)
        update(cargroup, "draw")
        update(lightgroup, "draw")
        night(night_setting[mouse.objective["tod"]])
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
        update(cargroup, "stop")

    if screen == "intro":
        window.fill([0, 0, 0])
        if sfx:
            playchoice = random.randint(0, 1)
            if playchoice == 0:
                car.play()
            elif playchoice == 1:
                motorcycle.play()
        intro()
        screen = "game"
        update(cargroup, "stop")

    if screen == "high score":
        background()
        highScore()
        update(cargroup, "stop")

    pygame.display.flip()

scoreFile = open("./data/scores.dat", "wb")
pickle.dump(highScores, scoreFile)
scoreFile.close()

pygame.quit()
