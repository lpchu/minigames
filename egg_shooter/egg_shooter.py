"""
Bubble shooter game: try to remove all bubble under a time constraint

To be run on web browser (Chrome) @ www.codeskulptor.org
Although it is possible to run in the offline mode, it's highly NOT recommneded!

Created by LPC on Jan 2019
"""

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import math
import random

# declare global constants
BUBBLE_RADIUS = 20
BUBBLE_ACCELERATION = 5
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 700
FIRING_POSITION = [CANVAS_WIDTH/2, CANVAS_HEIGHT]
FIRING_ANG_VEL_INC = 0.05 #radian
FIRING_LINE_LENGTH = 70
COLOR_LIST = ['White', 'Red', 'Blue', 'Green', 'Purple']

# declare global variables
firing_angle = (math.pi)/2
firing_ang_vel = 0
firing_tip = list(FIRING_POSITION)


# define some helper functions
def angle_to_vector(angle):
    return [math.cos(angle), math.sin(angle)]


# define Bubble class
class Bubble:
    def __init__(self, position, velocity):
        self.pos = position
        self.vel = velocity
        self.color = random.choice(COLOR_LIST)

    def get_position(self):
        return self.pos

    def update(self):
        firing_direction = angle_to_vector(firing_angle)
        self.vel[0] += BUBBLE_ACCELERATION * firing_direction[0]
        self.vel[1] -= BUBBLE_ACCELERATION * firing_direction[1]

    def draw(self, canvas):
        # update bubble position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        canvas.draw_circle(self.pos, BUBBLE_RADIUS, 1, self.color, self.color)


# def key handlers
def key_down(key):
    global firing_ang_vel
    if key == simplegui.KEY_MAP['left']:
        firing_ang_vel += FIRING_ANG_VEL_INC
    elif key == simplegui.KEY_MAP['right']:
        firing_ang_vel -= FIRING_ANG_VEL_INC

    # hit spacebar to fire a bubble
    if key == simplegui.KEY_MAP['space']:
        a_bubble.update()


def key_up(key):
    global firing_ang_vel
    if key == simplegui.KEY_MAP['left']:
        firing_ang_vel -= FIRING_ANG_VEL_INC
    elif key == simplegui.KEY_MAP['right']:
        firing_ang_vel += FIRING_ANG_VEL_INC


# define draw handler
def draw(canvas):
    global firing_angle, firing_ang_vel

    # update firing_angle & convert to vertical and horizontal components
    firing_angle += firing_ang_vel
    firing_direction = angle_to_vector(firing_angle)

    # draw the firing line
    firing_tip[0] = FIRING_POSITION[0] + FIRING_LINE_LENGTH * firing_direction[0]
    firing_tip[1] = FIRING_POSITION[1] - FIRING_LINE_LENGTH * firing_direction[1]

    canvas.draw_line(FIRING_POSITION, firing_tip, 5, 'White')

    # draw bubbles
    a_bubble.draw(canvas)


# Create frame and register handlers
frame = simplegui.create_frame('Bubble shooter', CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(draw)
frame.set_keyup_handler(key_up)
frame.set_keydown_handler(key_down)
frame.start()

# Initiate an instance of Bubble class
a_bubble = Bubble(list(FIRING_POSITION), [0, 0])

