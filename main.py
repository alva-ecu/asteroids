import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()  # This initializes all imported pygame modules
    print("Starting Asteroids!")  # This prints the string to the console when starting the game
    print(f"Screen width: {SCREEN_WIDTH}")  # Same as above
    print(f"Screen height: {SCREEN_HEIGHT}")  # Same as above
    
    # Object variables to allocate sprite groups
    drawable = pygame.sprite.Group()  # pygame.sprite.Group() creates an empty container group for sprites
    updatable = pygame.sprite.Group()  # updatable and drawable are variables that contain those groups 
    asteroids = pygame.sprite.Group()  # Same as above, but for asteroids
    shot = pygame.sprite.Group()  # Same as above, but for shots

    # Tells each Class which groups new instances (e.g. player1, player2) should automatically join
    Player.containers = (updatable, drawable)  # When a Player object is created, it's automatically added to both the updatable and drawable groups
    Asteroid.containers = (asteroids, updatable, drawable)  #Same, but for the Asteroid class
    AsteroidField.containers = (updatable,)  #Same, but for the AsteroidField class
    Shot.containers = (shot, updatable, drawable)  #Same, but for the Shot class

    #Game-related variables
    screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))  # Creates the game window with specified dimensions
    clock = pygame.time.Clock()  # Controls frame rate timing
    dt = 0  # Delta time - time elapsed since last frame
    paused = False  # Boolean for later pause functionality
    game_state = "playing"  # String tracking current state (playing or game over)

    # Lives system variables
    lives = 3  # Number of lives
    invincibility_timer = 0  # Countdown for temporary invincibility after being hit
    invincibility_duration = 120  # How long invincibility lasts (2 seconds at 60 FPS)

    #Variables for the blinking "Press SPACE for restart" text
    last_text_blink = 0.0
    restart_text_visible = True
    blink_interval = 0.5

    # Font variables
    pause_font = pygame.font.Font("fonts/PressStart2P.ttf", 70)  # Font makes it 8-bit like
    over_font = pygame.font.Font("fonts/PressStart2P.ttf", 60)
    restart_font = pygame.font.Font("fonts/PressStart2P.ttf", 35)
    lives_font = pygame.font.Font("fonts/PressStart2P.ttf", 24)
    
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  #This creates a player at the center of the screen
    asteroidfield = AsteroidField()  #This creates the asteroid spawning system

    # New function for respawning after being hit
    def respawn_player():
        nonlocal player, invincibility_timer  #nonlocal calls for variables from outside the function
        player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # Repositions the player at the center
        player.velocity = pygame.Vector2(0, 0)  # Stops player movement
        invincibility_timer = invincibility_duration  #Activates invincibility 

    # This is where the fun starts: the main game loop!
    while True:  # We set a while (infinite) loop, the code below keeps running continuously
        screen.fill(color="black")  # This will clear the screen to black each frame
        
        # Event handling code
        for event in pygame.event.get():  # Gets all input events since last frame
            if event.type == pygame.QUIT:  # The player pressed the X button on the game window...
                return  # So it exits the game

            # Handles the "paused" state
            if event.type == pygame.KEYDOWN:  # KEYDOWN refers to when a key is pressed
                if event.key == pygame.K_ESCAPE:  # The key pressed is ESC
                    paused = not paused  # The original "paused" Boolean changes between FALSE and not FALSE  
            
            # Handles the "game over" and "restart/playing" states
            if game_state == "game_over":  # This state will change when a collision happens
                if event.type == pygame.KEYDOWN:  # KEYDOWN refers to when a key is pressed
                    if event.key == pygame.K_SPACE:  # The key pressed is SPACE
                        # Reset everything for new game
                        game_state = "playing"  # Reset the state to playing 
                        lives = 3
                        invincibility_timer = 0
                        asteroids.empty()  # This empties the group's values
                        shot.empty()
                        updatable.empty()
                        drawable.empty()
                        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) # player is positioned at the center
                        asteroidfield = AsteroidField()
                        last_text_blink = 0.0
                        restart_text_visible = True

        #  Handles the invincibility after respawn and the update logic
        if game_state == "playing" and not paused:  # First time for updating
            # Update invincibility timer
            if invincibility_timer > 0:  # When respawning, invincibility is set to 120 frames
                invincibility_timer -= 1  # This keeps reducing the timer until it reaches zero
            updatable.update(dt)  # Only updates game objects when playing and not paused

            # Collision detection with invincibility check
            for obj in asteroids:
                if obj.collides_with(player) and invincibility_timer <= 0:  # collides_with from CircleShape
                    lives -= 1  # Keep reducing lives
                    if lives <= 0:
                        print("Game over!")
                        game_state = "game_over"  # The game_over state is tied to the number of lives
                    else:
                        print(f"Lives remaining: {lives}")
                        respawn_player()  # We use the function previously defined outside the game loop
                    break  # Only handle one collision per frame
            
            # Detect the collisions between the asteroids and the bullets
            for obj in asteroids:  # For each asteroid
                for bullet in shot:  # And for each bullet
                    if bullet.collides_with(obj):
                        obj.split()  # The asteroid breaks into smaller pieces
                        bullet.kill()  # The bullet is removed from all sprite groups, it "disappears"

        # Drawing
        if game_state == "playing" and not paused: # Second time for drawing
            for obj in drawable:  # For each element in drawable
                # Flicker player during invincibility
                if obj == player and invincibility_timer > 0:  # And if that element is an invincible player
                    if invincibility_timer % 10 < 5:  # Flicker every 10 frames
                        continue  # Skip drawing player
                obj.draw(screen)  # If the timer reaches zero, the player is drawn solid
            # Draw lives counter
            lives_text = lives_font.render(f"Lives: {lives}", True, (255, 255, 255))  # Renders only text
            screen.blit(lives_text, (10, 10))  # This effectively draws the lives counter at the top left
        
        elif paused:  # If the main condition above isn't met...
            text_surface = pause_font.render("Paused", True, (0, 0, 200))  # Render this text instead
            text_rect = text_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2))  # Center it
            background_rect = text_rect.inflate(40, 20)  # Creates a background rectangle that covers the objects
            pygame.draw.rect(screen, (0, 0, 0), background_rect)  # Draws a black rectangle on the screen
            screen.blit(text_surface, text_rect)  # Draws the text surface onto the screen (source, destination)    
        
        elif game_state == "game_over": # If the conditions above aren't met...
            text_surface = over_font.render("Game Over", True, (0, 0, 200)) # Render this text instead
            text_rect = text_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 50)) # Offset text
            screen.blit(text_surface, text_rect)  # Draws the text surface onto the screen (source, destination)

            # This makes the text blink
            last_text_blink += dt  # Original set to zero, so it will grow along with dt
            if last_text_blink >= blink_interval:  # Where the interval is 0.5. If enough time has passed... 
                restart_text_visible = not restart_text_visible  # It toggles the restart_text_visible
                last_text_blink = 0.0  # It resets the timer to zero every time

            if restart_text_visible: # When restart_text_visible is TRUE
                restart_text = restart_font.render("Press SPACE to restart", True, (225, 40, 40))  # It renders the text
                restart_rect = restart_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 50)) # Offset text
                screen.blit(restart_text, restart_rect)  # Draws the text surface onto the screen (source, destination)
        
        pygame.display.flip()  # Updates the entire screen with everything drawn this frame
        dt = (clock.tick(60)) / 1000  # Limits the game to 60 fps and converts to seconds for dt

# Prevents main from running if the file is imported as a module
if __name__ == "__main__":
    main()