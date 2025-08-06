import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS, SHOT_DURATION, SCREEN_WIDTH, SCREEN_HEIGHT

# The Shot class inherits all the attributes and methods from CircleShape (including collides with)
class Shot(CircleShape):
    def __init__(self, x, y):  # This is the constructor, the arguments are x and y (Vector2 values)
        # This calls the constructor of the parent class CircleShape and sets the radius to a constant
        # The initial velocity will be set by default as 0,0 and updated by the Player when it shoots
        super().__init__(x, y, SHOT_RADIUS)
        # Set a duration for the shot for when it wraps around the screen 
        self.shot_duration = SHOT_DURATION
        # The initial value is False, it will be updated when the shot has wrapped at least once
        self.wrapped = False

    # draw method of the Shot class
    def draw(self, screen):
        # It draws the shot (a circle) on the screen, 0 means it's an empty circle
        pygame.draw.circle(screen, "white", self.position, self.radius, 0)

    # update method of the Shot class
    def update(self, dt):
        # The shot's position is updated by adding the velocity and multiplying it by delta time
        self.position += self.velocity * dt
        # Call the wrap_position method if the shot needs to wrap around the screen
        self.wrap_position()
        # Decrease the shot's duration only after it wraps around the screen
        if self.wrapped == True:
            self.shot_duration -= dt
        # If the shot's time has reached or exceeded the threshold and it has wrapped:
        if self.shot_duration <= 0 and self.wrapped == True:
            self.kill()  # It will be killed 
    
    # wrap_position method of the Shot class
    def wrap_position(self):  # Considering that (0,0) in Pygame is the top left corner: 
        wrapped_this_call = False  # Initial value to be checked against the following conditions
    # Check X-axis wrapping
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
            wrapped_this_call = True  # True only if the shot wrapped around this side of the screen
        elif self.position.x < 0:
            self.position.x = SCREEN_WIDTH
            wrapped_this_call = True  # Same
    # Check Y-axis wrapping
        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
            wrapped_this_call = True  # Same
        elif self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
            wrapped_this_call = True  # Same
        
        if wrapped_this_call:  # If the shot wrapped around any side of the screen:
            self.wrapped = True  # The shot indeed wrapped and the initial value will change
