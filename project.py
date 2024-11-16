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
# Your chips are indicated with maximum brightness (w9)
# The bot's chips are indicated with half brightness (4)
# Connect 4 to win

# Two player - use A to change the column to drop the chip in
# The position that the chip will be dropped in is indicated by a flashing light
# Use B to drop the chip
# The turn is indicated by a 1 or a 2 after each round
# Player 1's chips are indicated with maximum brightness (9)
# Player 2's chips are indicated with half brightness (4)
# Connect 4 to win


def check_winner(board):
    # loop over each cell as a potential start point
    for row in range(5):
        for col in range(5):
            # check left to right
            if col <= 1 and board[row][col] != "0" and board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3]:
                return 1 if int(board[row][col]) == 9 else 2

            # check top to bottom
            if row <= 1 and board[row][col] != "0" and board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col]:
                return 1 if int(board[row][col]) == 9 else 2

            # check bottom left to top right
            if row <= 1 and col <= 1 and board[row][col] != "0" and board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3]:
                return 1 if int(board[row][col]) == 9 else 2

            # check diagonal top left to bottom right
            if row >= 3 and col <= 1 and board[row][col] != "0" and board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3]:
                return 1 if int(board[row][col]) == 9 else 2

    return 0  # no winner found


def find_height(game, col):  # function to find the lowest empty cell in a column
    for i in range(4, -1, -1):
        if int(game[i][col]) == 0:
            return i


choice = 0  # 0 - undecided, 1 - single player, 2 - two player

display.scroll("A-1P   B-2P  ", delay=105, wait=False, loop=True)  # show the prompt message
while choice == 0:  # while the user is still undecided
    if button_a.was_pressed():  # single player
        choice = 1
    elif button_b.was_pressed():  # two player
        choice = 2

# GAME START!
if choice == 1:
    display.scroll("1P GO!", delay=90)  # 1 player message
else:
    display.scroll("2P GO!", delay=90)  # 2 player message

if choice == 2:  # implementation for two player
    # setup variables
    turn = 1  # player 1 turn or player 2 turn

    board = [["0", "0", "0", "0", "0"], 
             ["0", "0", "0", "0", "0"], 
             ["0", "0", "0", "0", "0"],
             ["0", "0", "0", "0", "0"],
             ["0", "0", "0", "0", "0"]]  # game board as a 2D list
    winner = 0  # 0 - still playing, 1 - player 1 won, 2 - player 2 won
    board_image = Image()  # game board as an Image
    column = 2  # currently selected column, 0 is leftmost, starts in the middle
    
    # main game loop
    while winner == 0:  # while game is still going on
        column = 2
        display.show(turn)  # show the current turn
        sleep(900)  # wait
        display.show(board_image)
        selected = False  # player has finished selecting a column?

        # variables to set up chip flashing
        last_toggle = running_time()  
        flash_on = True
        
        while not selected:
            height = find_height(board, column)  # find the topmost empty cell

            # flash the currently selected chip
            if running_time() - last_toggle >= 350:  # interval for flashing
                flash_on = not flash_on  # toggle flash
                last_toggle = running_time()  # get running time again
                
            if flash_on:
                if turn == 1:
                    display.set_pixel(column, height, 9)  # flash on
                else:
                    display.set_pixel(column, height, 5)  # flash on
            else:
                display.set_pixel(column, height, 0)  # flash off

            # change column
            if button_a.was_pressed():
                display.set_pixel(column, height, 0)  # stop flashing current pixel
                column = (column + 1) % 5  # add to the column or cycle back
                height = find_height(board, column)

            # confirm choice
            if button_b.was_pressed():
                if turn == 1:
                    board[height][column] = "9"  # update board
                    turn = 2  # change turn
                else:
                    board[height][column] = "5"  # update board
                    turn = 1  # change turn
                selected = True
                # construct the board in an image format
                board_image = Image(str(':'.join(''.join(
                    str(cell) for cell in row) for row in board)))
                display.show(board_image)  # show the board state
        winner = check_winner(board)
        print(winner)
        

                    
