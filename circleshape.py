import pygame

# Acts as a base class for game objects such as the player, the asteroids and the shots
class CircleShape(pygame.sprite.Sprite):  # A Sprite is a class that represents a visual object, its position and behavior
    def __init__(self, x, y, radius):  # This is the constructor, called whenever we create a CircleShape object
        if hasattr(self, "containers"):  # This Pygame pattern ensures that when an object is created, it is added to the specified groups
            super().__init__(self.containers)  # If self has its respective container, add the object to the corresponding groups
        else:
            super().__init__()  # If not, simply initialize the Sprite without adding it to any groups

        self.position = pygame.Vector2(x, y)  # This creates and stores a Vector2 object with the position of the circle, where +y (in Pygame) is the -y axis
        self.velocity = pygame.Vector2(0, 0)  # This creates and stores another Vector2 object for the circle's velocity (distance/time and direction)
        self.radius = radius  # This establishes the radius of the circle, defining its size

    # These methods are overridden by the class-specific methods of the same name 
    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    # This method calculates the distance between two circle objects
    # If the distance between them is lesser than or equal to the sum of the radii, it means they collided
    def collides_with(self, other):
        return self.position.distance_to(other.position) <= self.radius + other.radius
        # Returns True if 'this' circle overlaps with 'other'
