# The Nature of Code
# Daniel Shiffman
# http://natureofcode.com

# Seeking "vehicle" follows the mouse position

# Implements Craig Reynold's autonomous steering behaviors
# One vehicle "seeks"
# See: http://www.red3d.com/cwr/

# Atualizado por: Larissa Britto and Marcos Barreto
# Centro de Informatica - UFPE 2021.1 (Pos-Graduacao)
# Introducao a Agentes Inteligentes

from Vehicle import Vehicle
import random

max_width = 640
max_height = 360

food_x = random.randint(0, max_width)
food_y = random.randint(0, max_height)

epsilon = 5

food_eaten_counter = 0

def setup():
    global v
    global f
    
    f = createFont("Arial", 16)
    size(max_width, max_height)
    v = Vehicle(width / 2, height / 2)
    

def is_food_eaten(x_position, y_position, x_target, y_target):
    global epsilon
    return abs(x_position - x_target) <= epsilon and abs(y_position - y_target) <= epsilon


def draw():
    global food_eaten_counter
    global food_x
    global food_y
    global f
    
    background(51)
    textFont(f)
    fill(255)
    text('Food eaten: {}'.format(food_eaten_counter), 10, 30)

    mouse = PVector(food_x, food_y)

    # Draw an ellipse at the mouse position
    fill(127)
    stroke(200)
    strokeWeight(2)
    ellipse(mouse.x, mouse.y, 25, 25)

    # Call the appropriate steering behaviors for our agents
    v.arrive(mouse)
    v.update()
    v.display()
    
    v_position = v.position
    if is_food_eaten(v_position[0], v_position[1], mouse.x, mouse.y):
        food_eaten_counter += 1
        food_x = random.randint(0, max_width)
        food_y = random.randint(0, max_height)
