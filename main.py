import pygame
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
    paused = False
    game_state = "playing"
    dt = 0

    pause_font = pygame.font.Font("fonts/PressStart2P.ttf", 70)
    over_font = pygame.font.Font("fonts/PressStart2P.ttf", 40)
    restart_font = pygame.font.Font("fonts/PressStart2P.ttf", 25)
    
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
            
            if game_state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_state = "playing"
                        asteroids.empty()
                        shot.empty()
                        updatable.empty()
                        drawable.empty()
                        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) 
                        asteroidfield = AsteroidField()

        if game_state == "playing" and not paused:
            updatable.update(dt)

            for obj in asteroids:
                if obj.collides_with(player):
                    print("Game over!")
                    game_state = "game_over"
            
            for obj in asteroids:
                for bullet in shot:
                    if bullet.collides_with(obj):
                        obj.split()
                        bullet.kill()

            screen.fill(color="black")

        if game_state == "playing" and not paused:
            for obj in drawable:
                obj.draw(screen)
        elif paused:
            text_surface = pause_font.render("Paused", True, (0, 0, 200))
            text_rect = text_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
            background_rect = text_rect.inflate(40, 20)
            pygame.draw.rect(screen, (0, 0, 0), background_rect)
            screen.blit(text_surface, text_rect)    
        elif game_state == "game_over":
            text_surface = over_font.render("Game Over", True, (0, 0, 200))
            text_rect = text_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 30))
            screen.blit(text_surface, text_rect)

            restart_text = restart_font.render("Press SPACE to restart", True, (225, 40, 40))
            restart_rect = restart_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 30))
            screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
  
        dt = (clock.tick(60)) / 1000        

if __name__ == "__main__":
    main()
