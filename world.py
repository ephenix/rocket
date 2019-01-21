import pygame, random

class world:

    screen = None

    default_size = 1500, 700

    horizon = []
    
    def __init__ ( self, size = None ):
        pygame.init()

        if size == None:
            size = self.default_size

        self.horizon.append( [ 0, size[1] / 2 ] )
        self.horizon.append( [ size[0], size[1] / 2 ] )
        
        self.screen = pygame.display.set_mode( size )

    def generate_screen ( self, direction ):
        
        if direction == 1 :
            datum = self.horizion[-1][1]
        elif direction == -1:
            datum = self.horizon[0][1]

        differential = ( random.randint( -1 * self.screen.get_size(), self.screen.get_size() ) )
        target_datum = datum + differential

        num_segments = random.randint(10,20)
        total_width = self.screen.get_size()[0]
        remaining_width = total_width
        remaining_differential = differential
        average_width = total_width / num_segments

    while remaining_width > 0 :
        segment_width = random.randint( average_width * 0.8, average_width * 1.2)
        remaining_width = remaining_width - segment_width




world1 = world()
game_state = 'run'
clock = pygame.time.Clock()

while game_state == 'run':
    clock.tick(60)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = 'quit'

    world1.screen.fill( (0,0,0) )

    pygame.display.flip()