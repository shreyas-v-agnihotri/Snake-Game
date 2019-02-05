# Simple retro snake game
# Instructions: Space to start, WASD to move, P to pause, Q to quit
# Author: Shreyas Agnihotri
# Credit to Dartmouth COSC department for cs1lib graphics library
# March 2018

from cs1lib import *
from point import *
import math
import random

# Global constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
FRAME_RATE = 10
BOX_WIDTH = 20          # Standard width of grid tile
START_BODY_LENGTH = 5

# Global variables
box_list = []           # Represents snake body; array of points for top corner of each body piece
game_on = False
first_game = True
accepting_key = True    # Records whether keyboard commands should be registered
score = 0
end_score = score
direction = "right"     # Snake starts on left side of screen and moves right
paused = False
needs_food = True
food = Point(0, 0)

# Inserts points into snake body array (number determined by global constant)
def create_initial_snake():
    global box_list
    for i in range(START_BODY_LENGTH):
        box_list.insert(0, Point(int(i * BOX_WIDTH), int(math.ceil((WINDOW_HEIGHT / BOX_WIDTH) / 2)) * BOX_WIDTH))

# Creates black background
def set_background():
    set_clear_color(0, 0, 0)  # black
    clear()

# Draws orange circles at each point in body array
def draw_snake():
    for box in box_list:
        set_fill_color(.9, .52, .25)       # orange
        disable_stroke()
        draw_circle(box.get_x() + int(BOX_WIDTH/2), box.get_y() + int(BOX_WIDTH/2), int(BOX_WIDTH/2))
        enable_stroke()

# Draws cyan rectangle at current position of food
def draw_food():
    set_fill_color(77/256, 255/256, 219/256)    # cyan
    draw_rectangle(food.get_x(), food.get_y(), BOX_WIDTH, BOX_WIDTH)

# Updates food coordinate to new location on grid outside of snake body
def update_food():

    # Places food at snake head temporarily
    food.set_coordinates(box_list[0].get_x(), box_list[0].get_y())
    in_snake = True

    # While food coordinate is within snake
    while(in_snake):
        counter = 0

        # Sets food position to random box within game grid
        food_x = BOX_WIDTH * random.randint(0, WINDOW_WIDTH / BOX_WIDTH - 1)
        food_y = BOX_WIDTH * random.randint(0, WINDOW_HEIGHT / BOX_WIDTH - 1)
        food.set_coordinates(food_x, food_y)

        # Checks that food has not been placed inside snake body
        for i in range(0, len(box_list), 1):
            if(box_list[i].get_x() == food.get_x() and box_list[i].get_y() == food.get_y()):
                counter = counter + 1
        if(counter == 0):
            in_snake = False

# Draws white grid lines across window
def draw_grid():
    set_stroke_color(1, 1, 1)  # white

    # Vertical grid lines
    for i in range(1, int(WINDOW_WIDTH/BOX_WIDTH) + 1):
        line_x = BOX_WIDTH * i
        draw_line(line_x, 0, line_x,  WINDOW_HEIGHT)

    #Horizontal grid lines
    for i in range(1, int(WINDOW_HEIGHT/BOX_WIDTH) + 1):
        line_y = BOX_WIDTH * i
        draw_line(0, line_y, WINDOW_WIDTH, line_y)

# Processes user-inputted key-press and implements appropriate command
def press(key):
    global direction, paused, accepting_key, game_on, end_score

    # Gameplay controls
    if(not paused and accepting_key):   # Check that game is accepting key to avoid double-commands within one frame

        # Changes direction based on key press, if direction change is valid
        # Snake cannot immediately reverse direction (i.e. from down to up)
        if(key == "w" and direction != "down"):     # W key moves snake up
            direction = "up"
            accepting_key = False
        elif(key == "a" and direction != "right"):  # A key moves snake left
            direction = "left"
            accepting_key = False
        elif(key == "s" and direction != "up"):     # S key moves snake down
            direction = "down"
            accepting_key = False
        elif(key == "d" and direction != "left"):   # D key moves snake right
            direction = "right"
            accepting_key = False

    # Game menu controls
    if(key == "p"):                                 # P key pauses/unpauses game
        paused = not paused
    if key == "q":                                  # Q key quits program
        cs1_quit()
    if key == " ":                                  # Space key starts game
        game_on = True

# Shifts points in snake body array by 1 grid unit
def update_snake():

    # Shifts every snake unit to take on position of the next
    for i in range(len(box_list)-1, 0, -1):
        temp_x = box_list[i-1].get_x()
        temp_y = box_list[i-1].get_y()
        box_list[i].set_coordinates(temp_x,temp_y)

    # Moves head by one unit based on current snake direction
    head_x = box_list[0].get_x()
    head_y = box_list[0].get_y()
    if(direction == "right"):
        box_list[0].set_coordinates(head_x + BOX_WIDTH, head_y)
    if (direction == "left"):
        box_list[0].set_coordinates(head_x - BOX_WIDTH, head_y)
    if(direction == "down"):
        box_list[0].set_coordinates(head_x, head_y + BOX_WIDTH)
    if(direction == "up"):
        box_list[0].set_coordinates(head_x, head_y - BOX_WIDTH)

# Checks if snake has collided with food; if so, adds unit to snake body
def check_eaten():
    global score, needs_food

    # Check if snake head is at same position as food
    if(box_list[0].get_x() == food.get_x() and box_list[0].get_y() == food.get_y()):
        needs_food = True
        score += 1

        # Store coordinates of current snake tail
        end_x = box_list[len(box_list) - 1].get_x()
        end_y = box_list[len(box_list) - 1].get_y()

        # If single-length snake, add new body unit to opposite side of head (compared to moving direction)
        if(len(box_list) == 1):
            if(direction == "up"):
                box_list.append(Point(end_x, end_y + BOX_WIDTH))
            elif(direction == "down"):
                box_list.append(Point(end_x, end_y - BOX_WIDTH))
            elif(direction == "left"):
                box_list.append(Point(end_x + BOX_WIDTH, end_y))
            elif(direction == "right"):
                box_list.append(Point(end_x - BOX_WIDTH, end_y))

        # If not single-length snake, could have corner in body)
        # Add new body unit to opposite side of last and second-to-last units (compared to moving direction)
        else:
            next_x = box_list[len(box_list)-2].get_x()
            next_y = box_list[len(box_list)-2].get_y()
            (x, y) = (end_x - next_x, end_y - next_y)
            if(x == 0 and y > 0):
                box_list.append(Point(end_x, end_y + BOX_WIDTH))
            elif(x == 0 and y < 0):
                box_list.append(Point(end_x, end_y - BOX_WIDTH))
            elif(x > 0 and y == 0):
                box_list.append(Point(end_x + BOX_WIDTH, end_y))
            elif(x < 0 and y == 0):
                box_list.append(Point(end_x - BOX_WIDTH, end_y))

# Checks if snake has collided with a wall; if so, ends game
def check_wall():
    global game_on, first_game, end_score

    head_x = box_list[0].get_x()
    head_y = box_list[0].get_y()

    # Check head location for right, left, bottom, and top wall
    if(head_x == WINDOW_WIDTH - BOX_WIDTH and direction == "right"):
        game_on = False
        first_game = False
        end_score = score
    if(head_x == 0 and direction == "left"):
        game_on = False
        first_game = False
        end_score = score
    if (head_y == WINDOW_HEIGHT - BOX_WIDTH and direction == "down"):
        game_on = False
        first_game = False
        end_score = score
    if (head_y == 0 and direction == "up"):
        game_on = False
        first_game = False
        end_score = score

# Checks if snake has collided with its own body; if so, ends game
def check_contact():
    global game_on, first_game, end_score

    head_x = box_list[0].get_x()
    head_y = box_list[0].get_y()

    # Check that no unit in snake body is at same position as head
    for i in range(1, len(box_list), 1):
        if (box_list[i].get_x() == head_x and box_list[i].get_y() == head_y):
            game_on = False
            first_game = False
            end_score = score

# Creates, draws, and updates game for every frame
def game():
    global needs_food, accepting_key, score, box_list, first_game, direction
    set_background()

    if not game_on:

        # Lists score if a game has already been playes
        if not first_game:
            game_over_message_x = int(WINDOW_WIDTH * 2 / 5) - WINDOW_WIDTH/BOX_WIDTH
            game_over_message_y = WINDOW_HEIGHT/2 - WINDOW_HEIGHT/10
            draw_text("Game over! Your score was: " + str(end_score), game_over_message_x, game_over_message_y)

        # Resets all variables to defaults and prints starting instructions
        score = 0
        box_list = []
        direction = "right"
        create_initial_snake()
        needs_food = True
        set_stroke_color(1, 1, 1)

        start_instructions_x = int(WINDOW_WIDTH * 2/5)
        start_instructions_y = WINDOW_HEIGHT/2
        control_instructions_x = int(WINDOW_WIDTH * 29/90)
        control_instructions_y = WINDOW_HEIGHT/2 + WINDOW_HEIGHT/BOX_WIDTH
        draw_text("Press space to begin!", start_instructions_x, start_instructions_y)
        draw_text("WASD to move, P to pause, Q to quit", control_instructions_x, control_instructions_y)

    if game_on:

        # Updates positions
        if(not paused):
            update_snake()
            accepting_key = True
        if(needs_food):
            update_food()
            needs_food = False

        # Draws game interface
        draw_grid()
        draw_food()
        draw_snake()

        # Handles gameplay
        check_eaten()
        check_wall()
        check_contact()

        # Displays score
        draw_text("Score: " + str(score), WINDOW_WIDTH - 75, BOX_WIDTH)

start_graphics(game, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, key_press=press, framerate=FRAME_RATE)