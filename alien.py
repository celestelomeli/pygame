import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    
    def __init__(self, ai_game, alien_type='green'):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.alien_type = alien_type

        # Load the alien image
        self.image = pygame.image.load('images/alien.bmp')
        
        # Set points and apply color tint based on alien type
        if alien_type == 'red':
            self.points = 50
            # Tint red for high-value aliens
            self.image = self.image.copy()
            self.image.fill((255, 100, 100), special_flags=pygame.BLEND_MULT)
        elif alien_type == 'yellow':
            self.points = 20
            # Tint yellow for medium-value aliens
            self.image = self.image.copy()
            self.image.fill((255, 255, 150), special_flags=pygame.BLEND_MULT)
        else:  # green
            self.points = 10
            # Keep original green image (no tint needed)
        
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store exact horizontal position for smooth movement
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien horizontally based on fleet direction."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x  # Update rect position