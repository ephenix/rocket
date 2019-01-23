import sys
import pygame
from rocket import rocket
from hud import hud
from world import world


pygame.init()
screen = pygame.display.set_mode((1024, 720))
game_state = 'run'
clock = pygame.time.Clock()

world1 = world()
rocket1 = rocket( world1 )


while game_state == 'run':
    clock.tick(60)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = 'quit'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                rocket1 = rocket( world )

    # logic
    currentcontrols = pygame.key.get_pressed()

    turn = 0.0
    accelerate = 0.0

    rocket1.update(turn, accelerate)

    world1.draw()
    rocket1.draw()
    

    pygame.display.flip()
