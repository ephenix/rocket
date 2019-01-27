import sys
import pygame
from rocket import rocket
from distancemarkers import distancemarkers
from world import world

game_state = 'run'
clock = pygame.time.Clock()

world1 = world()
rocket1 = rocket( world1 )
distancemarkers1 = distancemarkers( world1 )

while game_state == 'run':
    clock.tick(60)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = 'quit'

    world1.draw()
    rocket1.draw()
    distancemarkers1.draw( )


    currentcontrols = pygame.key.get_pressed()


    if currentcontrols[pygame.K_UP]:
        world1.camera_offset[1] = world1.camera_offset[1] + ( 5.0 / world1.camera_zoom )
    if currentcontrols[pygame.K_DOWN]:
        world1.camera_offset[1] = world1.camera_offset[1] - ( 5.0 / world1.camera_zoom )
    if currentcontrols[pygame.K_LEFT]:
        world1.camera_offset[0] = world1.camera_offset[0] + ( 5.0 / world1.camera_zoom )
    if currentcontrols[pygame.K_RIGHT]:
        world1.camera_offset[0] = world1.camera_offset[0] - ( 5.0 / world1.camera_zoom )
    if currentcontrols[pygame.K_LCTRL]:
        world1.camera_zoom = world1.camera_zoom * 0.99
        world1.camera_offset[0] = world1.camera_offset[0] * 1.01
        world1.camera_offset[1] = world1.camera_offset[1] * 1.01
    if currentcontrols[pygame.K_LSHIFT]:
        world1.camera_zoom = world1.camera_zoom * 1.01
        world1.camera_offset[0] = world1.camera_offset[0] * 0.99
        world1.camera_offset[1] = world1.camera_offset[1] * 0.99


    pygame.display.flip()