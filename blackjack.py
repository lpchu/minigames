# Mini-project #6 - Blackjack
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui  
import random

# load casino background
# source: https://superlenny.com/gb/lennytalks/live-blackjack-guide/
background = simplegui.load_image('https://i.imgur.com/jxWkDi9.jpg')
BACKGROUND_SIZE = (1000, 667) #ratio-lock ~1.5
BACKGROUND_CENTER = (1000/2, 667/2)

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = 'Enter your bet and press Deal to start!'

start_money = 500
money_left = 500
bet = 0
wins = 0
losses = 0
counter = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define globals for canvas
WIDTH = 900
HEIGHT = 600

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        
    def __str__(self):
        # return a string representation of a hand
        s = 'Hand contains: '
        for card in self.cards:
            s += card.get_suit() + card.get_rank() + ' '
        return s

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        hand_value = 0
        ace_count = 0
        for card in self.cards:
            hand_value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                ace_count += 1

        while ace_count > 0:
            if hand_value + 10 <= 21:
                hand_value += 10
            ace_count -= 1
            
        return hand_value
    
    def draw(self, canvas, init_pos):
        for card in self.cards:
            card.draw(canvas, init_pos)
            init_pos[0] += CARD_SIZE[0] / 2
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()	# deal a card object from the deck
    
    def __str__(self):
        # return a string representing the deck
        s = 'Hand contains: '
        for card in self.cards:
            s += card.get_suit() + card.get_rank() + ' '
        return s

# define event handlers for buttons
def deal():
    global outcome, in_play, wins, losses, bet, money_left
    global deck, player_hand, dealer_hand, counter
    
    
    # initialise a new deck of card and shuffle
    deck = Deck()
    deck.shuffle()
        
    # keep counts of the game
    counter += 1

    # initialise player's and dealer's hands
    player_hand = Hand()
    dealer_hand = Hand()

    # deal 2 cards each to player (first) and dealer
    player_hand.add_card(deck.deal_card()) 
    dealer_hand.add_card(deck.deal_card()) 
    player_hand.add_card(deck.deal_card()) 
    dealer_hand.add_card(deck.deal_card()) 

    # if player presses 'deal' in the middle of the round -> player loses
    if in_play:
        losses += 1
        money_left -= bet

    in_play = True
    outcome = 'Hit or stand?'
    
    # update current balance
    label3.set_text('Current balance: ' + str(money_left) + '$')
                                   
def hit():
    global in_play, outcome, losses, deck, player_hand, bet, money_left
    
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = "You have busted! Enter a new bet or deal again?"
            in_play = False
            losses += 1
            money_left -= bet
    
    # update current balance
    label3.set_text('Current balance: ' + str(money_left) + '$')

def stand():
    global deck, dealer_hand, player_hand
    global in_play, outcome, wins, losses, bet, money_left
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value() > 21:
            outcome = "Dealer has busted! Enter a new bet or deal again?"
            wins += 1
            money_left += bet
            in_play = False
            # update money_left
            label3.set_text('Current balance: ' + str(money_left) + '$')
            return
    else:
        return
    
    # assign a message to outcome, update in_play and score
    if dealer_hand.get_value() < player_hand.get_value():
        outcome = 'You win! Enter a new bet or deal again?'
        wins += 1
        money_left += bet
    else:
        # dealer wins ties
        outcome = 'You lose... Enter a new bet or deal again?'
        losses += 1
        money_left -= bet

    in_play = False
    
    # update current balance
    label3.set_text('Current balance: ' + str(money_left) + '$')

def input_handler(text_input):
    global bet, money_left, outcome, in_play
    
    if not in_play:
        try:
            bet = float(text_input)
            outcome = "Bet registered. Press Deal to play!"
            label1.set_text('Current bet: ' + str(bet) + '$')
        except ValueError:
            outcome = 'Wrong input: enter only numbers!'
    else:
        outcome = "Cards already dealt, can't change bet amount!"
        
        
#=============================================================
dealer_hand = Hand()
player_hand = Hand()

# draw handler    
def draw(canvas):
    global in_play, card_images, card_back, wins, losses, outcome, counter
    
    # draw canvas background
    canvas.draw_image(background, BACKGROUND_CENTER, BACKGROUND_SIZE,
                      [WIDTH/2, HEIGHT/2], [WIDTH, HEIGHT])
    
    # draw some texts
    canvas.draw_text("Dealer's hand", [4*CARD_CENTER[0], CARD_CENTER[1]/2+10], 30, 'White')
    canvas.draw_text("Your hand", [4*CARD_CENTER[0], HEIGHT * 5/6 + CARD_CENTER[1] * 3/2], 30, 'White')
    canvas.draw_text(outcome, (2*CARD_SIZE[0], HEIGHT * 1/2), 35, 'Maroon') 
    canvas.draw_text('Blackjack', (WIDTH * 2/3, 60), 50, 'Black')
    canvas.draw_text('Game # ' + str(counter), (WIDTH*2/3, HEIGHT*2/3), 50, 'Black')
    
    canvas.draw_text('Wins: ' + str(wins), (WIDTH * 2/3, 100), 30, 'Black')
    canvas.draw_text('Losses: ' + str(losses), (WIDTH * 2/3, 130), 30, 'Black')
    
    # draw player_hand at the bottom of the canvas
    player_hand.draw(canvas, [4*CARD_CENTER[0], CARD_CENTER[1] + HEIGHT * 2/3])
    dealer_hand.draw(canvas, [4*CARD_CENTER[0], CARD_CENTER[1]])
    
    # when the player is still playing, hide one card of the dealer
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                          [6*CARD_CENTER[0], 2*CARD_CENTER[1]], CARD_SIZE)
    else:
        canvas.draw_text(str(dealer_hand.get_value()), [5*CARD_SIZE[0], CARD_CENTER[1]/2+10], 30, 'White')
        canvas.draw_text(str(player_hand.get_value()), [5*CARD_SIZE[0], HEIGHT * 5/6 + CARD_CENTER[1] * 3/2], 30, 'White')
     
    
# initialization frame
frame = simplegui.create_frame("Blackjack", WIDTH, HEIGHT)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)
frame.add_input('Enter your bet: ', input_handler, 200)

label1 = frame.add_label('Current bet: ' + str(bet) + '$')
label2 = frame.add_label('You start with ' + str(start_money) + '$')
label3 = frame.add_label('Current balance: ' + str(money_left) + '$')

# get things rolling
frame.start()
