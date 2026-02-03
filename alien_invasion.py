import sys
from time import sleep

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

        # Set fullscreen mode and update settings with actual screen dimensions
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Create game statistics and scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Create game objects
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make Play button
        self.play_button = Button(self, "Play")

        # Create pause message
        self.font = pygame.font.SysFont(None, 80)

        # Set background color
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active and not self.stats.game_paused: # check if not paused
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset game settings
            self.settings.initialize_dynamic_settings()

            # Hide mouse cursor
            pygame.mouse.set_visible(False)

            # Reset game stats
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Clear remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:    # Move right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:   # Move left
            self.ship.moving_left = True
        elif event.key == pygame.K_q:      # Quit game
            sys.exit()
        elif event.key == pygame.K_SPACE:  # Fire bullet
            self._fire_bullet()
        elif event.key == pygame.K_p:      # Pause/unpause game
            self._toggle_pause()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed and not self.stats.game_paused:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
     
     # Pause game with 'P' key
    def _toggle_pause(self):
        """Toggle pause state when P is pressed."""
        if self.stats.game_active:      # Only allow pausing when game is active
            self.stats.game_paused = not self.stats.game_paused  # Toggle pause state

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()

        # Remove bullets that have disappeared off screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Check for collisions and remove both bullets and aliens
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                # Award points based on each alien's individual point value
                for alien in aliens:
                    self.stats.score += alien.points
            self.sb.prep_score()
            self.sb.check_high_score()

        # If fleet destroyed, start new level
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Calculate how many aliens fit on screen
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # Calculate number of aliens per row (with margins)
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Calculate number of rows that fit on screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        # Assign alien type based on row number
        # Higher value aliens at top (harder to reach)
        total_rows = 6  # Approximate number of rows
        if row_number < total_rows // 3:
            alien_type = 'red'  # Top rows (hardest to reach, 50 points)
        elif row_number < 2 * total_rows // 3:
            alien_type = 'yellow'  # Middle rows (medium, 20 points)
        else:
            alien_type = 'green'  # Bottom rows (easiest to hit, 10 points)
        
        alien = Alien(self, alien_type)
        alien_width, alien_height = alien.rect.size

        # Position alien with spacing
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat same as ship hit
                self._ship_hit()
                break

    def _update_aliens(self):
        """Check if fleet is at edge, then update positions of all aliens."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of screen
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Clear remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        # Draw bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draw aliens
        self.aliens.draw(self.screen)

        # Draw score information
        self.sb.show_score()

        # Draw play button if game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Draw pause message if game is paused
        if self.stats.game_paused:         
            self._draw_pause_message()        # Draw PAUSED message

        pygame.display.flip()                 # Make the most recently drawn screen visible

    # New method to draw pause message
    def _draw_pause_message(self):
        """Draw PAUSED message in center of screen."""
        pause_text = self.font.render("PAUSED", True, (100, 100, 100), self.settings.bg_color)
        pause_rect = pause_text.get_rect()                  # Get rect for positioning
        pause_rect.center = self.screen.get_rect().center   # Center on screen
        self.screen.blit(pause_text, pause_rect)


if __name__ == '__main__':
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()