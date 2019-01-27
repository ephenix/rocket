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
        return [ int( ( point[0] - self.position[0] ) * self.zoom - self.offset[0] ), -int( ( point[1] - self.position[1] ) * self.zoom + self.offset[1] )  ]


class Rocket:

    mass     = 800.0 #kg
    fuel     = 1000.0 #liters
    fuel_consumption = 5.0 #liters/s 
    fuel_consumption_current = 0.0 #current fuel consumption   
    angle = 0.0 #radians
    turn_responsiveness = 0.1 #radians/s/s 
    angular_velocity = 0.0 #angular velocity in radians/s
    lastupdate = None #Unix timestamp of last update
    time_multiplier = 3.0 #amount to multiply timespans by for faster physics
    is_accelerating = False #acceleration state -- whether to draw flame
    is_boosting = False #boost state -- whether to draw big flame

    def __init__ ( self, position = None, size = 5.0, fuel = 1000.0, thrust = 12000.0, angle = 0.0, mass = 800.0, vector = [0.0, 0.0], angular_velocity = 0 ):
        self.size = size
        self.mass = mass
        self.fuel = fuel
        self.angular_velocity = angular_velocity
        self.thrust = thrust
        self.angle = angle
        self.vector = vector
        if position is None:
            self.position = [ 0, -1 - self.size * 2 ]
        self.lastupdate = time.time()
    
    def accelerate ( self, throttle, turn, timespan ):
        if self.fuel > 0.0:
            thrust = self.thrust * throttle
        else:
            thrust = 0.0

        if abs( turn ) > 0.0:
            self.angular_velocity = self.angular_velocity + ( self.turn_responsiveness * turn * timespan )
        self.angle = self.angle + ( self.angular_velocity * timespan )

        fuel_use = 0.0
        self.fuel_consumption_current = fuel_use
        if throttle > 0.0:
            fuel_use = self.fuel_consumption * timespan * throttle
            self.is_accelerating = True
            if throttle > 1.0:
                self.is_boosting = True
            else:
                self.is_boosting = False
            self.fuel = self.fuel - fuel_use
        else:
            self.is_accelerating = False

        #find thrust components
        thrust_component_x = thrust * math.sin( self.angle )
        thrust_component_y = thrust * math.cos( self.angle )

        #find acceleration components
        acceleration_x = thrust_component_x / self.mass
        acceleration_y = thrust_component_y / self.mass

        #gravitational acceleration
        acceleration_g = -9.81
        acceleration_vector = [ acceleration_x, ( acceleration_y + acceleration_g ) ]

        #velocity = v0 + at
        self.vector[0] = self.vector[0] + ( acceleration_vector[0] * timespan )
        self.vector[1] = self.vector[1] - ( acceleration_vector[1] * timespan )

    def move ( self, timespan ):
        self.position[0] = self.position[0] + ( self.vector[0] * timespan )
        self.position[1] = self.position[1] + ( self.vector[1] * timespan )

        if self.position[1] >= 0.0:
            self.position[1] = 0
            self.vector[1] = 0.0
            self.vector[0] = 0.0
            self.angular_velocity = 0.0

    def update ( self, turn, accelerate ):
        currenttime = time.time()
        timespan = ( currenttime - self.lastupdate ) * self.time_multiplier
        self.lastupdate = currenttime
        self.accelerate( accelerate, turn, timespan )
        self.move( timespan )
    
    def get_points ( self, camera ):
        position = self.position
        offset = camera.offset
        zoom = camera.zoom
        
        points = [
            ( ( position[0] - self.size ), ( position[1] + self.size * 2.0 ) ),
            ( ( position[0] + self.size ), ( position[1] + self.size * 2.0 ) ),
            ( ( position[0] + self.size ), ( position[1] - self.size * 2.0 ) ),
            ( ( position[0]             ), ( position[1] - self.size * 3.0 ) ),
            ( ( position[0] - self.size ), ( position[1] - self.size * 2.0 ) )
        ]

        rotated = []
        for point in points:
            rotated.append( [
                ( ( math.cos( self.angle ) * ( point[0]-position[0] ) - math.sin( self.angle ) * ( point[1]-position[1] ) + position[0] ) - offset[0] ) * zoom ,
                ( ( math.sin( self.angle ) * ( point[0]-position[0] ) + math.cos( self.angle ) * ( point[1]-position[1] ) + position[1] ) - offset[1] ) * zoom
            ] )
        
        return rotated

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

class Terrain:

    def __init__ ( self, segment_size = 100, ruggedness = 50, horizon = None ):
        if horizon is None:
            self.horizon = [
                [ segment_size / -2, 0 ],
                [ segment_size /  2, 0 ]
            ]
        self.segment_size = segment_size
        self.ruggedness = ruggedness

    def get_points ( self, camera ):
        bounds = camera.getBounds()
        overflow = self.segment_size * 2
        topleft = bounds[0]
        bottomright = bounds[1]
        returnlist = []
        for point in self.horizon:
            if ( point[0] > ( topleft[0] - overflow ) and
                 point[0] < ( bottomright[0] + overflow ) and
                 point[1] > ( topleft[1] - overflow ) and
                 point[1] < ( bottomright[1] + overflow) ):
                returnlist.append( point )
                if point is self.horizon[0]:
                    self.generate( -1 )
                if point is self.horizon[1]:
                    self.generate( 1 )


        return returnlist

    def generate ( self, dir ):
        variation = random.randint(-30, 30)
        if dir == 1:
            frompoint = self.horizon[-1]
            topoint   = [ ( frompoint[0] + self.segment_size ), ( frompoint[1] + variation )]
            self.horizon.append( topoint )
        else:
            frompoint = self.horizon[0]
            topoint   = [ ( frompoint[0] - self.segment_size ), ( frompoint[1] + variation )]
            self.horizon.insert( 0, topoint )

class World:
    
    def __init__ ( self, size = [1600, 900] ):
        pygame.init()
        self.size = size
        self.screen = pygame.display.set_mode( size )
        self.camera = Camera( self.screen )
        self.grid = PointGrid( size[0] )
        self.rocket = Rocket()
        self.terrain = Terrain()

    def draw ( self ):

        font = pygame.font.SysFont('Arial', 12)
        
        self.screen.fill( (0,0,0) )
        
        points = self.grid.get_points( self.camera )

        for point in points:
            transformedpoint = self.camera.transformPoint( point )
            pygame.draw.circle( self.screen, (255,255,255), transformedpoint, int( 3.0*self.camera.zoom ) )
            text_surface = font.render( str( [int( point[0] ), int( point[1] ) ] ), True, (55,55,55) )
            self.screen.blit(text_surface, [transformedpoint[0] + 5*self.camera.zoom, transformedpoint[1]] )

        rocket_points = self.rocket.get_points( self.camera )
        rocket_transformed = []
        for point in rocket_points:
            rocket_transformed.append( self.camera.transformPoint( point ) )

        pygame.draw.lines( self.screen, (255,0,0), True, rocket_points )

        pygame.display.flip()
    
    def reset_rocket ( self ):
        self.rocket = Rocket()



world = World()
rocket = world.rocket

game_state = 'run'
clock = pygame.time.Clock()

while game_state == 'run':
    clock.tick(60)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = 'quit'
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            world.reset_rocket()
            rocket = world.rocket

    currentcontrols = pygame.key.get_pressed()
    
    accelerate = 0.0
    if currentcontrols[pygame.K_UP]:
        accelerate = 1.0
        if currentcontrols[pygame.K_LSHIFT]:
          accelerate = 2.0

    turn = 0.0
    if currentcontrols[pygame.K_LEFT]:
        turn = -1.0
    elif currentcontrols[pygame.K_RIGHT]:
        turn = 1.0

    #turning brake
    if currentcontrols[pygame.K_DOWN]:
        if rocket.angular_velocity > 0:
            turn = -1.0
        elif rocket.angular_velocity < 0:
            turn = 1.0

    rocket.update( turn, accelerate )
    world.camera.position = rocket.position
    
    world.draw()