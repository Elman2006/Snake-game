# -------------------------- modules ------------------------------
from tkinter import Tk, Canvas, Label, Button, ALL # Import what we need from tkinter and avoid other
from random import randint # we just need random intigers
import os
import sys

# -------------------------- variables -------------------------------
GAME_WIDTH = 500
GAME_HEIGHT = 500
SPACE_SIZE = 25  # SPACE_SIZE % GAME_WIDTH = 0, SPACE_SIZE % GAME_HEIGHT = 0
BODY_SIZE = 2 # How many squers will the snake have? and when snake eats, it is going to increase
GAME_SPEED = 150 # Decrease speed by increasing number
BG_COLOR = "#3E5F44"
SNAKE_CLR = "#93DA97"
FOOD_CLR = "#E8FFD7"
score = 0
direction = "down" # default first move


# --------------------------- Classes -------------------------------------
class Snake:
    """ To make an object of our snake, to develop better """
    def __init__(self):
        self.body_size = BODY_SIZE
        self.coordinates = []
        self.squers = []

        for i in range(0, BODY_SIZE):
            self.coordinates.append([0, 0])
        
        for x, y in self.coordinates:
            # We use a loop to creat snake's body squers with tkinter's canvas
            squer = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_CLR, tag = "snake")
            self.squers.append(squer)


class Food:
    """ An object to creat foods """
    def __init__(self):
        x = randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE # Make a random x for food
        y = randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE # Make a random y for food

        self.coordinate = [x, y]
        # canvas.create_oval() will create us an oval, but if we give it x=y, it will be a circle
        canvas.create_oval(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=FOOD_CLR, tag="food")


# -------------------------- functions ----------------------------------
def check_game_over(snake):
    """ Checks for the gameover via .... """

    head_x, head_y = snake.coordinates[0]

    # Checks for borders
    if head_x < 0 or head_x >= GAME_WIDTH or head_y < 0 or head_y >= GAME_HEIGHT:
        return True

    # Check for body collection
    if [head_x, head_y] in snake.coordinates[1:]:
        return True

    return False

def game_over():
    """ What happens, when check_game_over() returns True? """

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=("Terminal",50), text="Game over", fill="red", tag="game_over")


def change_direction(new_dir):
    """ A function to change the direction, and ignor reverse movement """
    
    global direction

    match new_dir:
        case "left" if direction != "right": direction = new_dir
        case "right" if direction != "left": direction = new_dir
        case "up" if direction != "down": direction = new_dir
        case "down" if direction != "up": direction = new_dir

def movement(snake, food):
    """ Control the movement of the snake """

    x, y = snake.coordinates[0] # snake's head coordinate

    match direction:
        case "up": y -= SPACE_SIZE
        case "down": y += SPACE_SIZE
        case "right": x += SPACE_SIZE
        case "left": x -= SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    squer = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_CLR)
    snake.squers.insert(0, squer)

    # Checks for eating the food, and the squer that have been created won't be delete
    if x == food.coordinate[0] and y == food.coordinate[1]:
        global score
        score +=1
        score_lbl.config(text=f"Score: {score}")
        canvas.delete("food") # using tag to delet the food
        food = Food() # Creat another food
    
    # If there was't any collection, the last squer and it's coordinates will be deleted
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squers[-1])
        del snake.squers[-1]

    if check_game_over(snake):
        game_over()

    else:
        window.after(GAME_SPEED, movement, snake, food)


def restart():
    """ When your click the restart button, it restarts the game"""

    global direction, score, snake, food
    direction = "down"
    score = 0
    score_lbl.config(text=f"Score: {score}")
    canvas.delete("all")
    snake = Snake()
    food = Food()
    movement(snake, food)

    
# -------------------------- Main codes ----------------------------------
window = Tk()

window.title("Snake game") # Make a name for game
window.resizable(False, False) # Make the window unchangable

# score label
score_lbl = Label(window, text=f"Score: {score}", font={"Roman", 30})
score_lbl.pack()

# Main body for drwaing snake and food
canvas = Canvas(window, bg=BG_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Restart button 
restart_btn = Button(window,
                    text="Restart", 
                    width=30,
                    font=("Aria", 12),
                    fg="#2F5249", 
                    bg="#97B067",
                    activebackground="#D6D85D",
                    command=restart)
restart_btn.pack(pady=10)

# Setting the game window to the center
window.update()
window_width = window.winfo_width() # The width of the window GAME_WIDTH(canvas) + a few pixcels  
window_height = window.winfo_height() # The height of the window GAME_HEIGHT(canvas)

# Gets your monitors resolution in pixcel
screen_width = window.winfo_screenwidth() 
screen_height = window.winfo_screenheight()

# Make a (x, y) to centeralize the game window
x = int((screen_width / 2)-(window_width/2))
y = int((screen_height / 2)-(window_height/2))

# Set the window in the center with the x,y and .geometry()
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Check for button presses
window.bind("<Down>", lambda event: change_direction("down"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))

# Make the objects
snake = Snake()
food = Food()
movement(snake, food)

window.mainloop()
