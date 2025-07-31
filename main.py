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

    # Lives system variables
    lives = 3
    invincibility_timer = 0
    invincibility_duration = 120  # 2 seconds at 60 FPS

    pause_font = pygame.font.Font("fonts/PressStart2P.ttf", 70)
    over_font = pygame.font.Font("fonts/PressStart2P.ttf", 70)
    restart_font = pygame.font.Font("fonts/PressStart2P.ttf", 35)
    lives_font = pygame.font.Font("fonts/PressStart2P.ttf", 24)  # New font for lives
    
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()

    last_text_blink = 0.0
    restart_text_visible = True
    blink_interval = 0.5

    def respawn_player():
        nonlocal player, invincibility_timer
        player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        player.velocity = pygame.Vector2(0, 0)
        invincibility_timer = invincibility_duration

    while True:
        screen.fill(color="black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
            
            if game_state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Reset everything for new game
                        game_state = "playing"
                        lives = 3
                        invincibility_timer = 0
                        asteroids.empty()
                        shot.empty()
                        updatable.empty()
                        drawable.empty()
                        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) 
                        asteroidfield = AsteroidField()
                        last_text_blink = 0.0
                        restart_text_visible = True

        if game_state == "playing" and not paused:
            # Update invincibility timer
            if invincibility_timer > 0:
                invincibility_timer -= 1

            updatable.update(dt)

            # Collision detection with invincibility check
            for obj in asteroids:
                if obj.collides_with(player) and invincibility_timer <= 0:
                    lives -= 1
                    if lives <= 0:
                        print("Game over!")
                        game_state = "game_over"
                    else:
                        print(f"Lives remaining: {lives}")
                        respawn_player()
                    break  # Only handle one collision per frame
            
            for obj in asteroids:
                for bullet in shot:
                    if bullet.collides_with(obj):
                        obj.split()
                        bullet.kill()

        # Drawing
        if game_state == "playing" and not paused:
            for obj in drawable:
                # Flicker player during invincibility
                if obj == player and invincibility_timer > 0:
                    if invincibility_timer % 10 < 5:  # Flicker every 10 frames
                        continue  # Skip drawing player
                obj.draw(screen)
            
            # Draw lives counter
            lives_text = lives_font.render(f"Lives: {lives}", True, (255, 255, 255))
            screen.blit(lives_text, (10, 10))
            
        elif paused:
            text_surface = pause_font.render("Paused", True, (0, 0, 200))
            text_rect = text_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
            background_rect = text_rect.inflate(40, 20)
            pygame.draw.rect(screen, (0, 0, 0), background_rect)
            screen.blit(text_surface, text_rect)    
        elif game_state == "game_over":
            text_surface = over_font.render("Game Over", True, (0, 0, 200))
            text_rect = text_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 50))
            screen.blit(text_surface, text_rect)

            last_text_blink += dt
            if last_text_blink >= blink_interval:
                restart_text_visible = not restart_text_visible
                last_text_blink = 0.0

            if restart_text_visible:
                restart_text = restart_font.render("Press SPACE to restart", True, (225, 40, 40))
                restart_rect = restart_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 50))
                screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        dt = (clock.tick(60)) / 1000        

if __name__ == "__main__":
    main()