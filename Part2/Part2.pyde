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

from A_star import search
from Path import Path
from Vehicle import Vehicle
import random
import math

# Solution path to target
path = None

# Next step on path to agent walk to
path_next_target = None

# Incremental path index
path_index = 0

# Main agent
agent = None

# Distance difference epsilon (in pixels)
epsilon = 5

# The map squared default size
map_size = 660

# The size in pixel of a floor (safe or not)
floor_size = 33

# The middle point in a floor coordinate
mid_floor_size = math.ceil(floor_size / 2) + 1

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

#Defines the color for each type of floor
ground_color = {
                0: (255, 204, 204),
                1: (0, 0, 0),
                2: (225, 225, 0),
                3: (153, 76, 0),
                4: (0, 128, 255)
                }

# Global variables for target location in map
target_x = 4
target_y = 10


# Checks distance difference of two given points on map (using epsilon)
def arrived(x_position, y_position, x_target, y_target):
    global epsilon
    return abs(x_position - x_target) <= epsilon and abs(y_position - y_target) <= epsilon


# Iterates over the map representation to draw the map (safe floor, obstacle, sand, mud and water)
def draw_map():
    for i in range(0, len(map_matrix)):
        for j in range(0, len(map_matrix)):
            floor_type = map_matrix[i][j]
            r, g, b = ground_color[floor_type]
            fill(r, g, b)
            rect(i*floor_size, j*floor_size, floor_size, floor_size, 2)


# Converts a map position [(x, y) - integers] to screen coordinates (in pixels) based on center of a floor
def position_to_coordinate(x, y):
    x_calc = (x * floor_size) + mid_floor_size
    y_calc = (y * floor_size) + mid_floor_size
    return x_calc, y_calc


# Updates the global variables of the target position to a valid one (not into a obstacle and not in the same position as agent)
def update_target_position():
    global target_x
    global target_y
    
    while map_matrix[target_x][target_y] == 1 or arrived(agent.position.x, agent.position.y, *position_to_coordinate(target_x, target_y)):
        target_x = random.randint(0, len(map_matrix)-1)
        target_y = random.randint(0, len(map_matrix)-1)
        
    print('Target coordinates: ', target_x, target_y)


# Draw the target star-based symbol in map
def draw_target():
    global map_matrix
    
    x_calc, y_calc = position_to_coordinate(target_x, target_y)

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
    
    shape(star, x_calc, y_calc)


# Build a Path using positions (based on map)
def build_path(positions):
    global path
    
    # A path is a series of connected points
    # A more sophisticated path might be a curve
    path = Path()
    
    for x, y in positions:
        x_calc, y_calc = position_to_coordinate(x, y)
        path.addPoint(x_calc, y_calc)

    print('Path coordinates: ', path.points)


def setup():
    global agent
    global path_index
    global path
    global path_next_target
    
    size(map_size, map_size)
    build_path(search(map_matrix, (0,0), (4,10)))
    
    path_next_target = path.points[path_index]
    path_index = path_index + 1
    
    agent = Vehicle(path_next_target.x, path_next_target.y)


def draw():
    global agent
    global path_index
    global path
    global path_next_target
    
    background(255)
    noStroke()
    
    draw_map()
    path.display()
    draw_target()
    
    agent.arrive(path_next_target)
    agent.update()
    agent.display()

    # Walk through path
    if arrived(agent.position.x, agent.position.y, path_next_target.x, path_next_target.y) and path_index < len(path.points):
        # Update the next step on Path
        path_next_target = path.points[path_index]
        path_index = path_index + 1
    
    # Check if agent reach its goal
    x_calc, y_calc = position_to_coordinate(target_x, target_y)
    if arrived(agent.position.x, agent.position.y, x_calc, y_calc):
        # Target should reappear in a new random location 
        update_target_position()
    
