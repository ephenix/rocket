import pygame, time, math, random

class Terrain:

    def __init__ ( self, segment_size = 100, ruggedness = 50, horizon = None ):
        if horizon is None:
            self.horizon = [
                [ 0, -1 ],
                [ segment_size, 0 ]
            ]
        self.originindex = 0
        self.segment_size = segment_size
        self.ruggedness = ruggedness

    def draw ( self, camera ):
        bounds = camera.getBounds()
        overflow = self.segment_size * 2
        topleft = bounds[0]
        bottomright = bounds[1]
        points = []
        for point in self.horizon:
            if ( point[0] > ( topleft[0] - overflow ) and
                 point[0] < ( bottomright[0] + overflow ) and
                 point[1] > ( topleft[1] - overflow ) and
                 point[1] < ( bottomright[1] + overflow) ):
                points.append( point )
                if point is self.horizon[0]:
                    self.generate( -1 )
                if point is self.horizon[1]:
                    self.generate( 1 )
        terrain_transformed = []
        for point in points:
            terrain_transformed.append( camera.transformPoint( point ) )
        
        if len( terrain_transformed ) > 1:
            pygame.draw.lines( camera.screen, (0,200,50), False, terrain_transformed )

    def generate ( self, dir ):
        variation = random.randint(-self.ruggedness, self.ruggedness)
        if dir == 1:
            frompoint = self.horizon[-1]
            topoint   = [ ( frompoint[0] + self.segment_size ), ( frompoint[1] + variation )]
            self.horizon.append( topoint )
        else:
            frompoint = self.horizon[0]
            topoint   = [ ( frompoint[0] - self.segment_size ), ( frompoint[1] + variation )]
            self.originindex = self.originindex + 1
            self.horizon.insert( 0, topoint )