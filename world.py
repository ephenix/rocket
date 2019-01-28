import pygame, time, math, random
from camera import Camera
from terrain import Terrain
from rocket import Rocket
from hud import HUD

class World:
    
    def __init__ ( self, size = [1600, 900] ):
        pygame.init()
        self.size = size
        self.screen = pygame.display.set_mode( size )
        self.camera = Camera( self.screen )
        self.rocket = Rocket( position=[0,-25] )
        self.terrain = Terrain()
        self.hud = HUD( self.rocket, self.camera )

    def draw ( self ):        
        self.screen.fill( (0,0,0) )
        self.terrain.draw( self.camera )
        self.rocket.draw( self.camera )
        self.hud.draw( )
        pygame.display.flip()
    
    def reset_rocket ( self ):
        self.rocket = Rocket()
        self.rocket.vector = [0.0, 0.0]
        self.rocket.angular_velocity = 0.0
        self.hud.rocket = self.rocket
