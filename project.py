from microbit import *

# GET 4 IN A ROW TO WIN!

# Instructions
# Select single player or two player
# Button A - single player
# Button B - two player

# Single player - use A to change the column to drop the chip in
# The position that the chip will be dropped in is indicated by a flashing light
# Use B to drop the chip
# Wait for the bot to place and then it's your turn again
# Your chips are indicated with maximum brightness (9)
# The bot's chips are indicated with half brightness (4)
# Connect 4 to win

# Two player - use A to change the column


def check_winner():  # function to check winner
    pass


def find_height(board, col):  # function to find the topmost empty cell in a column
    for i in range(4, -1, -1):
        if int(board[col][i]) == 0:
            return i


choice = 0  # 0 - undecided, 1 - single player, 2 - two player

display.scroll("A-1P   B-2P  ", delay=120, wait=False, loop=True)  # show the prompt message
while choice == 0:  # while the user is still undecided
    if button_a.is_pressed():  # single player
        choice = 1
    elif button_b.is_pressed():  # two player
        choice = 2

# GAME START!
if choice == 1:
    display.scroll("1P GO!", delay=120)  # 1 player message
else:
    display.scroll("2P GO!", delay=120)  # 2 player message

if choice == 2:  # implementation for two player
    # setup variables
    turn = 1  # player 1 turn or player 2 turn
    winner = 0  # 0 - still playing, 1 - player 1 won, 2 - player 2 won
    board = [["0", "0", "0", "0", "0"], 
             ["0", "0", "0", "0", "0"], 
             ["0", "0", "0", "0", "0"],
             ["0", "0", "0", "0", "0"],
             ["0", "0", "0", "0", "0"]]  # game board as a 2D list
    board_image = Image()  # game board as an Image
    column = 0  # currently selected column, 0 is leftmost

    # main game loop
    while not winner:  # while game is still going on
        display.show(turn)  # show the current turn
        sleep(900)
        display.show(board_image)  # show the board state
        selected = False  # player has finished selecting a column?
        while not selected:
            if turn == 1:
                display.set_pixel(column, find_height(board, column), 9)
            else:
                display.set_pixel(column, find_height(board, column), 5)
            if button_a.was_pressed():  # change column
                column += 1
                if column >= 4:  # cycle back
                    column = 0
            if button_b.was_pressed():
                pass
                    


