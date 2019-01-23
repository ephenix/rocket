import math, time, pygame

class rocket:

  world = None

  #pixels x, y
  position = [ 0.0, 0.0 ]

  #pixels/s
  velocity_vector = [ 0.0, 0.0 ]

  #radians
  angle = 0.0
  
  #radians/s/s
  turn_responsiveness = 0.1

  #angular velocity in radians/s
  angular_velocity = 0.0

  #kgg
  mass = 1000.0

  #KN
  thrust = 20000.0

  #Unix timestamp of last update
  lastupdate = None

  #amount to multiply timespans by for faster physics
  time_multiplier = 3.0

  #acceleration state -- whether to draw flame
  is_accelerating = False
  
  #boost state -- whether to draw big flame
  is_boosting = False

  #fuel
  fuel_quanity = 1000.0

  #base fuel consumption
  fuel_consumption = 5.0

  #current fuel consumption
  fuel_consumption_current = 0.0

  #sizes
  rocket_size = 10.0, 25.0

  def __init__ ( self, world, size=None, position=None ):
    self.position = [ 0, 0 ]
    if position :
      self.position = position
    if size != None :
      self.size = size

    self.lastupdate = time.time()
    self.world = world

  def turn ( self, direction, timespan ):
    if abs(direction) > 0:
      self.angular_velocity = self.angular_velocity + ( self.turn_responsiveness * direction * timespan )
    self.angle = self.angle + ( self.angular_velocity * timespan )

  def accelerate ( self, throttle, timespan ):
    
    if self.fuel_quanity > 0.0:
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
      self.fuel_quanity = self.fuel_quanity - fuel_use
      self.fuel_consumption_current = fuel_use
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
    velocity_x = self.velocity_vector[0] + ( acceleration_vector[0] * timespan )
    velocity_y = self.velocity_vector[1] + ( acceleration_vector[1] * timespan )

    self.velocity_vector[0] = velocity_x
    self.velocity_vector[1] = velocity_y
  
  def move ( self, timespan ):
    self.position[0] = self.position[0] + ( self.velocity_vector[0] * timespan )
    self.position[1] = self.position[1] + ( self.velocity_vector[1] * timespan )

    if self.position[1] <= 0.0:
      self.position[1] = 0
      self.velocity_vector[1] = 0.0
      self.velocity_vector[0] = 0.0
      self.angular_velocity = 0.0

    if self.position[0] < ( 0.0 - self.world['origin'][0] ):
      self.position[0] = self.world['screen'].get_size()[0]
    elif self.position[0] > self.world['screen'].get_size()[0]:
      self.position[0] = 0

    
  def update ( self, turn, accelerate ):
    currenttime = time.time()
    timespan = ( currenttime - self.lastupdate ) * self.time_multiplier
    self.lastupdate = currenttime

    self.turn( turn, timespan )
    self.accelerate( accelerate, timespan )
    self.move( timespan )

  def draw ( self ):
    rocket_center =  [ ( self.world['origin'][0] + int( self.position[0] ) ), ( self.world['origin'][1] - int ( self.position[1] ) ) ]
    points = [
      ( rocket_center[0] - self.rocket_size[0], rocket_center[1] + self.rocket_size[1]  ),
      ( rocket_center[0] + self.rocket_size[0], rocket_center[1] + self.rocket_size[1]  ),
      ( rocket_center[0] + self.rocket_size[0], rocket_center[1] - self.rocket_size[1]  ),
      ( rocket_center[0] - self.rocket_size[0], rocket_center[1] - self.rocket_size[1]  )
    ]
    rotated_points = []
    for point in points:
      new_x = math.cos(self.angle) * (point[0]-rocket_center[0]) - math.sin(self.angle) * (point[1]-rocket_center[1]) + rocket_center[0]
      new_y = math.sin(self.angle) * (point[0]-rocket_center[0]) + math.cos(self.angle) * (point[1]-rocket_center[1]) + rocket_center[1]
      rotated_points.append( ( new_x, new_y ) )
    
    pygame.draw.polygon( self.world['screen'], self.world['colors']['white'], rotated_points)

    if self.is_accelerating:
      points = (
        ( rocket_center[0] - self.rocket_size[0], rocket_center[1] + self.rocket_size[1] ),
        ( rocket_center[0] + self.rocket_size[0], rocket_center[1] + self.rocket_size[1] ),
        ( rocket_center[0], rocket_center[1] + self.rocket_size[1] + 25 ),
      )
      rotated_points = []
      for point in points:
        new_x = math.cos(self.angle) * (point[0]-rocket_center[0]) - math.sin(self.angle) * (point[1]-rocket_center[1]) + rocket_center[0]
        new_y = math.sin(self.angle) * (point[0]-rocket_center[0]) + math.cos(self.angle) * (point[1]-rocket_center[1]) + rocket_center[1]
        rotated_points.append( ( new_x, new_y ) )
    
      pygame.draw.polygon( self.world['screen'], self.world['colors']['yellow'], rotated_points)

      if self.is_boosting:
        points = (
        ( rocket_center[0] - ( self.rocket_size[0] * 0.8 ), rocket_center[1] + self.rocket_size[1] ),
        ( rocket_center[0] + ( self.rocket_size[0] * 0.8 ), rocket_center[1] + self.rocket_size[1] ),
        ( rocket_center[0], rocket_center[1] + self.rocket_size[1] + 15 ),
      )
        rotated_points = []
        for point in points:
          new_x = math.cos(self.angle) * (point[0]-rocket_center[0]) - math.sin(self.angle) * (point[1]-rocket_center[1]) + rocket_center[0]
          new_y = math.sin(self.angle) * (point[0]-rocket_center[0]) + math.cos(self.angle) * (point[1]-rocket_center[1]) + rocket_center[1]
          rotated_points.append( ( new_x, new_y ) )
        pygame.draw.polygon( self.world['screen'], self.world['colors']['red'], rotated_points)

  


