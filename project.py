from microbit import *
import music

# INSTRUCTIONS
# Press any button to start
# The turn is indicated by a 1 or a 2
# Use A to change the column to drop the chip in
# The position that the chip will be dropped in is indicated by a flashing light
# Use B to drop the chip
# Player 1's chips are indicated with maximum brightness (9)
# Player 2's chips are indicated with half brightness (4)
# Get 4 in a row to win


# function to find winner and the 4 cells they won in
def check_winner(board):
    # loop over each cell as a potential start point for a win
    for row in range(5):
        for col in range(5):
            # check left to right
            if col <= 1 and board[row][col] != "0" and board[row][col] == board[row][col + 1] == board[row][col + 2] == \
                    board[row][col + 3]:
                return [1 if int(board[row][col]) == 9 else 2,
                        ((row, col), (row, col + 1), (row, col + 2), (row, col + 3))]

            # check top to bottom
            if row <= 1 and board[row][col] != "0" and board[row][col] == board[row + 1][col] == board[row + 2][col] == \
                    board[row + 3][col]:
                return [1 if int(board[row][col]) == 9 else 2,
                        ((row, col), (row + 1, col), (row + 2, col), (row + 3, col))]

            # check diagonal
            if row <= 1 and col <= 1 and board[row][col] != "0" and board[row][col] == board[row + 1][col + 1] == \
                    board[row + 2][col + 2] == board[row + 3][col + 3]:
                return [1 if int(board[row][col]) == 9 else 2,
                        ((row, col), (row + 1, col + 1), (row + 2, col + 2), (row + 3, col + 3))]

            # check other diagonal
            if row >= 3 and col <= 1 and board[row][col] != "0" and board[row][col] == board[row - 1][col + 1] == \
                    board[row - 2][col + 2] == board[row - 3][col + 3]:
                return [1 if int(board[row][col]) == 9 else 2,
                        ((row, col), (row - 1, col + 1), (row - 2, col + 2), (row - 3, col + 3))]

    return [0, None]  # no winner found


# function to find the lowest empty cell in a column
def find_height(game, col):
    for i in range(4, -1, -1):
        if int(game[i][col]) == 0:
            return i


started = False

display.scroll("PRESS START", delay=85, wait=False, loop=True)  # show the prompt message
while not started:  # while the user hasn't started
    if button_a.was_pressed() or button_b.was_pressed():
        started = True
        sfx = ["C5:1", "G5:2"]  # start sound
        music.play(sfx, wait=False)  # play the start sound

# GAME START!
display.scroll("GO!", delay=90)  # 2 player message

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
                display.set_pixel(column, height, 4)  # flash on
        else:
            display.set_pixel(column, height, 0)  # flash off
        # change column
        if button_a.was_pressed():
            display.set_pixel(column, height, 0)  # stop flashing current pixel
            column = (column + 1) % 5  # add to the column or cycle back
            music.play("F5:1", wait=False)  # play sound
            height = find_height(board, column)
        # confirm choice
        if button_b.was_pressed():
            if turn == 1:
                board[height][column] = "9"  # update board
                turn = 2  # change turn
            else:
                board[height][column] = "4"  # update board
                turn = 1  # change turn
            music.play("F#5:3", wait=False)  # play sound
            selected = True
            # construct the board in an image format
            board_image = Image(str(':'.join(''.join(
                str(cell) for cell in row) for row in board)))
            display.show(board_image)  # show the board state
    win_info = check_winner(board)  # get the win info
    winner = win_info[0]  # winner of game
    win_squares = win_info[1]  # cells in which they won

# final steps
end_time = running_time() + 3250  # flash for 3.25 seconds
flash_on = True  # flash toggler

while running_time() < end_time:
    # flash ON or OFF
    for (r, c) in win_squares:
        # flash the pixel depending on who won and whether flash is on or off
        display.set_pixel(c, r, 9 if winner == 1 and flash_on else 4 if winner == 2 and flash_on else 0)
    music.play("C:1", wait=False)
    flash_on = not flash_on  # toggle
    sleep(175)  # wait

# display the victory message
music.play(music.BA_DING, wait=False)  # play victory sound
for i in range(3):
    display.scroll("P%s WINS!" % winner, delay=100)
