###### Imports ###########

import pygame
import math
from math import sin, cos
from Stick import Stick
########### Variable Declaration ##########


# ------------ Constants ---------

# Window Size
DISPLAY_WIDTH = 700
DISPLAY_HEIGHT = 700
DISPLAY_DIM = (DISPLAY_WIDTH, DISPLAY_HEIGHT)

# Creating Windows
WIN = pygame.display.set_mode(DISPLAY_DIM)
pygame.display.set_caption("Double Pendulum Simulation")

# Setting Frames per Second
FPS = 60
CLOCK = pygame.time.Clock()


# ------------ Defining Global Variables ---------

# Gravitational Acceleration
g = 9.8

# --- Pendulum Characteristics ---

class Pendulum:
    def __init__(self, mass :int , lenght : int) -> None:
        # Physical characteristics
        self.mass = mass
        self.lenght = lenght

        # Position
        self.angle = 0
        self.angle_vel = 0
        
        self.rotation_point = (0, 0)

        # Cosmetic
        self.radius = 5
        self.color = pygame.Color("black")
        self.line_width = 1

        # Scale factor
        self.scale = 200

    def end_coordinates(self, rotation_point : tuple = None):
        origin = self.rotation_point if not rotation_point else rotation_point
        x = origin[0] + self.lenght * sin(self.angle) * self.scale
        y = origin[1] + self.lenght * cos(self.angle) * self.scale
        return (x, y)

    def draw(self, win, rotation_point : tuple = None):
        origin = self.rotation_point if not rotation_point else rotation_point
        r2 = self.end_coordinates(rotation_point)
        pygame.draw.circle(win, self.color, r2, self.radius)
        pygame.draw.line(win, self.color, origin, r2, self.line_width)


n_sticks = 50 #number of sticks
stick_len = 5

# Top Pendulum
stick_list = []
for i in range(n_sticks):
    stick = Stick(stick_len, [DISPLAY_WIDTH // 2 , DISPLAY_HEIGHT // 2])
    stick.width = int((i + 1) ** 0.5)
    stick_list.append(stick)



######### Auxiliary Funtions ########


#####################################
# Initializing DeltaT counter
getTicksLastFrame = pygame.time.get_ticks()


# Running Simulation

running = True
while running:

    # Handling Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #### Stepping Objects ######
    #---- Finding Delta T -----
    t = pygame.time.get_ticks()
    dt = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t

    # --- Stepping ---
    # stick_1.set_direction(pygame.mouse.get_pos())


    ###### Rendering objects ####
    # Background Color
    WIN.fill("white")


    # Drawing sticks
    for i in range(len(stick_list)):
        if i == 0:
            stick_list[i].set_end(pygame.mouse.get_pos())
            continue
        stick_list[i].set_end(stick_list[i-1].origin)

    for i in reversed(range(len(stick_list))):
        if i == len(stick_list) - 1 :
            stick_list[i].move_origin([DISPLAY_WIDTH // 2 , DISPLAY_HEIGHT // 2])
            continue
        stick_list[i].move_origin(stick_list[i+1].end)
    
    
    for stick in stick_list:
        stick.draw(WIN)


    # Updating Display
    pygame.display.update()

    CLOCK.tick(FPS)


pygame.quit()





