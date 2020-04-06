"""
The program is to implement Craig Reynolds’ Boids System
"""

from tkinter import *
import math
import random
from datetime import datetime


class Boid:  # boid class defines basic elements
    def __init__(self, x, y):
        self.velocity_x = random.randint(20, 50)
        self.velocity_y = random.randint(20, 50)
        if self.velocity_x == 0 or self.velocity_y == 0:
            pass
        self.new_velocity_x = self.velocity_x  # make all bois update at the same time
        self.new_velocity_y = self.velocity_y
        self.neighbors = []
        self.perchCount = 0
        try:
            self.angle = math.atan2(self.velocity_y, self.velocity_x)  # in radians
        except ZeroDivisionError:
            if self.velocity_y >= 0:
                self.angle = math.pi / 2
            else:
                self.angle = -math.pi / 2
        self.x = x
        self.y = y

    def getPoints(self):  # get the points position for draw a boid
        H = 12  # the height for the boids
        fwd = (-6 + 4 * math.sqrt(3)) * H
        bck = (3 * math.sqrt(6) - 5 * math.sqrt(2)) * H
        return [self.x + fwd * math.cos(self.angle), self.y + fwd * math.sin(self.angle),
                self.x + bck * math.cos(self.angle + math.radians(105)),
                self.y + bck * math.sin(self.angle + math.radians(105)),
                self.x + bck * math.cos(self.angle - math.radians(105)),
                self.y + bck * math.sin(self.angle - math.radians(105))]

    def updateVelocity(self, velocity):
        self.new_velocity_x += velocity[0]
        self.new_velocity_y += velocity[1]

    def updatePosition(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        try:
            self.angle = math.atan2(self.new_velocity_y, self.new_velocity_x)  # in radians
        except ZeroDivisionError:
            if self.velocity_y >= 0:
                self.angle = math.pi / 2
            else:
                self.angle = -math.pi / 2

        # make all bois update at the same time
        self.velocity_x = self.new_velocity_x / 50
        self.velocity_y = self.new_velocity_y / 50

    @staticmethod
    def isNeighbor(boid, neighbor):  # this function used for determin if two boids are neighbor
        if ((neighbor.x - boid.x) ** 2 + (neighbor.y - boid.y) ** 2 <= 3600) and (
                neighbor != boid):  # neighbor radius = 60,out angle= 20deg to -20deg
            try:
                if boid.angle >= 0:
                    angle = math.degrees(
                        math.atan2(neighbor.y - boid.y, neighbor.x - boid.x) - (math.pi - boid.angle))  # to degrees
                else:
                    angle = math.degrees(
                        math.atan2(neighbor.y - boid.y, neighbor.x - boid.x) - (-math.pi - boid.angle))  # to degrees
            except ZeroDivisionError:
                return True
            if angle > 20 or angle < -20:
                return True
            else:
                return False

    @staticmethod
    def Cohesion(boid):
        sumX = 0
        sumY = 0
        if len(boid.neighbors) == 0:
            return 0, 0
        for neighbor in boid.neighbors:
            if not (Boid.isNeighbor(boid, neighbor)):  # no longer neighbor
                boid.neighbors.remove(neighbor)
                continue
            sumX += neighbor.x
            sumY += neighbor.y
        if len(boid.neighbors) > 0:
            sumX /= len(boid.neighbors)
            sumY /= len(boid.neighbors)
        return (sumX - boid.x) / 50, (sumY - boid.y) / 50

    @staticmethod
    def Separation(boid):
        sumX = 0
        sumY = 0
        for neighbor in boid.neighbors:
            if not (Boid.isNeighbor(boid, neighbor)):  # no longer neighbor
                boid.neighbors.remove(neighbor)
                continue
            if (neighbor.x - boid.x) ** 2 + (neighbor.y - boid.y) ** 2 < 625:  # too close radius = 25
                sumX -= (neighbor.x - boid.x)
                sumY -= (neighbor.y - boid.y)
        return sumX / 8, sumY / 8

    @staticmethod
    def Alignment(boid):
        sumX = 0
        sumY = 0
        if len(boid.neighbors) == 0:
            return 0, 0
        for neighbor in boid.neighbors:
            if not (Boid.isNeighbor(boid, neighbor)):  # no longer neighbor
                boid.neighbors.remove(neighbor)
                continue
            sumX += neighbor.velocity_x
            sumY += neighbor.velocity_y
        if len(boid.neighbors) > 0:
            sumX /= len(boid.neighbors)
            sumY /= len(boid.neighbors)
        return (sumX - boid.velocity_x) / 4, (sumY - boid.velocity_y) / 4

    @staticmethod
    def tendToCenter(boid):
        centerX = 400
        centerY = 500
        return (centerX - boid.x) / 1000, (centerY - boid.y) / 1000


class Graph:
    def __init__(self, boidNum, WIDTH=800, HEIGHT=800):
        self.count = 0  # for later use
        self.boids = []  # collection for boids
        self.windX = random.randint(-30, 30) / 50
        while abs(self.windX) < 0.3:
            self.windX = random.randint(-30, 30) / 50
        for i in range(boidNum):
            self.boids.append(Boid(random.randint(200, 600), random.randint(300, 600)))

        # GUI init
        self.root = Tk()
        self.root.overrideredirect(True)
        self.root.geometry("%dx%d+%d+%d" % (
        WIDTH, HEIGHT, (self.root.winfo_screenwidth() - WIDTH) / 2, (self.root.winfo_screenheight() - HEIGHT) / 2))
        self.root.bind_all("<Escape>", lambda event: event.widget.destroy())  # esc to quit
        self.graph = Canvas(self.root, width=WIDTH, height=HEIGHT, background="white")
        self.graph.after(500, self.update)
        self.graph.pack()
        self.root.mainloop()

    def update(self):  # update the display
        start = datetime.now()
        self.graph.delete(ALL)
        self.graph.create_text(600, 100, font=("Georgia", 16, "bold"), text="Press <ESC> to exit", fill="blue")
        self.count += 1  # time count
        self.graph.create_line(0, 700, 800, 700)  # the ground line
        for boid in self.boids:  # Draw
            self.graph.create_polygon(boid.getPoints())
            for boid_again in self.boids:  # get neighbors
                if boid_again in boid.neighbors:
                    continue
                if Boid.isNeighbor(boid, boid_again):  # neighbor radius = 60,out angle= 20deg to -20deg
                    boid.neighbors.append(boid_again)
            boid.updateVelocity(Boid.Cohesion(boid))
            boid.updateVelocity(Boid.Separation(boid))
            boid.updateVelocity(Boid.Alignment(boid))
            boid.updateVelocity(Boid.tendToCenter(boid))

        for boid in self.boids:  # Move to new position
            boid.updatePosition()

        # delay = 20ms
        delay = int(20 + (start - datetime.now()).total_seconds() * 1000)
        self.graph.after(delay, self.update)



if __name__ == "__main__":
    # main function entry
    graph = Graph(40)

