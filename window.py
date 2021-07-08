import pygame
import threading
from joystick import Joystick

class Window(object):
    def __init__(self, xbox, client):
        pygame.init()

        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 400
        self.FPS = 30
        self.TOGGLE_HEIGHT = 300
        self.ENABLED_COLOR = (0, 150, 0)
        self.ENABLED_HOVER = (0, 100, 0)
        self.DISABLED_COLOR = (150, 0, 0)
        self.DISABLED_HOVER = (100, 0, 0)

        self.enabled_rect = pygame.Rect(0, 0, self.SCREEN_WIDTH, self.TOGGLE_HEIGHT)
        self.debug_rect   = pygame.Rect(0, self.TOGGLE_HEIGHT, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        self.screen = pygame.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont('Arial', 50)

        pygame.display.set_caption('Medusa')
        self.programIcon = pygame.image.load('medusa.png')
        pygame.display.set_icon(self.programIcon)

        self.enabled = False
        self.debugging = False

        self.console_text = ''

        self.xbox = xbox
        self.client = client

        self.run()

    def run(self):
        mousex = 0
        mousey = 0
        enable_hover = False
        debug_hover = False
        mouse_clicked = False

        running = True
        while running:

            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEMOTION:
                    mousex, mousey = event.pos
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousex, mousey = event.pos
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_clicked = True

            if not self.client.connected:
                self.client.connect()

            enable_hover = self.enabled_rect.collidepoint(mousex, mousey)
            debug_hover = self.debug_rect.collidepoint(mousex, mousey)

            if debug_hover and mouse_clicked:
                self.debugging = not self.debugging
                mouse_clicked = False
            elif enable_hover and mouse_clicked:
                self.enabled = not self.enabled
                mouse_clicked = False

            # Fill the background with white
            self.screen.fill((255, 255, 255))

            if self.debugging:
                self.draw_debug_window()
            else:
                self.draw_toggle(self.enabled, enable_hover)

            debug_text = self.font.render("Debugging Console", True, (0,0,0))
            debug_text_rect = debug_text.get_rect(center=(self.SCREEN_WIDTH/2, self.TOGGLE_HEIGHT + (self.SCREEN_HEIGHT-self.TOGGLE_HEIGHT)/2))
            self.screen.blit(debug_text, debug_text_rect)

            # Update controller and send data to Medusa
            self.xbox.update()
            self.client.send_data(self.xbox.format_data(self.enabled))

            # Flip the display
            pygame.display.update()
            self.clock.tick(self.FPS)

        # Done! Time to quit.
        pygame.quit()

    def draw_toggle(self, enabled, hover):
        window_focused = pygame.mouse.get_focused()

        if self.enabled:
            toggle_text = self.font.render("Enabled", True, (0,0,0))

            if hover and window_focused:
                pygame.draw.rect(self.screen, self.ENABLED_HOVER, self.enabled_rect)
            else: 
                pygame.draw.rect(self.screen, self.ENABLED_COLOR, self.enabled_rect)
        else:
            toggle_text = self.font.render("Disabled", True, (0,0,0))
            
            if hover and window_focused:
                pygame.draw.rect(self.screen, self.DISABLED_HOVER, self.enabled_rect)
            else:
                pygame.draw.rect(self.screen, self.DISABLED_COLOR, self.enabled_rect)

        enabled_text_rect = toggle_text.get_rect(center=(self.SCREEN_WIDTH/2, self.TOGGLE_HEIGHT/2))
        self.screen.blit(toggle_text, enabled_text_rect)

    def draw_debug_window(self):
        self.screen.fill((0, 0, 0))

    def add_debug_text(self, text):
        self.console_text += text
