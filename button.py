import pygame.font #module allows render text to screen

class Button:
    def __init__(self, ai_game, msg):
        """Initialize button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48) #prepare font attribute for rendering text; none = default font and 48 = text size

        #Build the button's rect object and center it 
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #the button message needs to be prepped only once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color) #font.render turns text in msg into an image #boolean for antialiasing(edges of text smoother)
        self.msg_image_rect = self.msg_image.get_rect() #center text image on button by creating rect from image 
        self.msg_image_rect.center = self.rect.center #set the center to match the button

    def draw_button(self):
        # Draw blank button and then draw message
        self.screen.fill(self.button_color, self.rect) #draw rectangular portion of button
        self.screen.blit(self.msg_image, self.msg_image_rect) #draw text image to screen, passing it image and rect object associated with the image
