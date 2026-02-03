import pygame
from pygame.sprite import Sprite

# Inherits from Sprite - allows grouping related elements and acting on them at once
class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        super().__init__()  # Inherit properly from Sprite
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Build rect from scratch (no image) - requires x, y coords of top-left corner
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop  # Bullet spawns from ship's position

        # Store position as decimal for smooth movement
        self.y = float(self.rect.y)

    def update(self):
        """Move bullet up screen (decreasing y-coordinate)."""
        self.y -= self.settings.bullet_speed  # Allows dynamic speed adjustments
        self.rect.y = self.y  # Update rect position

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
