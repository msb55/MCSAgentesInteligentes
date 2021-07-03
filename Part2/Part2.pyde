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
import math

# The map squared default size
map_size = 660

# The size in pixel of a floor (safe or not)
floor_size = 33

# The map representation:
# 0: safe floor
# 1: obstacle (agent cant pass through)
# 2: sand
# 3: mud
# 4: water
map_matrix = [
              [0, 3, 3, 4, 4, 4, 4, 4, 3, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2],
              [0, 0, 3, 4, 4, 4, 4, 4, 4, 3, 0, 0, 1, 0, 2, 3, 3, 3, 3, 2],
              [1, 0, 0, 3, 4, 4, 4, 4, 4, 4, 3, 0, 1, 0, 2, 3, 4, 4, 3, 2],
              [1, 1, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0, 1, 0, 2, 3, 3, 3, 3, 2],
              [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 2, 2, 2, 2, 2],
              [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 0, 2, 2, 2, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0],
              [0, 0, 0, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
              [0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0],
              [0, 0, 2, 2, 0, 2, 4, 4, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
              [0, 0, 2, 2, 0, 2, 2, 4, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 4, 4, 4, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 4, 3, 4, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2],
              [0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2],
              [0, 3, 3, 0, 0, 4, 4, 4, 0, 0, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3],
              [0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3],
              [3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4],
              [3, 3, 3, 3, 0, 0, 1, 1, 1, 0, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4],
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4],
              [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4],
              ]

# Defines the cost for each type of floor
# 0: no cost
# 1: maximum cost
# 2: cost of 5
# 3: cost of 10
# 4: cost of 20
ground_cost = {
               0: 0,
               1: 999,
               2: 5,
               3: 10,
               4: 20
               }

#Defines the color for each type of floor (for #5 is white due target location)
ground_color = {
                0: (255, 204, 204),
                1: (0, 0, 0),
                2: (225, 225, 0),
                3: (153, 76, 0),
                4: (0, 128, 255),
                5: (255, 255, 255)
                }

# Global variables for target location in map
target_x = random.randint(0, len(map_matrix)-1)
target_y = random.randint(0, len(map_matrix)-1)

# Enable the update_target_position to reload target position
change_target_position = True

# Iterates over the map representation to draw the map (safe floor, obstacle, sand, mud and water)
def draw_map():
    for i in range(0, len(map_matrix)):
        for j in range(0, len(map_matrix)):
            floor_type = map_matrix[i][j]
            r, g, b = ground_color[floor_type]
            fill(r, g, b)
            rect(i*floor_size, j*floor_size, floor_size, floor_size, 2)

# Updates the global variables of the target position to a valid one (not into a obstacle)
def update_target_position():
    global target_x
    global target_y
    
    while map_matrix[target_x][target_y] == 1:
        target_x = random.randint(0, len(map_matrix)-1)
        target_y = random.randint(0, len(map_matrix)-1)

    change_target_position = False

# Draw the target star-based symbol in map
def draw_target():
    global map_matrix
    global target_x
    global target_y
    
    x_calc = (target_x * floor_size) + math.ceil(floor_size / 2) + 1
    y_calc = (target_y * floor_size) + math.ceil(floor_size / 2) + 1
    
    translate(x_calc, y_calc)
    star = createShape()
    star.beginShape()
    star.fill(255, 0, 0)
    star.stroke(155, 0, 0)
    star.strokeWeight(2)
    star.vertex(0, -50)
    star.vertex(14, -20)
    star.vertex(47, -15)
    star.vertex(23, 7)
    star.vertex(29, 40)
    star.vertex(0, 25)
    star.vertex(-29, 40)
    star.vertex(-23, 7)
    star.vertex(-47, -15)
    star.vertex(-14, -20)
    star.scale(0.3)
    star.endShape(CLOSE)
    
    shape(star)


def setup():
    size(map_size, map_size)


def draw():
    background(255)
    noStroke()
    
    update_target_position()
    map_matrix[target_x][target_y] = 5
    
    draw_map()
    draw_target()   
