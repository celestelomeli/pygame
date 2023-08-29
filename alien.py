import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    
    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top of the left screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen"""
        # check if its at the right edge or left edge 
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien to the right."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction) #speed time given direction speed 
        # move alien by amount stored in alien speed in settings; self.x tells you aliens exact position
        self.rect.x = self.x #update position of aliens rect

    
        


