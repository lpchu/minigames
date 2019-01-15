# implementation of card game - Memory
# sources for card images:
    # http://www.loadtve.biz/playing-card-back.html
    # https://bonafideplayingcards.com/portfolio/count-monte-cristo-playing-cards/

# import modules
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui  
import random

# load images of cards
back_card = simplegui.load_image('https://i.imgur.com/W1V4z7G.png')
back_card_size = [427, 600] #ratio-lock ~1.4
back_card_center = [back_card_size[0]/2, back_card_size[1]/2]

ace = simplegui.load_image('https://i.imgur.com/Iv0tM7Q.png') #ace of diamonds
two = simplegui.load_image('https://i.imgur.com/k59hwth.png') #2 of diamonds
three = simplegui.load_image('https://i.imgur.com/Zd16VhN.png') #3 of hearts
four = simplegui.load_image('https://i.imgur.com/l3mfLhp.png') #4 of clubs
five = simplegui.load_image('https://i.imgur.com/nvZQK4W.png') #5 of clubs
six = simplegui.load_image('https://i.imgur.com/KNQp4A7.png') #6 of spades
seven = simplegui.load_image('https://i.imgur.com/PM3RbR7.png') #7 of hearts
joker = simplegui.load_image('https://i.imgur.com/Za73zWO.png')

cards = [joker, ace, two, three, four, five, six, seven]

front_card_size = [500, 704] #ratio-lock ~1.4
front_card_center = [front_card_size[0]/2, front_card_size[1]/2]

# define global constants
# canvas size: to accommodate 8 cards x 2 rows
WIDTH = 1000 
HEIGHT = 352

card_size = [125, 176]
card_center = [card_size[0]/2, card_size[1]/2]

shuffled_deck = list(range(8)) + list(range(8)) #16 cards

# helper function to initialize globals
def new_game():
    global shuffled_deck, counter, exposed, curr_idx
    
    random.shuffle(shuffled_deck)
    exposed = [False] * len(shuffled_deck)
    curr_idx = []
    
    counter = 0
    label.set_text('Turns = ' + str(counter))

# define event handlers
def mouseclick(pos):
    global exposed, curr_idx, counter
    
    # locate position of mouseclick
    if pos[1] <= 176:
        # first row
        idx = pos[0] / card_size[0]
    else:
        # second row
        idx = pos[0] / card_size[0] + 8
    
    # check if the card is currently facing down
    # before updating exposed, curr_idx and counter
    # to prevent double counting on cards already exposed
    if not exposed[idx]:
        exposed[idx] = True
        if idx not in curr_idx:
            curr_idx.append(idx)
            if len(curr_idx) == 2:
                counter += 1
    
    # check state of the game at the 3rd click
    if len(curr_idx) == 3: 
        if shuffled_deck[curr_idx[0]] != shuffled_deck[curr_idx[1]]:
            # the previous 2 cards are NOT a match
            exposed[curr_idx[0]] = exposed[curr_idx[1]] = False
        # reset curr_idx
        curr_idx = [curr_idx[2]]
    
    # update the counter text
    label.set_text('Turns = ' + str(counter))
    
# def draw handler 
def draw(canvas):
    global exposed
        
    # check if any card is exposed -> draw the front card
    for idx, val in enumerate(exposed):
        if val:
            # shuffled_deck[idx] will return a value in range(8)
            # which can be used to locate the corresponding image in the cards list
            image = cards[shuffled_deck[idx]]
            canvas.draw_image(image, front_card_center, front_card_size,
                              [(idx % 8) * card_size[0] + card_size[0]/2,
                              (idx // 8) * card_size[1] + card_size[1]/2], card_size)
        else:
            # draw the back of the cards
            canvas.draw_image(back_card, back_card_center, back_card_size,
                              [(idx % 8) * card_size[0] + card_size[0]/2,
                              (idx // 8) * card_size[1] + card_size[1]/2], card_size)
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
