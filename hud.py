import pygame, time, math, random

class HUD:

    def __init__ ( self, rocket, camera, font_size = 14, location = 'topright', size = [300, 300] ):
        self.rocket = rocket
        self.camera = camera
        self.padding = font_size * 2
        self.font = pygame.font.SysFont('Courier New', font_size)
        self.size = size
        screensize = camera.screen.get_size()
        if location == 'topright':
            self.position = [ screensize[0] - ( size[0] + self.padding ), self.padding ]
        elif location == 'topleft':
            self.position = [ self.padding, self.padding ]
        elif location == 'bottomright':
            self.position = [ screensize[0] - ( size[0] + self.padding ), screensize[1] - ( size[1] + self.padding ) ]
        elif location == 'bottomleft':
            self.position = [ self.padding, screensize[1] - ( size[1] + self.padding ) ]
        else:
            self.position = location

    def draw ( self ):
        screen = self.camera.screen
        rocket = self.rocket

        pygame.draw.rect( screen, (128,128,128), [self.position[0], self.position[1], self.size[0], self.size[1]] ) 
        
        elements = [
            "Altitude:     " + str ( round ( -1 * rocket.position[1], 1 ) ) + " m",
            "Velocity:     " + str ( round ( rocket.velocity, 1 ) ) + " m/s",
            "Angle:        " + str ( round( rocket.angle_deg, 1 ) ) + "°",
            "Angular Vel:  " + str ( round( math.degrees( rocket.angular_velocity ), 1 ) ) + "°/s",
            "Vel Vector:   " + str ( round( rocket.vector[0], 1 ) ) + "x, " + str( round( -rocket.vector[1], 1 ) ) + "y m/s",
            "Absolute Pos: " + str ( round( rocket.position[0] / 1000, 1 ) ) + "x, " + str( round( -rocket.position[1] / 1000, 1) ) + "y km",
            "Fuel:         " + str ( round( rocket.fuel ) ) + " l",
        ]

        indexmultiplier = 0
        for element in elements:
            indexmultiplier = indexmultiplier + 1
            textposition = ( self.position[0] + self.padding ), self.position[1] + ( indexmultiplier * self.padding * 1.2 )
            text = self.font.render( element, True, (255,255,255) )
            screen.blit( text, textposition )

        if self.camera.zoom < .75 or rocket.velocity > 100.0:
            circlesize = max( 15, int( 5 * rocket.size * self.camera.zoom ) )
            pygame.draw.circle( screen, (225,0,0), [-int(self.camera.offset[0]), -int(self.camera.offset[1])], circlesize, 1)

            angle = rocket.angle
            x = circlesize * math.sin( -angle )
            y = circlesize * math.cos( -angle )
            origin = [-int(self.camera.offset[0] + x), -int(self.camera.offset[1] + y)]
            point = [-int(self.camera.offset[0] + 2*x), -int(self.camera.offset[1] + 2*y)]
            pygame.draw.line( screen, (225,0,0), origin, point )

            velocity_multiplier = min( 5, rocket.velocity / 100.0 )
            vectorangle = 0.0
            if rocket.vector[1] != 0:
                vectorangle = math.atan( rocket.vector[0] / rocket.vector[1] )
            y_multiplier = 1.0
            if rocket.vector[1] > 0:
                y_multiplier = -1.0
            x = circlesize * math.sin( vectorangle ) * y_multiplier
            y = circlesize * math.cos( vectorangle ) * y_multiplier

            origin = [-int(self.camera.offset[0] + x), -int(self.camera.offset[1] + y)]
            point = [-int(self.camera.offset[0] + velocity_multiplier *x), -int(self.camera.offset[1] + velocity_multiplier * y)]
            pygame.draw.line( screen, (0,225,0), origin, point )

            