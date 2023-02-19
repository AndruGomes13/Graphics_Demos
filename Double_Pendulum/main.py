###### Imports ###########

import pygame
import math
from math import sin, cos

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

# Create Transparent Surface for path tracking
path_history = pygame.Surface(DISPLAY_DIM, pygame.SRCALPHA, 32)
path_history = path_history.convert_alpha()

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




# Top Pendulum
pendulum_top = Pendulum(2, 1)
pendulum_top.rotation_point = (DISPLAY_WIDTH / 2, DISPLAY_WIDTH * 0.4)
# Bottom Pendulum
pendulum_bottom = Pendulum(1, 0.7)

# Initial conditions
pendulum_top.angle = math.radians(60)
pendulum_bottom.angle = math.radians(-30)


######### Auxiliary Funtions ########
def solve_accelerations(p1 : Pendulum, p2 : Pendulum):
    m1 = p1.mass
    l1 = p1.lenght
    x1 = p1.angle
    v1 = p1.angle_vel

    m2 = p2.mass
    l2 = p2.lenght
    x2 = p2.angle
    v2 = p2.angle_vel

    num1 = -g*(2*m1 + m2)*sin(x1)
    num2 = -m2*g*sin(x1-2*x2)
    num3_1 = -2*sin(x1-x2) * m2
    num3_2 = v2**2 * l2 + v1**2*l1*cos(x1-x2)
    den = l1 * (2 * m1 + m2 - m2 * cos(2*x1 -2 *x2))

    a1 = (num1 + num2 + num3_1 * num3_2 ) / den

    num1_1 = 2 * sin(x1 - x2)
    num2 = v1 ** 2 * l1 * (m1 + m2)
    num3 = g * (m1 + m2) * cos(x1)
    num4 = v2 ** 2 * l2 * m2 * cos(x1 - x2)
    den = l2 * (2 * m1 + m2 - m2 * cos(2 * x1 - 2 * x2))

    a2 = num1_1 * (num2 + num3 + num4) / den

    return (a1, a2)

def color_from_velocity(vel):
    vel = abs(vel)
    vel_range = 7

    a = min(vel, vel_range) / vel_range * 255
    blue = 255 - a
    red = a

    color = (red, 0 , blue)

    

    # color = (
    #             min(max(vel,0),255),
    #             min(max(0,0),255),
    #             min(max(vel,0),255)
    #         )

    return color
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
    pendulum_top_acceleration, pendulum_bottom_acceleration = solve_accelerations(pendulum_top, pendulum_bottom)

    pendulum_top.angle_vel += pendulum_top_acceleration * dt
    pendulum_bottom.angle_vel += pendulum_bottom_acceleration * dt

    pendulum_top.angle += pendulum_top.angle_vel * dt
    pendulum_bottom.angle += pendulum_bottom.angle_vel * dt





    ###### Rendering objects ####
    # Background Color
    WIN.fill("white")


    # --- Drawing path ---
    pygame.draw.circle(path_history, color_from_velocity(pendulum_bottom.angle_vel), pendulum_bottom.end_coordinates(pendulum_top.end_coordinates()), 1)
    WIN.blit(path_history, path_history.get_rect())

    # Drawing Pendulums
    pendulum_top.draw(WIN)
    pendulum_bottom.draw(WIN, pendulum_top.end_coordinates())



    # Updating Display
    pygame.display.update()




pygame.quit()





