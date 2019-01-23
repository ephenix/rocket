import pygame, math

class distancemarkers:
    
    units_per_km = 300.0

    world = None

    def __init__ ( self, world ):
        self.world = world
        self.units_per_km = world.units_per_km

    def draw ( self ):

        screen_x = self.world.screen.get_size()[0]
        screen_y = self.world.screen.get_size()[1]

        marker_effective_distance = self.units_per_km * self.world.camera_zoom
        num_markers = self.world.screen.get_size()[0] / marker_effective_distance
        
        start_x = self.world.camera_offset[0] - ( self.world.camera_offset[0] % self.units_per_km )
        x_list = []
        for i in range( int( num_markers ) + 2 ) :
            x1 = start_x + ( i * self.units_per_km )
            x_list.append( x1 )

        pygame.draw.rect( self.world.screen, self.world.colors['dark_grey'], [0,screen_y, screen_x, -35])
        pygame.draw.line( self.world.screen, self.world.colors['white'], [ 0, screen_y - 35], [screen_x, screen_y - 35] ) 

        for x in x_list:
            x1 = ( x - self.world.camera_offset[0] ) * self.world.camera_zoom
            rect = [ x1, screen_y, 5, -15 ]
            pygame.draw.rect( self.world.screen, self.world.colors['white'], rect)
            
            distance_text = str( int( x / self.units_per_km ) ) + " km"
            text_surface = self.world.small_font.render( distance_text, True, self.world.colors['white'] )
            self.world.screen.blit( text_surface, [ x1 - 5, screen_y - 34 ] )