from typing import Text
import pygame
from pygame import Color
import threading
from joystick import Joystick

class TextLine(object):
    # Manages drawing and caching a single line of text
    # You can make font size, .color_fg etc be properties so they *automatically* toggle dirty bool.
    def __init__(self, font=None, size=16, text="hi world"):        
        self.font_name = font
        self.font_size = size
        self.color_fg = Color("white")
        self.color_bg = Color("gray20")

        self._aa = True 
        self._text = text                
        self.font = pygame.font.Font(font, size)
        self.screen = pygame.display.get_surface()

        self.x = 0
        self.y = 0

        self.dirty = True
        self.image = None
        self._render()

    def _render(self):
        # render for cache
        """no AA = automatic transparent. With AA you need to set the color key too"""
        self.dirty = False        
        self.image = self.font.render(self._text, True, self.color_fg)            
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def center(self, x, y):
        self.x = x
        self.y = y
        self._render()

    def draw(self):
        # Call this do draw, always prefers to use cache
        if self.dirty or (self.image is None): self._render()
        self.screen.blit(self.image, self.rect)     

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self.dirty = True
        self._text = text

class Window(object):
    def __init__(self, xbox, client):
        pygame.init()

        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 400
        self.FPS = 30
        self.TOGGLE_HEIGHT = 300
        self.ENABLED_COLOR = (0, 150, 0)
        self.ENABLED_HOVER = (0, 125, 0)
        self.DISABLED_COLOR = (150, 0, 0)
        self.DISABLED_HOVER = (125, 0, 0)

        self.enabled_rect = pygame.Rect(0, 0, self.SCREEN_WIDTH, self.TOGGLE_HEIGHT)
        self.controller_rect = pygame.Rect((0, self.TOGGLE_HEIGHT, self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT-self.TOGGLE_HEIGHT))
        self.wifi_rect = pygame.Rect((self.SCREEN_WIDTH/2, self.TOGGLE_HEIGHT, self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT-self.TOGGLE_HEIGHT))

        self.screen = pygame.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont('Arial', 50)

        self.enabled_text = TextLine(text="Enabled")
        self.controller_text = TextLine(text="🎮 Not Connected")
        self.wifi_text = TextLine(text="WiFi Not connected")

        self.enabled_text.center(self.enabled_rect.centerx, self.enabled_rect.centery)
        # self.controller_text.center(100, 100)
        # self.wifi_text.center(200, 200)
        self.controller_text.center(self.controller_rect.centerx, self.controller_rect.centery)
        self.wifi_text.center(self.wifi_rect.centerx, self.wifi_rect.centery)

        # pygame.display.set_caption('Medusa')
        # self.programIcon = pygame.image.load('medusa.png')
        # pygame.display.set_icon(self.programIcon)

        self.enabled = False

        self.xbox = xbox
        self.client = client

        self.run()

    def run(self):
        mousex = 0
        mousey = 0
        enable_hover = False
        controller_hover = False
        wifi_hover = False
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

            enable_hover     = self.enabled_rect.collidepoint(mousex, mousey)
            controller_hover = self.controller_rect.collidepoint(mousex, mousey)
            wifi_hover       = self.wifi_rect.collidepoint(mousex, mousey)

            self.handle_click(enable_hover, mouse_clicked, self.enabled_rect)
            self.handle_click(controller_hover, mouse_clicked, self.controller_rect)
            self.handle_click(wifi_hover, mouse_clicked, self.wifi_rect)

            self.draw_button(self.enabled, enable_hover, self.enabled_rect)
            self.draw_button(self.xbox.connected, controller_hover, self.controller_rect)
            self.draw_button(self.client.connected, wifi_hover, self.wifi_rect)

            # Update controller and send data to Medusa
            pygame.event.pump()
            self.xbox.update()
            self.client.data = self.xbox.format_data(self.enabled)

            # Flip the display
            pygame.display.update()
            self.clock.tick(self.FPS)

            enable_hover = False
            controller_hover = False
            wifi_hover = False
            mouse_clicked = False

        # Done! Time to quit.
        pygame.quit()

    def draw_button(self, condition, hover, rect):
        window_focused = pygame.mouse.get_focused()

        if condition:
            if hover and window_focused:
                pygame.draw.rect(self.screen, self.ENABLED_HOVER, rect)
            else: 
                pygame.draw.rect(self.screen, self.ENABLED_COLOR, rect)
        else:
            if hover and window_focused:
                pygame.draw.rect(self.screen, self.DISABLED_HOVER, rect)
            else:
                pygame.draw.rect(self.screen, self.DISABLED_COLOR, rect)

        text = self.get_state(condition, rect)
        text.draw()
    
    def handle_click(self, hover, clicked, rect):
        if hover and clicked:
            if rect == self.enabled_rect:
                self.enabled = not self.enabled
            elif rect == self.controller_rect:
                self.xbox.connect

    def get_state(self, condition, rect):
        text = None
        if rect == self.enabled_rect:
            if condition:
                self.enabled_text.text = "Enabled"
                text = self.enabled_text
            else:
                self.enabled_text.text = "Disabled"
                text = self.enabled_text
        elif rect == self.controller_rect:
            if condition:
                self.controller_text.text = "Controller Connected"
                text = self.controller_text
            else:
                self.controller_text.text = "Controller Not Connected"
                text = self.controller_text
        elif rect == self.wifi_rect:
            if condition:
                self.wifi_text.text = "WiFi Connected"
                text = self.wifi_text
            else:
                self.wifi_text.text = "Trying to connect..."
                text = self.wifi_text
        
        return text
