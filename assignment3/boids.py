"""
Craig Reynolds’ boid system
"""

from tkinter import *
import random as r
import math
from datetime import datetime  as dt

# The basic flocking model consists of three simple steering behaviors 
# which describe how an individual boid maneuvers based on the positions and velocities its nearby flockmates
class Boid:
    # initialization of boids
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity_x = r.randint(10, 40)
        self.velocity_y = r.randint(10, 40)
        self.new_v_x = self.velocity_x
        self.new_v_y = self.velocity_y
        self.neighbors = []
        try:
            self.angle = math.atan2(self.velocity_y, self.velocity_x)
        except ZeroDivisionError:
            if self.velocity_y >= 0:
                self.angle = math.pi / 2
            else:
                self.angle = -math.pi / 2

    # points position for a boid, a, b is the size of boid
    def getBoidPosition(self):  
        a = 5 
        b = 2 
        return [self.x + a * math.cos(self.angle), self.y + a * math.sin(self.angle),
                self.x + b * math.cos(self.angle + math.radians(100)),
                self.y + b * math.sin(self.angle + math.radians(100)),
                self.x + b * math.cos(self.angle - math.radians(100)),
                self.y + b * math.sin(self.angle - math.radians(100))]

    def update_velocity(self, velocity):
        self.new_v_x += velocity[0]
        self.new_v_y += velocity[1]

    def update_position(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        try:
            self.angle = math.atan2(self.new_v_y, self.new_v_x)  # in radians
        except ZeroDivisionError:
            if self.velocity_y >= 0:
                self.angle = math.pi / 2
            else:
                self.angle = -math.pi / 2
        self.velocity_x = self.new_v_x / 50
        self.velocity_y = self.new_v_y / 50

    # check if two boids are neighbors
    @staticmethod
    def isNeighbor(boid1, boid2):
        if ( abs(boid2.x - boid1.x) + abs(boid2.y - boid1.y)  <= 60) and ( boid2 != boid1):
            try:
                if boid1.angle >= 0:
                    angle = math.degrees(math.atan2(boid2.y - boid1.y, boid2.x - boid1.x) - (math.pi - boid1.angle))
                else:
                    angle = math.degrees(math.atan2(boid2.y - boid1.y, boid2.x - boid1.x) - (-math.pi - boid1.angle))
            except ZeroDivisionError:
                return True
            return True if angle > 20 or angle < -20 else False

    # rule 1 steer to move toward the average position of local flockmates
    @staticmethod
    def cohension(boid):
        sumX = 0
        sumY = 0
        if len(boid.neighbors) == 0:
            return 0, 0
        for neighbor in boid.neighbors:
            if not (Boid.isNeighbor(boid, neighbor)):  # not neighbor
                boid.neighbors.remove(neighbor)
                continue
            sumX += neighbor.x
            sumY += neighbor.y
        if len(boid.neighbors) > 0:
            sumX /= len(boid.neighbors)
            sumY /= len(boid.neighbors)
        return (sumX - boid.x) / 50, (sumY - boid.y) / 50

    # rule 2  steer to avoid crowding local flockmates
    @staticmethod
    def separation(boid):
        sumX = 0
        sumY = 0
        for neighbor in boid.neighbors:
            if not (Boid.isNeighbor(boid, neighbor)):  # no longer neighbor
                boid.neighbors.remove(neighbor)
                continue
            if abs(neighbor.x - boid.x) + abs(neighbor.y - boid.y)< 25:  # too close
                sumX -= (neighbor.x - boid.x)
                sumY -= (neighbor.y - boid.y)
        return sumX / 8, sumY / 8

    # rule 3 steer towards the average heading of local flockmates
    @staticmethod
    def alignment(boid):
        sumX = 0
        sumY = 0
        if len(boid.neighbors) == 0:
            return 0, 0
        for n in boid.neighbors:
            if not (Boid.isNeighbor(boid, n)):  # no longer neighbor
                boid.neighbors.remove(n)
                continue
            sumX += n.velocity_x
            sumY += n.velocity_y
        if len(boid.neighbors) > 0:
            sumX /= len(boid.neighbors)
            sumY /= len(boid.neighbors)
        return (sumX - boid.velocity_x) / 4, (sumY - boid.velocity_y) / 4

    @staticmethod
    def center(boid, centerX, centerY):
        return (centerX - boid.x) / 1000, (centerY - boid.y) / 1000

# Use TKInter to draw GUI
class Plot_boid:
    def __init__(self, num_of_boids):
        self.count = 0
        self.boids = []
        for i in range(num_of_boids):
            self.boids.append(Boid(r.randint(200, 400), r.randint(300, 500)))
        self.root = Tk()
        self.graph = Canvas(self.root, width=550, height=650, background="#FFFFCC")
        self.graph.after(400, self.update_boids)
        self.graph.pack()
        self.root.mainloop()

    def update_boids(self):
        start = dt.now()
        self.graph.delete(ALL)
        self.count += 1
        for b in self.boids:
            self.graph.create_polygon(b.getBoidPosition(), fill='#FF0033')
            for bn in self.boids:
                if not(bn in b.neighbors) and Boid.isNeighbor(b, bn):
                    b.neighbors.append(bn)
            b.update_velocity(Boid.cohension(b))
            b.update_velocity(Boid.separation(b))
            b.update_velocity(Boid.alignment(b))
            b.update_velocity(Boid.center(b, 400, 500))
        for i in self.boids:
            i.update_position()
        delay = int(16 + (start - dt.now()).total_seconds() * 1000)
        self.graph.after(delay, self.update_boids)


if __name__ == "__main__":
    boids = Plot_boid(50)

