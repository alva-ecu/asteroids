import pygame
import random
from asteroid import Asteroid  # This class is important to define the features of the individual asteroid
from constants import *

# The Asteroid class inherits from pygame.sprite.Sprite
class AsteroidField(pygame.sprite.Sprite):  # Sprite is a base class for visible game objects, it groups sprites and handles updates
    # The edges list defines the four edges of the screen from which the asteroids can spawn
    edges = [
        [   # This Vector2 represents where the asteroids should move from that edge
            pygame.Vector2(1, 0),  # Since 1, 0 means the object moves right, it spawns on the left edge
            #  A Lambda function calculates the spawn position along the edge, it takes a float (x or y) between 0 and 1
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),  # It returns a Vector2 for the position
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                # The ASTEROID_MAX_RADIUS is added or substracted so that the asteroids spawn off-screen
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    # This is the constructor method for the AsteroidField class
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)  #  This calls the constructor of the parent Sprite class
        self.spawn_timer = 0.0  # This timer will be used to track when it's time to spawn a new asteroid

    # spawn method for the AsteroidField class. It uses the Asteroid class as a basis for creating the field
    def spawn(self, radius, position, velocity, color):
        asteroid = Asteroid(position.x, position.y, radius, color)
        asteroid.velocity = velocity

    # update method for the AsteroidField class, this method is called typically once per frame
    def update(self, dt):  # dt is the time elapsed between frames
        self.spawn_timer += dt  # Increments the spawn_timer by delta time
        if self.spawn_timer > ASTEROID_SPAWN_RATE:  # If enough time has passed to spawn a new asteroid
            self.spawn_timer = 0  # Reset the timer
            
            # Generate a random color tuple for the new asteroid 
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)

            new_asteroid_color = (r, g, b)
            
            # Randomly selects one of the four screen edges from the self.edges list
            edge = random.choice(self.edges)
            # Chooses a random speed between 40 and 100
            speed = random.randint(40, 100)
            # Calculates the base velocity by multiplying the direction vector by the (random) speed
            velocity = edge[0] * speed
            # Rotates the random velocity by a random angle between -30 and 30
            velocity = velocity.rotate(random.randint(-30, 30))
            # Calculates the position of the new asteroid by using the lambda function
            position = edge[1](random.uniform(0, 1))  # It also uses a random float to get a random point along the edge
            # Determines the kind (size) of the asteroid
            kind = random.randint(1, ASTEROID_KINDS)
            # Calls the spawn method to create a new asteroid with all the given parameters
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity, new_asteroid_color)
