import sys
import pygame
from rocket import rocket
from hud import hud


pygame.init()
screen = pygame.display.set_mode((1024, 720))
game_state = 'run'
clock = pygame.time.Clock()

world = {
    "origin": [ 20.0, 480.0 ],
    "screen": screen,
    'colors': {
        'black': (1, 1, 1),
        'grey': (128, 128, 128),
        'white': (222, 222, 222),
        'yellow': (192, 192, 12),
        'red': (252, 52, 12)
    },
    'font': pygame.font.SysFont('Arial', 14)
}

rocket1 = rocket( world )
hud1 = hud( world, rocket )


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
        if rocket1.angular_velocity > 0:
            turn = -1.0
        elif rocket1.angular_velocity < 0:
            turn = 1.0


    rocket1.update(turn, accelerate)

    # draw
    screen.fill(world['colors']['black'])
    pygame.draw.rect(screen, world['colors']['grey'], (0, 480, 1024, 480))

    rocket1.draw()
    hud1.draw( rocket1 )
    

    pygame.display.flip()
