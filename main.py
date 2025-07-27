import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)

    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)

    AsteroidField.containers = (updatable,)

    shot = pygame.sprite.Group()
    Shot.containers = (shot, updatable, drawable)

    screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    dt = 0
    asteroidfield = AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)
        
        for obj in asteroids:
            if obj.collides_with(player):
                print("Game over!")
                sys.exit()
        
        for obj in asteroids:
            for bullet in shot:
                if bullet.collides_with(obj):
                    obj.kill()
                    bullet.kill()

        screen.fill(color="black")

        for obj in drawable:
            obj.draw(screen)
        
        pygame.display.flip()
        
        dt = (clock.tick(60)) / 1000        

if __name__ == "__main__":
    main()
