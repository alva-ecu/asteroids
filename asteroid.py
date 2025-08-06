import pygame
import random
from circleshape import CircleShape
from constants import SHOT_RADIUS, ASTEROID_MIN_RADIUS

# The Asteroid class inherits all the attributes and methods from CircleShape
class Asteroid(CircleShape):
    # This is the constructor, the arguments are x and y (Vector2 values), radius and color
    def __init__(self, x, y, radius, color):
        super().__init__(x, y, radius) # This calls the constructor of the parent class CircleShape
        self.rotation = 0  # Initial rotation is zero, can be used for something-shaped asteroids
        self.color = color  # Takes the color specified by the constructor

    # draw method of the Asteroid class
    def draw(self, screen):
        # It draws the asteroid (a circle) on the screen, 2 means it's an empty circle
        pygame.draw.circle(screen, self.color, self.position, self.radius, 2)

    # update method of the Asteroid class
    def update(self, dt):
        # The shot's position is updated by adding the velocity and multiplying it by delta time
        self.position += self.velocity * dt

    # split method of the Asteroid class (with a colorful twist)
    def split(self):
        self.kill() # Killing itself means that the asteroid is removed from all sprite groups, rendering it invisible
        if self.radius <= ASTEROID_MIN_RADIUS:  # If the current asteroid is smaller than or equal to the constant
            return  # The method returns, ending that asteroid's execution (it disappears)
        random_angle = random.uniform(20, 50) # Else, create a random divergence angle (random floating-point between min and max)
        # This takes the original asteroid's velocity vector and rotates it by the divergence angle
        new_velocity1 = self.velocity.rotate(random_angle)
        # Same as above, but uses a negative divergence angle, sending the asteroid in the opposite direction
        new_velocity2 = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS # This calculates the radius of the new smaller asteroids

        # The following code sets random values for the RGB color space
        r1 = random.randint(0, 255)
        g1 = random.randint(0, 255)
        b1 = random.randint(0, 255)
        color1 = (r1, g1, b1)

        r2 = random.randint(0, 255)
        g2 = random.randint(0, 255)
        b2 = random.randint(0, 255)
        color2 = (r2, g2, b2)

        # The resulting asteroids are spawned at the same position where the original was destroyed
        # Also, they are smaller due to their new radius and have a different color each :3
        new_asteroid1 = Asteroid(self.position.x, self.position.y, new_radius, color1)
        new_asteroid2 = Asteroid(self.position.x, self.position.y, new_radius, color2)
        
        # This makes the new smaller asteroids move faster than their parent asteroid
        scaling1 = new_velocity1 * 1.2
        new_asteroid1.velocity = scaling1
        scaling2 = new_velocity2 * 1.2
        new_asteroid2.velocity = scaling2
