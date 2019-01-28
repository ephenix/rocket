import pygame, time, math, random

class Rocket:

    def __init__ ( self, size = 10.0,
                         position = None,
                         fuel = 1000.0, 
                         thrust = 12000.0, 
                         angle = 0.0, 
                         mass = 800.0, 
                         vector = [0.0, 0.0], 
                         angular_velocity = 0.0, 
                         fuel_consumption = 5.0, 
                         turn_responsiveness = 0.1, 
                         time_multiplier = 3.0 ):
        self.size = size
        if position is None:
            self.position = [ 0.0, -1.0 - self.size * 2.0 ]
        else:
            self.position = position
        self.fuel = fuel
        self.thrust = thrust
        self.angle = angle
        self.mass = mass
        self.vector = vector
        self.angular_velocity = angular_velocity
        self.fuel_consumption = fuel_consumption
        self.velocity = math.sqrt( self.vector[0]**2 + self.vector[1]**2 )
        self.time_multiplier = time_multiplier
        self.turn_responsiveness = turn_responsiveness
        
        self.lastupdate = time.time()
        self.angle_deg = math.degrees( self.angle ) % 360
        self.fuel_consumption_current = 0.0
        self.is_accelerating = False
        self.is_boosting = False
        self.is_exploded = False
        self.altitude = 0.0
    
    def accelerate ( self, throttle, turn, timespan ):
        if self.fuel > 0.0:
            thrust = self.thrust * throttle
        else:
            thrust = 0.0

        if abs( turn ) > 0.0:
            self.angular_velocity = self.angular_velocity + ( self.turn_responsiveness * turn * timespan )
        self.angle = self.angle + ( self.angular_velocity * timespan )
        self.angle_deg = math.degrees( self.angle ) % 360

        fuel_use = 0.0
        self.fuel_consumption_current = fuel_use
        if throttle > 0.0:
            fuel_use = self.fuel_consumption * timespan * throttle
            self.is_accelerating = True
            if throttle > 1.0:
                self.is_boosting = True
            else:
                self.is_boosting = False
            if self.fuel > 0.0:
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

        self.velocity = math.sqrt( self.vector[0]**2 + self.vector[1]**2 )

    def move ( self, timespan, terrain ):
        horizon = terrain.horizon
        new_x = self.position[0] + ( self.vector[0] * timespan )
        new_y = self.position[1] + ( self.vector[1] * timespan )

        rotated = self.get_rotation( [new_x, new_y] )

        collision_detected = False
        if ( self.altitude > self.size * -5 ):
            for p in range ( len( rotated ) ):
                point1 = rotated[p]
                if p >= len(rotated)-1:
                    point2 = rotated[-1]
                else:
                    point2 = rotated[p+1]
                segment_a = [ point1, point2 ]

                i = int ( terrain.originindex + ( new_x / terrain.segment_size ) )
                if ( i >= len(horizon) ):
                    i = i - 1
                segment_b = [ horizon[i], horizon[i+1] ]
                collides = self.check_intersection( segment_a, segment_b )
                if collides != False:
                    collision_detected = True
                collides = self.check_intersection( segment_a, segment_b )

        if collision_detected:
            self.vector = [0.0, 0.0]
            self.angular_velocity = 0.0
            if self.velocity > 50.0:
                self.is_exploded = True
        else:
            self.position[0] = new_x
            self.position[1] = new_y

    def check_intersection(self, line1, line2):
        def line(p1, p2):
            A = (p1[1] - p2[1])
            B = (p2[0] - p1[0])
            C = (p1[0]*p2[1] - p2[0]*p1[1])
            return A, B, -C

        def intersection(L1, L2):
            D  = L1[0] * L2[1] - L1[1] * L2[0]
            Dx = L1[2] * L2[1] - L1[1] * L2[2]
            Dy = L1[0] * L2[2] - L1[2] * L2[0]
            if D != 0:
                x = Dx / D
                y = Dy / D
                return x,y
            else:
                return False
        
        def xdomain ( d1, d2 ):
            "checks two domain ranges to see if there is any overlap"
            return min(d2) < d1[0] < max(d2) or min(d2) < d1[1] < max(d2)
        
        x_domains = ( line1[0][0], line1[1][0] ), ( line2[0][0], line2[1][0] )
        y_domains = ( line1[0][1], line1[1][1] ), ( line2[0][1], line2[1][1] )
        if xdomain( x_domains[0], x_domains[1] ) and xdomain( y_domains[0], y_domains[1] ):
            l1 = line(line1[0], line1[1])
            l2 = line(line2[0], line2[1])
            return intersection(l1, l2)
        else:
            return False

    def get_altitude ( self, terrain ):
        rotated = self.get_rotation()
        rotated.sort( key = lambda x: x[1] )
        lowestpoint =  rotated[0][1]
        
        i = int ( terrain.originindex + ( self.position[0] / terrain.segment_size ) )
        groundlevel = terrain.horizon[i][1]
        self.altitude = lowestpoint - groundlevel

    def update ( self, turn, accelerate, world ):
        currenttime = time.time()
        timespan = min( 0.5, ( currenttime - self.lastupdate ) * self.time_multiplier )
        self.lastupdate = currenttime
        self.accelerate( accelerate, turn, timespan )
        self.move( timespan, world.terrain )
        self.get_altitude( world.terrain )
    
    def draw ( self, camera ):
        if self.is_exploded == False:
            rotated = self.get_rotation()
            transformed = []
            for point in rotated:
                transformed.append( camera.transformPoint( point ) )
            pygame.draw.lines( camera.screen, (255,50,50), True, transformed )
            if self.is_accelerating:
                position = self.position
                points = [
                    ( ( position[0] - self.size * 0.8 ), ( position[1] + self.size * 2.0 ) ),
                    ( ( position[0] ), ( position[1] + self.size * 3.5 ) ),
                    ( ( position[0] + self.size * 0.8 ), ( position[1] + self.size * 2.0 ) )            
                ]
                rotated = self.get_rotation( points = points )
                transformed = [ camera.transformPoint( point) for point in rotated ]
                pygame.draw.lines( camera.screen, (255,255,0), False, transformed )
                if self.is_boosting:
                    points = [
                        ( ( position[0] - self.size * 0.9 ), ( position[1] + self.size * 2.0 ) ),
                        ( ( position[0] ), ( position[1] + self.size * 5.0 ) ),
                        ( ( position[0] + self.size * 0.9 ), ( position[1] + self.size * 2.0 ) )            
                    ]
                    rotated = self.get_rotation( points = points )
                    transformed = [ camera.transformPoint( point) for point in rotated ]
                    pygame.draw.lines( camera.screen, (255,128,0), False, transformed )
        else:
            font = pygame.font.SysFont('Courier New', 42)
            text = font.render("GAME OVER", True, (255,0,0) )
            camera.screen.blit( text, [-camera.offset[0], -camera.offset[1] ] )

    def get_rotation ( self, faux_position = None, points = None ):
        if faux_position is None:
            position = self.position
        else:
            position = faux_position
        if points == None:
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
                ( ( math.cos( self.angle ) * ( point[0]-position[0] ) - math.sin( self.angle ) * ( point[1]-position[1] ) + position[0] )),
                ( ( math.sin( self.angle ) * ( point[0]-position[0] ) + math.cos( self.angle ) * ( point[1]-position[1] ) + position[1] ))
            ] )        
        return rotated