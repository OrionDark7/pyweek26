import pygame, random
import structures, entities, levels

window = pygame.display.set_mode([800, 600])
window.fill([88, 198, 73])
running = True
mouse = [0, 0]
cargroup = pygame.sprite.Group()
roadgroup = pygame.sprite.Group()
lightgroup = pygame.sprite.Group()
pygame.time.set_timer(pygame.USEREVENT, 100)
pygame.time.set_timer(pygame.USEREVENT + 1, 750)

def update(group, action):
    global cargroup, roadgroup, lightgroup, mouse, window

    if group == cargroup:
        group.update(action, cargroup, mouse, lightgroup)
    elif group == lightgroup:
        group.update(action, window, mouse)
    else:
        group.update(action)

roadgroup, cargroup, lightgroup = levels.level(0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = event.pos[0], event.pos[1]
            update(cargroup, "kill")
            update(lightgroup, "toggle")
        if event.type == pygame.USEREVENT:
            update(cargroup, "accel")
        if event.type == pygame.USEREVENT + 1:
            for i in roadgroup:
                orientation = i.orientation
                direction = random.choice([0, 1])
                if i.orientation == "vertical":
                    pos = i.rect.left + [6, 36][direction], i.rect.top + [20, 580][direction]
                    dir = [1, -1][direction]
                elif i.orientation == "horizontal":
                    pos = i.rect.left + [20, 780][direction], i.rect.top + [6, 36][direction]
                    dir = [1, -1][direction]
                cargroup.add(entities.car(pos, i.orientation, dir, cargroup))

    roadgroup.draw(window)
    update(cargroup, "traffic")
    update(cargroup, "crash")
    update(cargroup, "drive")
    cargroup.draw(window)
    update(lightgroup, "draw")

    pygame.display.flip()

pygame.quit()