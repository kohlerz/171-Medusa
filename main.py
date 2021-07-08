from window import Window
from client import Client
from joystick import Joystick

xbox = Joystick()
client = Client(xbox)
window = Window(xbox, client)
