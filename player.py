import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_ACCELERATION, PLAYER_MAX_SPEED, PLAYER_FRICTION, PLAYER_SHOT_SPEED, PLAYER_SHOOT_COOLDOWN
from shot import Shot

class Player(CircleShape):

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 180
        self.timer = 0
        self.velocity = pygame.Vector2(0, 0)  # Add velocity tracking
    
    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle())

    def rotate(self, dt):
        self.rotation += (PLAYER_TURN_SPEED * dt)

    def accelerate(self, dt, direction):
        # Calculate thrust in the direction the player is facing
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        thrust = forward * PLAYER_ACCELERATION * direction * dt
        self.velocity += thrust

        # Cap velocity at maximum speed
        if self.velocity.length() > PLAYER_MAX_SPEED:
            self.velocity = self.velocity.normalize() * PLAYER_MAX_SPEED

    def brake(self, dt):
        # Apply extra friction when braking
        brake_strength = PLAYER_FRICTION * 2  # Make braking X times stronger than normal friction
        self.velocity *= (1 - brake_strength * dt)
    
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt) 
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_s]:
            self.brake(dt) 
        if keys[pygame.K_w]:
            self.accelerate(dt, 1)
        if keys[pygame.K_SPACE]:
            if self.timer <= 0:
                self.shoot()
                self.timer = PLAYER_SHOOT_COOLDOWN
        
        # Apply friction to gradually slow down
        self.velocity *= (1 - PLAYER_FRICTION * dt)
        
        # Update position based on current velocity
        self.position += self.velocity * dt
        
        self.timer -= dt
     
    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0,1)
        shot.velocity = shot.velocity.rotate(self.rotation)
        shot.velocity *= PLAYER_SHOT_SPEED
