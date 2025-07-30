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
    font = pygame.font.SysFont(None, 72)
    paused = False
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()
    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

        if not paused:
            updatable.update(dt)
            
            for obj in asteroids:
                if obj.collides_with(player):
                    print("Game over!")
                    sys.exit()
            
            for obj in asteroids:
                for bullet in shot:
                    if bullet.collides_with(obj):
                        obj.split()
                        bullet.kill()

            screen.fill(color="black")

            for obj in drawable:
                obj.draw(screen)
            
        if paused:
            text_surface = font.render("Paused", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
            screen.blit(text_surface, text_rect)    
            
        pygame.display.flip()
  
        dt = (clock.tick(60)) / 1000        

if __name__ == "__main__":
    main()
