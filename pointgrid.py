class PointGrid:

    spacing_px = 100
    pointlist = []

    def __init__ ( self, size, spacing_px = 100 ):
        self.spacing_px = spacing_px
        size = int ( size / self.spacing_px )
        for y in range( -size, size ):
            for x in range( -size, size ):
                self.pointlist.append( [ ( x * self.spacing_px ), ( y * self.spacing_px ) ] )

    def get_points ( self, camera ):
        bounds = camera.getBounds()
        overflow = self.spacing_px * 2
        topleft = bounds[0]
        bottomright = bounds[1]
        returnlist = []
        for point in self.pointlist:
            if ( point[0] > ( topleft[0] - overflow ) and
                 point[0] < ( bottomright[0] + overflow ) and
                 point[1] > ( topleft[1] - overflow ) and
                 point[1] < ( bottomright[1] + overflow) ):
                returnlist.append( point )

        return returnlist
