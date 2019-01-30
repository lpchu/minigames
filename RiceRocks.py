# implementation of Spaceship - program template for RiceRocks
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui 

import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

HIGH_SCORE = 0

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 100
BUTTON_THICKNESS = 10

restart_box = ([WIDTH*1/7, HEIGHT*4/5], [WIDTH*1/7 + BUTTON_WIDTH, HEIGHT*4/5],
               [WIDTH*1/7 + BUTTON_WIDTH, HEIGHT*4/5 + BUTTON_HEIGHT], 
               [WIDTH*1/7, HEIGHT*4/5 + BUTTON_HEIGHT])

restart_box2 = ([0, 0], [0, 0], [0, 0], [0, 0])
for i in range(len(restart_box)):
    restart_box2[i][0] = restart_box[i][0] - BUTTON_THICKNESS
    restart_box2[i][1] = restart_box[i][1] - BUTTON_THICKNESS
    
quit_box = ([WIDTH*4.2/7, HEIGHT*4/5], [WIDTH*4.2/7 + BUTTON_WIDTH, HEIGHT*4/5],
            [WIDTH*4.2/7 + BUTTON_WIDTH, HEIGHT*4/5 + BUTTON_HEIGHT], 
            [WIDTH*4.2/7, HEIGHT*4/5 + BUTTON_HEIGHT])

quit_box2 = ([0, 0], [0, 0], [0, 0], [0, 0])
for i in range(len(quit_box)):
    quit_box2[i][0] = quit_box[i][0] + BUTTON_THICKNESS
    quit_box2[i][1] = quit_box[i][1] - BUTTON_THICKNESS
     

restart_box_center = (restart_box[0][0] + BUTTON_WIDTH/2, restart_box[0][1] + BUTTON_HEIGHT/2)
quit_box_center = (quit_box[0][0] + BUTTON_WIDTH/2, quit_box[0][1] + BUTTON_HEIGHT/2)
    

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# endgame splash- source: https://wallpapersafari.com/game-over-wallpaper
endsplash_info = ImageInfo([1920/2, 1080/2], [1920, 1080])
endsplash_image = simplegui.load_image("https://i.imgur.com/dADwpdd.jpg")

# restart button- source: http://theantranch.com/blog/retart-buttons/
restart_info = ImageInfo([550/2, 330/2], [400, 100])
restart_image = simplegui.load_image("https://i.imgur.com/mYdxRNq.jpg")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

ship_explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
ship_explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue2.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
#soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.3)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")


# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

def process_sprite_group(a_set, canvas):
    # This function takes a set and a canvas and call the update 
    #	and draw methods for each sprite in the group.
    for item in set(a_set):
        item.draw(canvas)
        if item.update():
            a_set.remove(item)
            
def group_collide(set_group, other_object):
    # This function takes a set_group and other_object and check for collisions 
    #	between other_object and elements of the set_group (sprite objects). 
    #	If there is a collision, the colliding object should be removed from the group.
    for item in set(set_group):
        if item.collide(other_object):
            set_group.remove(item)
            
            exploded_item = Sprite(item.get_pos(), [0, 0], 0, 0, explosion_image, explosion_info, sound = explosion_sound)
            explosion_group.add(exploded_item)
            
            # if the other_object is Ship class => explode ship when colliding with asteroids as well
            if isinstance(other_object, Ship):
                exploded_ship = Sprite(other_object.get_pos(), [0, 0], 0, 0, ship_explosion_image, ship_explosion_info, sound = explosion_sound)
                explosion_group.add(exploded_ship)
            return True
    return False

def group_group_collide(group_object1, group_object2):
    global score, no_collisions
    no_collisions = 0
    for item in set(group_object1):
        if group_collide(group_object2, item):
            no_collisions += 1
            group_object1.discard(item)
    return no_collisions

def reset():
    # resets game
    global score, lives, missile_group, rock_group, my_ship

    # initialize ship
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    
    timer.start()
    score = 0
    lives = 3
    missile_group = set()
    rock_group = set()
    soundtrack.play()
    
def quit():
    frame.stop()
    timer.stop()
    soundtrack.rewind()    
    ship_thrust_sound.rewind()
        
def endgame(canvas):
    global score
    # stops everything until mouseclick to restart/quit
    timer.stop()
    explosion_sound.rewind()
    
    # draw endgame splash
#    canvas.draw_image(endsplash_image, endsplash_info.get_center(), 
#                      endsplash_info.get_size(), [WIDTH/2, HEIGHT/2], [WIDTH, HEIGHT])
    canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), 
                      [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
    
#    ship_decor1 = Ship([WIDTH*1/6, HEIGHT*1/2], [0, -1], -math.pi/2, ship_image, ship_info)
#    ship_decor2 = Ship([WIDTH*5/6, HEIGHT*1/2], [0, -1], -math.pi/2, ship_image, ship_info)
#    ship_decor1.set_thrust('on')
#    ship_decor2.set_thrust('on')
#    ship_decor1.draw(canvas)
#    ship_decor2.draw(canvas)
    
    # draw highscore text
    canvas.draw_text('HIGH SCORE: ' + str(HIGH_SCORE), [WIDTH*1/4 + 27, HEIGHT*1/10], 40, 'Yellow', 'monospace')
    canvas.draw_text('Your score: ' + str(score), [WIDTH*1/4 + 27, HEIGHT*1/5], 40, 'White', 'monospace')
    
    # draw UI endgame
    canvas.draw_polygon(restart_box, 3, 'Lime')
    canvas.draw_polygon(restart_box2, 3, 'Lime')
    canvas.draw_polygon(quit_box, 3, 'Lime')
    canvas.draw_polygon(quit_box2, 3, 'Lime')
    canvas.draw_text('Retry!', [restart_box[0][0]+12, restart_box_center[1]+15], 50, 'White', 'monospace')
    canvas.draw_text('Quit', [quit_box[0][0]+40, quit_box_center[1]+15], 50, 'White', 'monospace')
        
# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
    
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def shoot(self):
        global a_missile, missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        
        missile_group.add(a_missile)
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
    
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, (self.age * self.image_size[0] + self.image_size[0] / 2, self.image_center[1]), 
                              self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # update age
        self.age += 1
        
        # if self.age >= self.lifespan: remove the sprite
        if self.age >= self.lifespan:
            return True
        return False
        
    def collide(self, other_object):
        # returns True if 2 objects collide
        return dist(self.pos, other_object.get_pos()) <= self.radius + other_object.get_radius()
        
# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives
    # mouseclick to start the game initially
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        soundtrack.play()
    
    # mouseclick to restart
    inwidth_restart = (restart_box_center[0] - BUTTON_WIDTH/2) < pos[0] < (restart_box_center[0] + BUTTON_WIDTH/2)
    inheight_restart = (restart_box_center[1] - BUTTON_HEIGHT/2) < pos[1] < (restart_box_center[1] + BUTTON_HEIGHT/2)
    if (lives == 0) and inwidth_restart and inheight_restart:
        reset()
    
    # mouseclick to quit
    inwidth_quit = (quit_box_center[0] - BUTTON_WIDTH/2) < pos[0] < (quit_box_center[0] + BUTTON_WIDTH/2)
    inheight_quit = (quit_box_center[1] - BUTTON_HEIGHT/2) < pos[1] < (quit_box_center[1] + BUTTON_HEIGHT/2)
    if (lives == 0) and inwidth_quit and inheight_quit:
        quit()
        
def draw(canvas):
    global time, started, lives, score, rock_group, missile_group, no_collisions, HIGH_SCORE
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text("Lives: " + str(lives), [50, 50], 22, "White", 'monospace')
    canvas.draw_text("Score: " + str(score), [650, 50], 22, "White", 'monospace')

    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # check for collision between ship and rock_group: reduce lives by 1 if there is collision
    if group_collide(rock_group, my_ship) and timer.is_running():
        lives -= 1
        
    # check for collision between rock_group and missile_group and update score
    group_group_collide(missile_group, rock_group)
    if timer.is_running():
        score += 10 * no_collisions

    # update ship
    my_ship.update()

    # draw splash screen when lives = 0 and remove all rocks:
    if lives == 0:
        if score > HIGH_SCORE:
            HIGH_SCORE = score
        rock_group = set()
        endgame(canvas)
        
    # draw splash screen if not started     
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock, rock_group, started, my_ship, score
    if started:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
        rock_avel = random.random() * .2 - .1
        
        # change rock_vel based on score to make the game more interesting
        rock_vel[0] += score // 50
        rock_vel[1] += score // 50 
        
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
        
            
        # limit the max number of rocks at any one time = 12
        if len(rock_group) < 12:
            # ignore events when a_rock is spawn within 1.5*radius of my_ship
            if dist(a_rock.get_pos(), my_ship.get_pos()) >= 2*my_ship.get_radius():
                rock_group.add(a_rock)
                
# create frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize a group of rocks, a group of missiles and a group of explosion
rock_group = set()
missile_group = set()
explosion_group = set()

# initialize ship
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
