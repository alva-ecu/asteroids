import pygame
import random
from circleshape import CircleShape
from constants import SHOT_RADIUS, ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, color):
        super().__init__(x, y, radius)
        self.rotation = 0
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        random_angle = random.uniform(20, 50)
        new_velocity1 = self.velocity.rotate(random_angle)
        new_velocity2 = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        r1 = random.randint(0, 255)
        g1 = random.randint(0, 255)
        b1 = random.randint(0, 255)
        color1 = (r1, g1, b1)

        r2 = random.randint(0, 255)
        g2 = random.randint(0, 255)
        b2 = random.randint(0, 255)
        color2 = (r2, g2, b2)

        new_asteroid1 = Asteroid(self.position.x, self.position.y, new_radius, color1)
        new_asteroid2 = Asteroid(self.position.x, self.position.y, new_radius, color2)
        
        scaling1 = new_velocity1 * 1.2
        new_asteroid1.velocity = scaling1
        scaling2 = new_velocity2 * 1.2
        new_asteroid2.velocity = scaling2
