import pygame, random, math, sys, time

class Camera:

    position = None
    zoom     = None
    offset   = [0,0]

    def __init__ ( self, position = [0, 0], zoom = 1.0, offset = [0,0] ):
        self.position = position
        self.zoom = zoom
        self.offset = offset
    
    def virtual_position ( self ):
        return [ ( self.position[0] + self.offset[0] ), ( self.position[1] + self.offset[1] ) ]

class Terrain:

    horizon      = []
    segment_size = None
    ruggedness   = None

    def __init__ ( self, segment_size = 100, ruggedness = 50, horizon = None ):
        if horizon is None:
            self.horizon = [
                [ segment_size / -2, 0 ],
                [ segment_size /  2, 0 ]
            ]
        self.segment_size = segment_size
        self.ruggedness = ruggedness

    def get_terrain ( self, camera, size ):
        
        zoom = camera.zoom
        offset = camera.virtual_position()

        #get screen bounds
        origin = [ ( offset[0] / zoom ), ( offset[1] / zoom ) ]
        bound  = [ ( size[0] / zoom + offset[0] ), ( size[1] / zoom + offset[1] ) ]

        min = origin[0]
        max = bound[0]
        while self.horizon[0][0] > min - self.segment_size * 10 :
            self.generate(-1)
        while self.horizon[-1][0] < max + self.segment_size * 10 :
            self.generate(1)
        

        points = []
        for point in self.horizon:
            if (min - self.segment_size * 10) < point[0] < (max + self.segment_size * 10) :
                points.append( point )

        #transform terrain points by camera offset and zoom
        transformed = []
        for point in points:
            transformed.append( [ ( point[0] - offset[0] ) * zoom, ( point[1] - offset[1] ) * zoom ] )

        return transformed

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

class Rocket:

    position = []
    vector   = []
    thrust   = 12000.0
    mass     = 800.0 #kg
    fuel     = 1000.0 #liters
    fuel_consumption = 5.0 #liters/s 
    fuel_consumption_current = 0.0 #current fuel consumption
    size     = 15.0    
    angle = 0.0 #radians
    turn_responsiveness = 0.1 #radians/s/s 
    angular_velocity = 0.0 #angular velocity in radians/s
    lastupdate = None #Unix timestamp of last update
    time_multiplier = 3.0 #amount to multiply timespans by for faster physics
    is_accelerating = False #acceleration state -- whether to draw flame
    is_boosting = False #boost state -- whether to draw big flame

    def __init__ ( self, position = None, size = 5.0, fuel = 1000.0, thrust = 12000.0, angle = 0.0, vector = [0.0, 0.0] ):
        self.size = size
        self.fuel = fuel
        self.thrust = thrust
        self.angle = angle
        self.vector = vector
        if position is None:
            self.position = [ 0, -1 - self.size * 2 ]
        self.lastupdate = time.time()

    def turn ( self, direction, timespan ):
        if abs(direction) > 0:
            self.angular_velocity = self.angular_velocity + ( self.turn_responsiveness * direction * timespan )
        self.angle = self.angle + ( self.angular_velocity * timespan )
    
    def accelerate ( self, throttle, timespan ):
        if self.fuel > 0.0:
            thrust = self.thrust * throttle
        else:
            thrust = 0.0

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
        velocity_x = self.vector[0] + ( acceleration_vector[0] * timespan )
        velocity_y = self.vector[1] - ( acceleration_vector[1] * timespan )

        self.vector[0] = velocity_x
        self.vector[1] = velocity_y

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

        self.turn( turn, timespan )
        self.accelerate( accelerate, timespan )
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

class World:
    
    size    = None
    screen  = None
    camera  = None
    terrain = None
    rocket  = None

    def __init__ ( self, size = [1600, 900] ):
        pygame.init()
        self.size = size
        self.screen = pygame.display.set_mode( size )
        self.camera = Camera( offset = [ size[0] * -0.5, size[1] * -0.5 ] )
        self.terrain = Terrain()
        self.reset_rocket()

    def draw ( self ):
        terrain = self.terrain

        #clear the screen
        self.screen.fill( (0,0,0) )
        
        terrain_points = terrain.get_terrain( self.camera, self.size )

        pygame.draw.lines( self.screen, (255,0,0), False, terrain_points )
        
        rocketpoints = self.rocket.get_points( self.camera )

        pygame.draw.lines( self.screen, (255,0,0), True, rocketpoints )

        font = pygame.font.SysFont('Arial', 12)
        text_surface = font.render( "rocket_position: " + str( [int(self.rocket.position[0]), int(self.rocket.position[1])]), True, (255,255,255) )
        self.screen.blit(text_surface, [300, 300] )

        text_surface = font.render( "camera_position: " + str( [int(self.camera.position[0]), int(self.camera.position[1])]), True, (255,255,255) )
        self.screen.blit(text_surface, [300, 314] )

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
    zoomlevel = 1.0 / 1.0 + (rocket.position[1] / 100.0)
    world.camera.zoom = zoomlevel

    world.draw()