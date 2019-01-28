import pygame, time, math, random
from camera import Camera
from world import World
from terrain import Terrain
from rocket import Rocket

world = World()
rocket = world.rocket

game_state = 'run'
clock = pygame.time.Clock()

while game_state == 'run':
    clock.tick(60)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = 'quit'
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            world.reset_rocket()
            rocket = world.rocket

    currentcontrols = pygame.key.get_pressed()
    
    accelerate = 0.0
    if currentcontrols[pygame.K_UP]:
        accelerate = 1.0
        if currentcontrols[pygame.K_LSHIFT]:
          accelerate = 2.0

    turn = 0.0
    if currentcontrols[pygame.K_LEFT]:
        turn = -1.0
    elif currentcontrols[pygame.K_RIGHT]:
        turn = 1.0

    #turning brake
    if currentcontrols[pygame.K_DOWN]:
        if rocket.angular_velocity > 0:
            turn = -1.0
        elif rocket.angular_velocity < 0:
            turn = 1.0

    rocket.update( turn, accelerate, world )
    world.camera.position = rocket.position

    if ( -rocket.position[1] < 250 ):
        zoomlevel = 2.0 + ( rocket.position[1] / 250 )
    elif ( 250 <= -rocket.position[1] < 500 ):
        zoomlevel = 1.0 + 0.5 * ( ( rocket.position[1] + 250 ) / 250 )
    elif ( 500 <= -rocket.position[1] <= 2000 ):
        zoomlevel = 0.5 + 0.4 * ( ( rocket.position[1] + 500 ) / 1500 )
    
    zoomlevel = max( 0.2 , min( zoomlevel, 1.0 - ( rocket.velocity / 500 ) ) )

    
    world.camera.zoom = zoomlevel
    

    world.draw()