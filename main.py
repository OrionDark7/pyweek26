import pygame, random
import structures, entities, levels

window = pygame.display.set_mode([800, 600])
window.fill([88, 198, 73])
running = True
mouse = [0, 0]
pygame.time.set_timer(pygame.USEREVENT, 100)
pygame.time.set_timer(pygame.USEREVENT + 1, 750)

def update(group, action):
    global cargroup, roadgroup, mouse

    if group == cargroup:
        group.update(action, cargroup, mouse)
    else:
        group.update(action)

roadgroup, cargroup = levels.level(0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = event.pos[0], event.pos[1]
            update(cargroup, "kill")
        if event.type == pygame.USEREVENT:
            update(cargroup, "accel")
        if event.type == pygame.USEREVENT + 1:
            for i in roadgroup:
                orientation = i.orientation
                direction = random.choice([0, 1])
                if i.orientation == "vertical":
                    pos = i.rect.left + [6, 36][direction], i.rect.top + [-60, 660][direction]
                elif i.orientation == "horizontal":
                    pos = i.rect.left + [-60, 860][direction], i.rect.top + [6, 36][direction]
                cargroup.add(entities.car(pos, i.orientation))

    roadgroup.draw(window)
    update(cargroup, "crash")
    update(cargroup, "drive")
    cargroup.draw(window)

    pygame.display.flip()

pygame.quit()