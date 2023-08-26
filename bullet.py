import pygame
from pygame.sprite import Sprite

# Bullet class inherits from sprite, imported from pygame.sprite module
# sprites allow you to group related elements in game and act on all grouped elements at once 
class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        # Super called to inherit properly from sprite
        #set attributes for screen and settings objects and buller color
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect attribute at (0, 0) and then set correct position 
        # must build a rect from scratch using pygame.Rect() class since bullet is not based on an image, class requires x and y coord. of top left corner
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height) # get width and height from settings 
        self.rect.midtop = ai_game.ship.rect.midtop #bullet and ship location at midtop match since bullet comes from ship

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y) 

    #manages bullet's position
    # when bullet is fired it moves up the screen corresponding to decreasing ycoordinate value
    # to update position, subtract the amount stored in settings.bulletspeed from self.y to get the bullet to move one pixel each time after its shot
    #x coordinate never changes since ship just moves postion over
    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet
        self.y -= self.settings.bullet_speed #bullet speed setting allows us to increase speed of bullets moving forward 
        # Update the rect position 
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen with color stored in self.color."""
        pygame.draw.rect(self.screen, self.color, self.rect)
