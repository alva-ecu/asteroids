SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 1     # How often the asteroids spawn (higher = less often)
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300     # How fast the player turns in a given direction
PLAYER_ACCELERATION = 400   # How fast the player accelerates
PLAYER_MAX_SPEED = 400      # Maximum speed the player can reach
PLAYER_FRICTION = 0.75      # How quickly the player slows down (higher = more friction)
PLAYER_SHOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN = 0.3 # How quickly the player shoots (higher = shoots slower)

SHOT_RADIUS = 5
SHOT_DURATION = 0.25    # How long the shot lasts after wrapping (higher = lasts more) 