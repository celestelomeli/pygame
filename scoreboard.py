import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """A class to report scoring information"""

    def __init__(self, ai_game): #aigame passed to give access to settings, screen, stats
        """"Initialize scorekeeping attributes"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48) #instantiate font object

        # Prepare initial score images
        self.prep_score()
        self.prep_high_score() #high score recorded and score
        self.prep_level()
        self.prep_ships()


    def prep_score(self):
        """Turn the score into a rendered image"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score) #comma separators large numbers
        #score_str = str(self.stats.score) #turn numerical value into a string
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color) #pass string to render which creates the image

        #Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect() #create score rect and place it's right edge 20 pixels from right edge of screen
        self.score_rect.right = self.screen_rect.right - 20 
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn high score into a rendered image"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top 

    def show_score(self):
        """Draw scores, levels, and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect) #draws the score image on screen at location score_rect specifies
        self.screen.blit(self.high_score_image, self.high_score_rect) 
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    # checks current score against high score
    def check_high_score(self): 
        """Check to see if there's a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self): #creates an image from value stored in stats.level
        """ Turn level into rendered image"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color) 

        # Position the level below the score
        self.level_rect = self.level_image.get_rect()
        #sets image's right attribute to match score's right attribute
        self.level_rect.right = self.score_rect.right 
        #set top attribute 10 pixels beneath bottom of score image to leave space btwn score and level
        self.level_rect.top = self.score_rect.bottom + 10

    # creates an empty group, self.ships, to hold ship instances
    def prep_ships(self):
        """Show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left): #loop runs once for every ship player has left
            ship = Ship(self.ai_game) 
            #create new ship and set each ship's x coord value so ships appear next to each other a 10 pixel margin on left side of group of ships
            ship.rect.x = 10 + ship_number * ship.rect.width
            # set y coord value 10 pixels down from the top of screen so ships appear in upper left corner of screen
            ship.rect.y = 10
            self.ships.add(ship) #add each new ship to group ships