import sys
from time import sleep #pause game when ship is hit

import pygame

from settings import Settings 
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

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

        #Create an instance to stop game statistics and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Takes in instance of alieninvasion, self, which refers to the current instance of alieninvasion
        # this parameter gives Ship access to games's resources such as screen object
        # assign this Ship instance to self.ship
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group() #sprite group is container provided; collection of aliens/alien sprites

        self._create_fleet()

        # Make Play button
        self.play_button = Button(self, "Play") # instancce of button with label "play"

        # Set the background color.
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """Start the main loop for the game."""
        #while loop calls checkevents, shipupdate, updatescreen
        while True:
                self._check_events() #must always check first to know if player quit or closes window

                if self.stats.game_active: #calls that only happen if game is active 
                     self.ship.update() # ships position updated after we've checked for keyboard events and before we update the screen
                    #ships position to be updated in response to player input
                     self._update_bullets() #calling update on a group, group automatically calls update for each sprite in group
                     self._update_aliens() #update position of each alien
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
            elif event.type == pygame.MOUSEBUTTONDOWN: #any mouse click on screen
                 mouse_pos = pygame.mouse.get_pos() #returns tuple containing mouse cursor's x and y coordinates
                 self._check_play_button(mouse_pos) #send those x & y coord to checkplaybutton

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos) #collidepoint to check whether mouse click overlaps region defined by play button's rect
        if button_clicked and not self.stats.game_active:
             #reset the game settings
             self.settings.initialize_dynamic_settings()
              # button clicked stores true or false; game will restart only if play is clicked and game is active
             # Hide the mouse cursor
             pygame.mouse.set_visible(False) #hide cursor when mouse is over the game window
             # reset game stats
             self.stats.reset_stats() #reset to 3 new ships
             self.stats.game_active = True #set to true if so 
             self.sb.prep_score()
             self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
             self.aliens.empty()

        # Create new fleet and center the ship
             self._create_fleet()
             self.ship.center_ship()     

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
        # Check for any bullets that have hit aliens
        # If so, get rid of the bullets that have hit aliens
         #Update bullet positions
         self.bullets.update()

         # Get rid of bullets that have disappeared off the screen bc they are increasing y coordinate and taking up memory
                # have to loop over copy of list since bc technically we cant remove items from a list/group
         for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0: #check each bullet to see whether it it disapeared off top of screen 
                self.bullets.remove(bullet) # if it has remove from it from bullets
                #print(len(self.bullets))

         self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
         """Respond to bullet-alien collisions."""
         #Remove any bullets and aliens that have collided
         collisions = pygame.sprite.groupcollide( self.bullets, self.aliens, True, True) #compares positions of all bullets and aliens and identifies any that overlap
         # two true arguments tell pygame to delete bullets and aliens that collided 
         if collisions:
              for aliens in collisions.values(): #collisions dictionary, each value in dict is list of aliens hit by single bullet
                 self.stats.score += self.settings.alien_points * len(aliens) #multiply value of each alien by number of aliensin each list and addamount to current score
              self.sb.prep_score()
              self.sb.check_high_score()
         if not self.aliens:
              # Check if alien group is empty; if so destroy existing bullets and create new fleet
              self.bullets.empty()
              self._create_fleet() #create new fleet
              self.settings.increase_speed()

              # Increase level.
              self.stats.level += 1
              self.sb.prep_level() #new level displays correctly


    # creating one instance of Alien and adding it to the group that will hold the fleet
    def _create_fleet(self):
         """Create the fleet of aliens"""
         # Make an alien
         alien = Alien(self) # create alien
         alien_width, alien_height = alien.rect.size # get alien size
         #bc we have two margins on the screen, available space for aliens is screen width minus two alien widths
         # to calculate number of rows fit on screen, y calculation after x calculation
         available_space_x = self.settings.screen_width - (2 * alien_width) #calculate horizonal space available for aliens and # of aliens that fit
         # divide the available space by two times the width of an alien  
         number_aliens_x = available_space_x // (2 * alien_width)

         # Determine number of rows of aliens that fit on screen
         ship_height = self.ship.rect.height
         available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
         number_rows = available_space_y // (2 * alien_height)

         # Create full fleet of aliens
         for row_number in range(number_rows): #inner loop creates aliens in one row
              for alien_number in range(number_aliens_x): #counts from 0 to number of rows we want 
                 self._create_alien(alien_number, row_number)

         # Create the first row of aliens.
         # loop that counts from 0 to number of aliens we need to make 
         # create new alien and set its x coordinate value to place in the row 
         #for alien_number in range(number_aliens_x):
              #self._create_alien(alien_number)
            # Create an alien and place it in a row
            
    def _create_alien(self, alien_number, row_number): #alien number thats currently being created 
         # Create an alien and place place it in the row
         alien = Alien(self)
         alien_width, alien_height = alien.rect.size
         # each alien pushed to the right one alien width from left margin, multipy alien width by 2 for space taken up by alien and multiply by alien's position in row
         alien.x = alien_width + 2 * alien_width * alien_number
         alien.rect.x = alien.x #set position of its rect
         alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number #
         self.aliens.add(alien) #add each new alien to the group aliens 

    def _check_fleet_edges(self):
         """Respond appropriately if any aliens have reached an edge"""
         # We loop through fleet and call check_edges() on each alien
         #if returns true alien is at an edge and call change fleet direction and break out of loop
         for alien in self.aliens.sprites():
              if alien.check_edges():
                   self._change_fleet_direction()
                   break 
              
    def _change_fleet_direction(self):
         """Drop the entire fleet and change the fleet's direction"""
         # loop through all aliens and drop each using setting fleet drop speed
         for alien in self.aliens.sprites():
              alien.rect.y += self.settings.fleet_drop_speed #change value of fleet direction by multiplying current value by -1
         self.settings.fleet_direction *= -1 #only want to change direction of fleet once so not in loop


    def _check_aliens_bottom(self):
         """"Check if any aliens have reached the bottom of the screen"""
         screen_rect = self.screen.get_rect()
         for alien in self.aliens.sprites():
              if alien.rect.bottom >= screen_rect.bottom:
                   #Treat this the time as if ship got hit
                   self._ship_hit()
                   break

    def _update_aliens(self):
         """Check if the fleet is at edge, then update positions of all aliens in fleet """
         self._check_fleet_edges()
         self.aliens.update()

         # Look for alien-ship collisions
         if pygame.sprite.spritecollideany(self.ship, self.aliens): #loops through group of aliens & returns first alien that has collided with ship 
              self._ship_hit() #after ship is hit, delete remaining bullets and aliens, recenter ship, create new fleet

        # Look for aliens hitting the bottom of screen
         self._check_aliens_bottom()
    
    def _ship_hit(self):
         """Respond to the ship being hit by an alien"""
         if self.stats.ships_left > 0:
            #Decrement ships_left, and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships() #call after decreasing value of ships_left so correct number of ships displays each time a ship is destroyed

         # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

         # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

         #Pause
            sleep(0.5)
         else:
            self.stats.game_active = False #if no more ships left, game over 
            pygame.mouse.set_visible(True) #make cursor visible again as soon as game becomes inactive which happens in ship_hit

    # added this method and moved the code that draws background and ship and flips the screen
    # redraws the screen on each pass through the main loop 
    def _update_screen(self):
         """Update images on the screen, and flip to the new screen."""
         self.screen.fill(self.settings.bg_color)
         self.ship.blitme()
         for bullet in self.bullets.sprites(): #bullets.sprite() method returns a list of all sprites in group bullets
              bullet.draw_bullet() #loop through sprites in bullets and call draw bullet on each one; this is to draw all fired bullets to screen
        # make alien appear call groups draw() method 
         self.aliens.draw(self.screen)  # draw method requires one attribute, surface to draw elements

        # Draw the score information
         self.sb.show_score()
        # Draw the play button if the game is inactive
         if not self.stats.game_active:
              self.play_button.draw_button()
         
         pygame.display.flip()

        
if __name__ == '__main__':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()        