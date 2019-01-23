import pygame, math

class rocket:
    
    position = [ 0.0, 0.0 ]
    angle = 0.0
    world = None
    rocket_size = 5.0

    def __init__ ( self, world ):
        self.world = world
        origin = self.world.horizon_data[self.world.origin_index]
        self.position[0] = origin[0]
        self.position[1] = origin[1]

    def draw ( self ):
        point_list = [
            [ 0.0, -3.5 * self.rocket_size ],
            [ -1.0 * self.rocket_size, -3.0 * self.rocket_size ],
            [ -1.0 * self.rocket_size, 3.0 * self.rocket_size ],
            [ self.rocket_size, 3.0 * self.rocket_size ],
            [ self.rocket_size, -3.0 * self.rocket_size ],
        ]

        transformed_points = []
        
        for point in point_list:
            zoom = self.world.camera_zoom
            offset = self.world.camera_offset
            rotated_point = [ 
                ( math.cos( self.angle ) * ( point[0] - self.position[0] ) - math.sin( self.angle ) * ( point[1] - self.position[1] ) + self.position[0] ),
                ( math.sin( self.angle ) * ( point[0] - self.position[0] ) + math.cos( self.angle ) * ( point[1] - self.position[1] ) + self.position[1] )
            ]
            transformedpoint = [ ( rotated_point[0] * zoom ) - offset[0], ( rotated_point[1] * zoom ) - offset[1] ]
            transformed_points.append( transformedpoint )

        pygame.draw.polygon( self.world.screen, self.world.colors['white'], transformed_points )