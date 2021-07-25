import pygame
from time import sleep
from math import copysign

class Joystick(object):
    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        self.left_stick = 0.0
        self.right_stick = 0.0
        self.deadzone = 0.05
        self.connected = False

        self.data = 'D 0.00 0.00'

        self.connect()

    def update(self):
        if pygame.joystick.get_count() == 0 or not self.connected:
            self.connected = False
            self.connect()

        try:
            self.left_stick = self.xbox.get_axis(1)
            self.right_stick = self.xbox.get_axis(2)
            print(self.left_stick)
        except:
            self.connected = False

    def connect(self):
        if pygame.joystick.get_count() > 0:
            self.xbox = pygame.joystick.Joystick(0)
            self.xbox.init()
            self.connected = True
        # else:
            # print("Controller not connected")

    def format_data(self, enabled):
        self.data = ''

        # Enable status
        if enabled:
            self.data += 'E '
        else:
            self.data += 'D '

        # Joystick values
        if abs(self.left_stick) > self.deadzone:
            left_normalized = round((abs(self.left_stick) - self.deadzone) / (1-self.deadzone), 2)
            self.data += str(copysign(left_normalized, self.left_stick)) + " "
        else:
            self.data += "0.00 "
        
        if abs(self.right_stick) > self.deadzone:
            right_normalized = round((abs(self.right_stick) - self.deadzone) / (1-self.deadzone), 2)
            self.data += str(copysign(right_normalized, self.right_stick))
        else:
            self.data += "0.00"

        return self.data