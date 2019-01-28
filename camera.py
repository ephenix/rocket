import pygame, time, math, random
class Camera:

    def __init__ ( self,  screen, position = [0, 0], zoom = 1.0 ):
        self.position = position
        self.zoom = zoom
        self.screen = screen
        self.offset = [ screen.get_size()[0] / -2, screen.get_size()[1] / -2 ]

    def getCenter ( self ):
        return [ ( self.position[0] ), ( self.position[1] + self.offset[1] ) ]

    def getBounds ( self ):
        origin = [ ( self.position[0] + ( self.offset[0] / self.zoom ) ), ( self.position[1] + ( self.offset[1] / self.zoom ) ) ]
        bound  = [ ( self.position[0] - ( self.offset[0] / self.zoom ) ), ( self.position[1] - ( self.offset[1] / self.zoom ) ) ]
        return [ origin, bound ]

    def transformPoint ( self, point ):
        return [ int( ( point[0] - self.position[0] ) * self.zoom - self.offset[0] ), int( ( point[1] - self.position[1] ) * self.zoom - self.offset[1] )  ]