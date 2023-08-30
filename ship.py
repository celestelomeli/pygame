import pygame
from pygame.sprite import Sprite
 
#pygame lets you treat all game elements like rects (rectangles)
class Ship(Sprite): #ship inherits from sprite
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        # Takes in the self reference and a reference to current instance of alieninvasion class
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect() #after image is loaded call getrect to access ships rectangle

        #Start each ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    # checks the position of the ship before changing the value of the self.x 
    # manage the ships position
    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's x value, not the rect.
        # self.rect.right returns x coordinate of right edge of the ship's rect
        # if this value is less than the value returned self.screen _rect.right ship hasnt reached right edge of screen
        # left: if value of left side of rect is greater than zero, hasnt reached left edge
        # assures the ship is within bounds before adjusting the value of self.x
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect object from self.x 
        self.rect.x = self.x
   
   
    # Draw the ship to the screen
    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x) # reset self.x attribute allowing us to track the ship's exact position 

        