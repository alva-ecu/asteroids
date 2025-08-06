import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_ACCELERATION, PLAYER_MAX_SPEED, PLAYER_FRICTION, PLAYER_SHOT_SPEED, PLAYER_SHOOT_COOLDOWN, SCREEN_WIDTH, SCREEN_HEIGHT
from shot import Shot

# The Player class inherits all the attributes and methods from CircleShape
class Player(CircleShape):

    def __init__(self, x, y): # This is the constructor, called whenever a new player object is created
        # This calls the constructor of the parent class CircleShape and sets its radius to a constant
        super().__init__(x, y, PLAYER_RADIUS)
        # This sets the initial rotation of the player
        # In Pygame, pygame.Vector2(0, 1) points down, and rotate() rotates counter-clockwise 
        # A rotation of 180 degrees will make the player initially point "up" on the screen
        self.rotation = 180
        self.timer = 0 # This initializes the timer, used for managing the cooldown between shots
        self.velocity = pygame.Vector2(0, 0)  # Add velocity tracking for the player
    
    # The triangle method calculates the three vertices for drawing the spaceship shape
    def triangle(self):
        # Vector points upward (in the direction the player is facing based on its rotation)
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        # Vector points perpendicular to forward, i.e. 270 degrees from -y and 13.33 units from the center
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        # This computes the actual coordinates of the the triangle relative to the player's self.position 
        # Tip spaceship: The initial position vector + the forward vector scaled by the radius
        a = self.position + forward * self.radius
        # Left corner: The initial position vector - the forward vector scaled by the radius and moved -right units from the center
        b = self.position - forward * self.radius - right
        # Right corner: The initial position vector - the forward vector scaled by the radius and moved +right units from the center
        c = self.position - forward * self.radius + right
        return [a, b, c] # Returns an isosceles triangle
    
    # draw method of the Player class
    def draw(self, screen):
        # It draws the triangle on the screen
        pygame.draw.polygon(screen, "white", self.triangle()) #Without the last parameter, it draws a filled triangle

    # rotate method of the Player class
    def rotate(self, dt):
        self.rotation += (PLAYER_TURN_SPEED * dt)  # Adjusts the rotation by adding the turn speed and multiplying it by delta time

    # accelerate method of the Player class
    def accelerate(self, dt, direction):
        # Calculate thrust in the direction the player is facing
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        # Updates the position by adding the forward vector, scaled by PLAYER_ACCELERATION, the direction and dt
        thrust = forward * PLAYER_ACCELERATION * direction * dt
        self.velocity += thrust  # The player's velocity grows by the thrust value 
        # dt is important for movement-related functions
        # When movement is associated to dt, it guarantees consistency regardless of the framerate

        # Cap velocity at maximum speed
        if self.velocity.length() > PLAYER_MAX_SPEED:
            self.velocity = self.velocity.normalize() * PLAYER_MAX_SPEED

    # brake method of the Player class
    def brake(self, dt):
        # Apply extra friction when braking
        brake_strength = PLAYER_FRICTION * 2  # Make braking X times stronger than normal friction
        self.velocity *= (1 - brake_strength * dt) # The closer to zero, the bigger the velocity reduction

    # update method of the Player class
    def update(self, dt):
        keys = pygame.key.get_pressed()  # Get the value of the button pressed, which one?

        if keys[pygame.K_a]:  # If A key is pressed
            self.rotate(-dt)  # Rotate the player in -dt direction (counter-clockwise)
        if keys[pygame.K_d]:  # If D key is pressed
            self.rotate(dt)  # Rotate the player in dt direction (clockwise)
        if keys[pygame.K_s]:  # If S key is pressed
            self.brake(dt)  # Brake (decrease self.velocity gradually each frame) 
        if keys[pygame.K_w]:  # If W is pressed
            self.accelerate(dt, 1)  # Accelerate (increase self.velocity by thrust)
        if keys[pygame.K_SPACE]:  # If SPACE is pressed
            if self.timer <= 0:  # And if the shoot timer is less than or equal to zero
                self.shoot()  # Use shoot method
                self.wrap_position()
                self.timer = PLAYER_SHOOT_COOLDOWN  # And set the shoot timer to the constant
        
        # Apply friction to gradually slow down)
        self.velocity *= (1 - PLAYER_FRICTION * dt) # The closer to zero, the bigger the velocity reduction
        # Update position based on current velocity
        self.position += self.velocity * dt
        # Call the wrap_position method if the player needs to wrap around the screen
        self.wrap_position()
        self.timer -= dt

    # shoot method of the Player class     
    def shoot(self):
        shot = Shot(self.position.x, self.position.y)  # Creates a bullet at the player's position
        shot.velocity = pygame.Vector2(0,1)  # This sets the velocity to point down
        # This rotates the vector so that the shot travels in the same direction as the player
        shot.velocity = shot.velocity.rotate(self.rotation)
        shot.velocity *= PLAYER_SHOT_SPEED  # The shot velocity changes by the given constant
    
    # wrap_position method of the Player class
    def wrap_position(self):  # Considering that (0,0) in Pygame is the top left corner: 
    # Check X-axis wrapping
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = SCREEN_WIDTH
    # Check Y-axis wrapping
        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
