1# The Nature of Code
# Daniel Shiffman
# http://natureofcode.com

# Seeking "vehicle" follows the mouse position

# Implements Craig Reynold's autonomous steering behaviors
# One vehicle "seeks"
# See: http://www.red3d.com/cwr/

# Atualizado por: Larissa Britto and Marcos Barreto
# Centro de Informatica - UFPE 2021.1 (Pos-Graduacao)
# Introducao a Agentes Inteligentes

from Path import Path
from Vehicle import Vehicle
import random

max_width = 640
max_height = 360

# A path object (series of connected points)
path = None

target = None

# One vehicle
car1 = None

epsilon = 5

curr_index = 0

def arrived(x_position, y_position, x_target, y_target):
    global epsilon
    return abs(x_position - x_target) <= epsilon and abs(y_position - y_target) <= epsilon

def setup():
    global car1
    global curr_index
    global path
    global target
    
    size(max_width, max_height)

    newPath()
    
    target = path.points[curr_index]
    curr_index = curr_index + 1

    car1 = Vehicle(target.x, target.y)

def draw():
    global car1
    global curr_index
    global path
    global target

    background(255)
    
    path.display()
    
    car1.arrive(target)
    car1.update()
    car1.display()

    if arrived(car1.position.x, car1.position.y, target.x, target.y):
        target = path.points[curr_index]
        curr_index = curr_index + 1

def newPath():
    global path
    
    # A path is a series of connected points
    # A more sophisticated path might be a curve
    path = Path()
    path.addPoint(0, height/2)
    path.addPoint(random.randint(0, width/2), random.randint(0, height))
    path.addPoint(random.randint(0, width), random.randint(0, height))
    path.addPoint(width, height/2)
