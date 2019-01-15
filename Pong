# Implementation of classic arcade game Pong

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui  
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

# flags for button pressing
w_pressed = False
s_pressed = False
up_pressed = False
down_pressed = False

acc = 5 #acceleration of the paddles

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    horizontal_vel = random.randrange(120, 240) / 60.0
    vertical_vel = random.randrange(60, 180) / 60.0
    
    if direction == 'RIGHT':
        #ball_vel should be upward and towards the right
        ball_vel = [horizontal_vel, -vertical_vel]
    elif direction == 'LEFT':
        #upward and towards the left
        ball_vel = [-horizontal_vel, -vertical_vel]
        
    ball_pos = [WIDTH/2, HEIGHT/2]

    return ball_pos, ball_vel

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    score1 = score2 = 0
    
    random_num = random.randrange(0,2)
    if random_num == 0:
        spawn_ball('LEFT')
    else:
        spawn_ball('RIGHT')
    
    # specify the vertical coordinates of the 2 paddles (mid-points of the paddles)
    paddle1_pos = paddle2_pos = HEIGHT/2
    
    paddle1_vel = paddle2_vel = 0
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    global w_pressed, s_pressed, up_pressed, down_pressed
    
    # right player
    if key == simplegui.KEY_MAP['up']:
        up_pressed = True
    elif key == simplegui.KEY_MAP['down']:
        down_pressed = True
    
    if up_pressed and not down_pressed:
        paddle2_vel -= acc
    elif down_pressed and not up_pressed:
        paddle2_vel += acc
    else:
        paddle2_vel = 0
    
    # left player
    if key == simplegui.KEY_MAP['w']:
        w_pressed = True
    elif key == simplegui.KEY_MAP['s']:
        s_pressed = True
    
    if w_pressed and not s_pressed:
        paddle1_vel -= acc
    elif s_pressed and not w_pressed:
        paddle1_vel += acc
    else:
        paddle1_vel = 0
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    global w_pressed, s_pressed, up_pressed, down_pressed
    
    # right player
    if key == simplegui.KEY_MAP['up']:
        up_pressed = False
    elif key == simplegui.KEY_MAP['down']:
        down_pressed = False

    if up_pressed and not down_pressed:
        paddle2_vel -= acc
    elif down_pressed and not up_pressed:
        paddle2_vel += acc
    else:
        paddle2_vel = 0
    
    # left player
    if key == simplegui.KEY_MAP['w']:
        w_pressed = False
    elif key == simplegui.KEY_MAP['s']:
        s_pressed = False
    
    if w_pressed and not s_pressed:
        paddle1_vel -= acc
    elif s_pressed and not w_pressed:
        paddle1_vel += acc
    else:
        paddle1_vel = 0
        
def restart():
    # restart the game
    new_game()
    
def draw(canvas):
    global score1, score2 
    global paddle1_vel, paddle2_vel, paddle1_pos, paddle2_pos
    global ball_pos, ball_vel
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # update paddle's vertical position, keep paddle on the screen
    # (check conditions of paddle positions before updating)
    if paddle1_pos - HALF_PAD_HEIGHT + paddle1_vel < 0 or \
       paddle1_pos + HALF_PAD_HEIGHT + paddle1_vel > HEIGHT:
        paddle1_vel = 0
    if paddle2_pos - HALF_PAD_HEIGHT + paddle2_vel < 0 or \
       paddle2_pos + HALF_PAD_HEIGHT + paddle2_vel > HEIGHT:
        paddle2_vel = 0
        
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel

    # ball bounces off the top and bottom of the canvas
    if ball_pos[1] - BALL_RADIUS < 0 or ball_pos[1] + BALL_RADIUS > HEIGHT:
        ball_vel[1] = -ball_vel[1]
        
    # when the ball touches the gutter,
    if ball_pos[0] - BALL_RADIUS < PAD_WIDTH: 
        # ball touches the left gutter
        if paddle1_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            # check if the ball and the left paddle collide 
            # also increase the ball_vel by 10%
            ball_vel[0] = -ball_vel[0] * 1.1
        else:
            # spawn a new ball in the center heading towards RIGHT
            spawn_ball('RIGHT')
            # right player wins
            score2 += 1
            
    elif ball_pos[0] + BALL_RADIUS > WIDTH - PAD_WIDTH:
        # ball touches the right gutter
        if paddle2_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            # check if the ball and the right paddle collide
            # also increase the ball_vel by 10%
            ball_vel[0] = -ball_vel[0] * 1.1
        else:
            # spawn a new ball in the center heading towards LEFT
            spawn_ball('LEFT')
            # left player wins
            score1 += 1
    
    # update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'White', 'White')
    
    # draw paddles
    canvas.draw_line([0, paddle1_pos], [PAD_WIDTH, paddle1_pos], PAD_HEIGHT, 'White') 
    canvas.draw_line([WIDTH - PAD_WIDTH, paddle2_pos], [WIDTH, paddle2_pos], PAD_HEIGHT, 'White') 
    
    # draw scores
    canvas.draw_text(str(score1), [WIDTH/4, HEIGHT/5], 40, 'Yellow')
    canvas.draw_text(str(score2), [WIDTH*3/4, HEIGHT/5], 40, 'Yellow')

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', restart, 50)

# start frame
new_game()
frame.start()
