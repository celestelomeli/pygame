import sys

import pygame

from settings import Settings 
from ship import Ship
from bullet import Bullet

class AlienInvasion: 
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        # this tells pygame to figure out a window size that will fit the screen
        # we dont know width and height of screen ahead of time, update these settings after the screen is created
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) #main display surface
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Takes in instance of alieninvasion, self, which refers to the current instance of alieninvasion
        # this parameter gives Ship access to games's resources such as screen object
        # assign this Ship instance to self.ship
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        # Set the background color.
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """Start the main loop for the game."""
        #while loop calls checkevents, shipupdate, updatescreen
        while True:
                self._check_events() #call this method from in this class using . notation
                self.ship.update() # ships position updated after we've checked for keyboard events and before we update the screen
                #ships position to be updated in response to player input
                self._update_bullets() #calling update on a group, group automatically calls update for each sprite in group

                #print(len(self.bullets))
                self._update_screen()

    # Check whether player has clicked to close the window
    # looking for new events and updating screen on each pass through the loop
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type ==  pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
                """ Respond to keypresses."""
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                elif event.key == pygame.K_q:
                    sys.exit()
                elif event.key == pygame.K_SPACE: #call firebullet when spacebar is down
                    self._fire_bullet()

    def _check_keyup_events(self, event):
                """Respond to key releases."""
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

                    # Move the ship to the right
                    #self.ship.rect.x += 1 #increase the value of ship by 1 to the right

            #Watch for keyboard and mouse events.
            #for event in pygame.event.get():
                #if event.type == pygame.QUIT:
                    #sys.exit()
            
            #Redraw the screen during each pass through the loop.
            #self.screen.fill(self.settings.bg_color)
            #self.ship.blitme() #after filling in background, we draw ship on screen calling ship.blitme()

    def _fire_bullet(self):
         """Create a new bullet and add it to the bullets group."""
         # when spacebar pressed, we check length of bullets and if it is less than 3 we create a new bullet
         if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self) #instance of bullet and call it new bullet, and add it to group bullets using add method (specific to pygame groups)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
         """Update position of bullets and get rid of old bullets."""
         #Update bullet positions
         self.bullets.update()

         # Get rid of bullets that have disappeared off the screen bc they are increasing y coordinate and taking up memory
                # have to loop over copy of list since bc technically we cant remove items from a list/group
         for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0: #check each bullet to see whether it it disapeared off top of screen 
                self.bullets.remove(bullet) # if it has remove from it from bullets
                #print(len(self.bullets))

    # added this method and moved the code that draws background and ship and flips the screen
    # redraws the screen on each pass through the main loop 
    def _update_screen(self):
         """Update images on the screen, and flip to the new screen."""
         self.screen.fill(self.settings.bg_color)
         self.ship.blitme()
         for bullet in self.bullets.sprites(): #bullets.sprite() method returns a list of all sprites in group bullets
              bullet.draw_bullet() #loop through sprites in bullets and call draw bullet on each one; this is to draw all fired bullets to screen
              

         pygame.display.flip()

        
if __name__ == '__main__':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()        