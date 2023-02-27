####### Imports ########

import pygame
from math import sin, cos, atan2

##############

class Stick:
    def __init__(self, length:int, origin:list) -> None:
        self.lenght = length
        self.origin = origin
        self.angle = 0
        self.end = [self.origin[0] + self.lenght * cos(self.angle) , self.origin[1] + self.lenght * sin(self.angle)]
        self.width = 4

    def draw(self, win):
        pygame.draw.line(win, pygame.Color("Black"), self.origin, self.end, self.width)

    def set_direction(self, mouse):
        dx = mouse[0] - self.origin[0]
        dy = mouse[1] - self.origin[1]
        self.angle = atan2(dy, dx)


    def move_origin(self, new_origin):
        self.origin = new_origin
        self.end = [self.origin[0] + self.lenght * cos(self.angle) , self.origin[1] + self.lenght * sin(self.angle)]

    def set_end(self, mouse):
        self.set_direction(mouse)
        self.end = [self.origin[0] + self.lenght * cos(self.angle) , self.origin[1] + self.lenght * sin(self.angle)]
        dx = mouse[0] - self.end[0]
        dy = mouse[1] - self.end[1]
        self.end[0] = self.end[0] + dx
        self.end[1] = self.end[1] + dy
        self.origin[0] = self.origin[0] + dx
        self.origin[1] = self.origin[1] + dy
        

    def step(self):
        self.end = [self.origin[0] + self.lenght * cos(self.angle) , self.origin[1] + self.lenght * sin(self.angle)]



