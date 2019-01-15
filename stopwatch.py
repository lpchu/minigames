""" STOPWATCH mini game 
Week 3 assignment of 'An introduction to interactive programming in Python' by Rice University (Coursera)

Script can be run online @ http://www.codeskulptor.org/ using built-in simplegui module
or offline using an equivalent SimpleGUICS2Pygame module (developed by Olivier Pirson)
"""

try:
    import simplegui
except:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    
import random

# define global variables
total_tenths_seconds = 0
winning_game = 0
game_counter = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    """
    Convert total time (tenths of seconds)
    into minute:second.tenth_second in a formatted string A:BC.D
    """

    tens_second = t // 10
    tenth_second = t - tens_second*10
    minute = tens_second // 60
    second = tens_second - minute*60

    return minute, second, tenth_second

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    """ Start the clock """
    if not timer.is_running():
        timer.start()

def stop():
    """ Stop the clock
    and check if the tenth_second is at the 0 mark
    """
    global total_tenths_seconds, winning_game, game_counter

    # Check if the timer is running (hence incrementing game_counter by 1)
    if timer.is_running():
        timer.stop()
        game_counter += 1

        [minute, second, tenth_second] = format(total_tenths_seconds)
        if tenth_second == 0:
            winning_game += 1

def reset():
    """ Reset the clock and the score"""
    global total_tenths_seconds, winning_game, game_counter

    timer.stop()
    total_tenths_seconds = 0
    winning_game = 0
    game_counter = 0

# define event handler for timer with 0.1 sec interval
def tick():
    """ Count the time elapsed """
    global total_tenths_seconds

    total_tenths_seconds += 1

# define draw handler
def draw(canvas):
    global total_tenths_seconds

    # Convert total_tenths_seconds into minute:second.tenth_second
    [minute, second, tenth_second] = format(total_tenths_seconds)

    # Game stops when minute reaches 9
    if total_tenths_seconds > 5999:
        timer.stop()

    # Print out the elapsed time
    if second < 10:
        second = '0'+ str(second)

    canvas.draw_text(str(minute) + ':' +
                     str(second) + '.' +
                     str(tenth_second), [65, 110], 70, 'White')

    # Print out the score
    canvas.draw_text(str(winning_game) + ' / ' + str(game_counter),
                     [20, 20], 20, 'Yellow')


# create frame & timer
frame = simplegui.create_frame('Stopwatch: The game', 300, 200)
timer = simplegui.create_timer(100, tick)

# register event handlers
frame.set_draw_handler(draw)
frame.add_button('Start', start, 50)
frame.add_button('Stop', stop, 50)
frame.add_button('Reset', reset, 50)

# start frame
frame.start()

# Please remember to review the grading rubric
