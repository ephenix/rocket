import pygame, math

class hud:

    world = None

    size = [250, 150]


    # topleft, topright, bottomleft, bottomright
    padding = 20
    position = [0, 0]
    relative_position = None

    def __init__( self, world, rocket, relative_position = 'topright' ):
        self.world = world
        self.relative_position = relative_position
        if relative_position == 'topleft':
            self.position[0] = self.padding
            self.position[1] = self.padding
        elif relative_position == 'topright':
            self.position[0] = self.world['screen'].get_size()[0] - (self.size[0] + self.padding)
            self.position[1] = self.padding
        elif relative_position == 'bottomleft':
            self.position[0] = self.padding
            self.position[1] = self.world['screen'].get_size()[1] - (self.size[1] + self.padding)
        elif relative_position == 'bottomright':
            self.position[0] = self.world['screen'].get_size()[0] - (self.size[0] + self.padding)
            self.position[1] = self.world['screen'].get_size()[1] - (self.size[1] + self.padding)

    def draw ( self, rocket ):
      rect = ( self.position[0], self.position[1], self.size[0], self.size[1] )
      pygame.draw.rect( self.world['screen'], self.world['colors']['grey'], rect )
      text = []
      text.append( "Position: " + str( int( rocket.position[0] ) ) + "x, " + str( int( rocket.position[1] ) ) + "y" )
      text.append( "Velocity: " + str( round(rocket.velocity_vector[0], 0 ) ) + ", " + str( round( rocket.velocity_vector[1], 0 ) ) )
      text.append( "Angle: " + str ( round( math.degrees( rocket.angle ), 2 ) ) + " degrees" )
      text.append( "Angular Velocity: " + str ( round( rocket.angular_velocity, 2 ) ) + " rads/s" )
      text.append( "Fuel: " + str( round( rocket.fuel_quanity, 2 )))
      text.append( "Current Fuel Consumption: " + str ( round( rocket.fuel_consumption_current, 2 ) ) + "/s" )
      offset = self.world['font'].get_height()
      for line in text:
        text_surface = self.world['font'].render( line, True, self.world['colors']['black'] )
        self.world['screen'].blit(text_surface, (self.position[0]+self.world['font'].get_height(), self.position[1]+offset) )
        offset = offset + self.world['font'].get_height()