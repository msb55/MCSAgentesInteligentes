# The Nature of Code
# Daniel Shiffman
# http://natureofcode.com

# The "Path" class

# Atualizado por: Larissa Britto and Marcos Barreto
# Centro de Informatica - UFPE 2021.1 (Pos-Graduacao)
# Introducao a Agentes Inteligentes

class Path():

    def __init__(self):
        self.points = []
        self.radius = 10

    def addPoint(self, x, y):
        point = PVector(x, y)
        self.points.append(point)

    def getStart(self):
        return self.points[0]

    def getEnd(self):
        return self.points[-1]

    def display(self):
        # Draw thick line for radius
        stroke(175)
        strokeWeight(self.radius*2)
        noFill()
        beginShape()

        for v in self.points:
            vertex(v.x, v.y)

        endShape()

        # Draw thin line for center of path
        stroke(0)
        strokeWeight(1)
        noFill()
        beginShape()

        for v in self.points:
            vertex(v.x, v.y)

        endShape()
