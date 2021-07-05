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

import A_star
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

food_eaten_counter = 0

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
target_x = None
target_y = None

# Global variables for agent location in map
agent_x = None
agent_y = None


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


# Generates randomly a position in map
def generate_random_position():
    return random.randint(0, len(map_matrix)-1), random.randint(0, len(map_matrix)-1)


# Generates randomly a VALID position in map
def generate_valid_position():
    x, y = generate_random_position()
    while map_matrix[x][y] == 1:
        x, y = generate_random_position()

    return x, y


# Checks if the agent is valid
def is_agent_valid():
    return agent is not None and agent.position is not None


# Checks if the target is valid
def is_target_valid():
    return target_x is not None and target_y is not None and (0 >= target_x < len(map_matrix)) and (0 >= target_y < len(map_matrix))


# Updates the global variables of the target position to a valid one (not into a obstacle and not in the same position as agent)
def update_target_position():
    global target_x
    global target_y
    
    target_x, target_y = generate_valid_position()
    while is_agent_valid() and arrived(agent.position.x, agent.position.y, *position_to_coordinate(target_x, target_y)):
        target_x = random.randint(0, len(map_matrix)-1)
        target_y = random.randint(0, len(map_matrix)-1)
        
    print('Target coordinates: ', target_x, target_y)
    

# Updates the global variables of the agent position to a valid one (not into a obstacle and not in the same position as target)
def update_agent_position():
    global agent
    global agent_x
    global agent_y

    agent_x, agent_y = generate_valid_position()    
    while is_target_valid() and arrived(agent_x, agent_y, *position_to_coordinate(target_x, target_y)):
        agent_x, agent_y = generate_valid_position()
    
    agent = Vehicle(*position_to_coordinate(agent_x, agent_y))
    print('Agent coordinates: ', agent_x, agent_y)


# Draws the search evolution: frontier nodes (in blue border) and explored nodes (in red border)
def draw_search():
    fill(255,255,255)
    textFont(createFont("Arial", 16))
    text('Food eaten: {}'.format(food_eaten_counter), 10, 30)

    fill(255,0,0)
    for explored_node in A_star.explored_set:
        x, y = position_to_coordinate(explored_node[0], explored_node[1])
        text('X', x-3, y+5)

    for _, frontier_node in A_star.frontier:
        x, y = frontier_node.state[0], frontier_node.state[1]
        noFill()
        stroke(0, 255 , 0)
        rect(x*floor_size, y*floor_size, floor_size, floor_size, 2)


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
    global path_index
    global path_next_target

    path = Path()
    
    for x, y in positions:
        x_calc, y_calc = position_to_coordinate(x, y)
        path.addPoint(x_calc, y_calc)
        
    path_next_target = path.points[0]
    path_index = 1

    print('Path coordinates: ', positions)


def setup():
    global agent
    global path_index
    global path
    global path_next_target
    
    size(map_size, map_size)
    
    update_target_position()
    update_agent_position()
    
    build_path(A_star.search(map_matrix, (agent_x, agent_y), (target_x, target_y)))


def draw():
    global food_eaten_counter
    global path_index
    global path_next_target
    global agent_x
    global agent_y
    

    background(255)
    noStroke()
    
    draw_map()
    path.display()
    draw_target()
    draw_search()
    
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
        food_eaten_counter += 1
        agent_x, agent_y = target_x, target_y
        update_target_position()
        build_path(A_star.search(map_matrix, (agent_x, agent_y), (target_x, target_y)))
    
