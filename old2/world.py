import pygame, random, math

class world:
    screen = None
    colors = {
        'black': (1, 1, 1),
        'grey': (128, 128, 128),
        'medium_grey': (64, 64, 64),
        'dark_grey': (32, 32, 32),
        'white': (222, 222, 222),
        'yellow': (192, 192, 12),
        'red': (252, 52, 12)
    }
    pygame.init()
    font = pygame.font.SysFont('Arial', 14)
    small_font = pygame.font.SysFont('Arial', 8)

    units_per_km = 300.0
    origin_index = 1

    camera_zoom = 1.0
    camera_offset = []
    horizon_data = []
    
    def __init__ ( self, size = [ 1500, 700 ] ):
        self.screen = pygame.display.set_mode( size )
        self.camera_offset = [ -200, -1 * size[1]/2 ]
        self.generate_screen()

    def generate_screen ( self, direction = 1 ):
        
        if len( self.horizon_data ) == 0:
            start_point = [ 0, 0 ]
        elif direction == -1:
            start_point = self.horizon_data[0]
        elif direction == 1:
            start_point = self.horizon_data[-1]
        
        num_points = random.randint( 10, 20 )
        screen_width = self.screen.get_size()[0]
        segment_size = screen_width / num_points

        #create a list of x coordinates
        x_list = [ start_point[0], ]
        for i in range( num_points ):
            x_list.append( ( x_list[-1] + int( segment_size ) * direction ) )
        
        current_grade = 0.0
        current_y = start_point[1]
        for x in x_list :
            #if it's steep, make it more likely to level out.
            if current_grade > 45.0:
                current_grade = current_grade + random.uniform( -30.0, 10.0 )
            elif current_grade < -45.0:
                current_grade = current_grade + random.uniform( -10.0, 30.0 )
            else:
                current_grade = current_grade + random.uniform( -30.0, 30.0 )
            current_y = int( current_y + ( segment_size * math.sin( current_grade ) ) )

            if x == 0:
                self.horizon_data.append( [ int(-1 * segment_size), int(current_y) ] )
            if direction == -1:
                self.horizon_data.insert( 0, [ int(x), int(current_y) ] )
                self.origin_index = self.origin_index + 1
            elif direction == 1:
                self.horizon_data.append( [ int(x), int(current_y) ] )
            
    def draw ( self ):
        self.screen.fill(self.colors['dark_grey'])
        screen_x = self.screen.get_size()[0]
        screen_y = self.screen.get_size()[1]
        
        points_in_view = []
        for point in self.horizon_data:
            x1 = ( point[0] - self.camera_offset[0] ) * self.camera_zoom
            y1 = ( point[1] - self.camera_offset[1] ) * self.camera_zoom
            if ( screen_x * 2 ) > x1 > ( screen_x * -1 ) :
                if ( screen_y * 2 ) > y1 > ( screen_y * -1 ) :
                    points_in_view.append( [ x1, y1 ] )
                    index = self.horizon_data.index( point )
                    if index > ( len( self.horizon_data ) - 20 ):
                        self.generate_screen()
                    if index < 20:
                        self.generate_screen(-1)

        points_in_view.append( [ screen_x, screen_y - 35 ] )
        points_in_view.append( [ 0, screen_y - 35 ] )
        pygame.draw.polygon( self.screen, self.colors['grey'], points_in_view )