# A python 3 version of SRL-6's _humanWindMouse from /lib/core/mouse.simba with modifications.
# Written by GitHub user Bahm
# https://gist.github.com/Bahm/8408ebf5d6aa83d3de8bb09655236888

import math
from pymouse import PyMouse
from random import randint
from time import sleep


class MouseMovementCalculator:
    def __init__(self, gravity, wind, mouseSpeed, targetError):
        self.gravity = gravity
        self.wind = wind
        self.mouseSpeed = mouseSpeed
        self.targetError = targetError

    def calcCoordsAndDelay(self, startCoords, endCoords):
        veloX, veloY = (0, 0)
        coordsAndDelay = []
        xs, ys = startCoords
        xe, ye = endCoords
        totalDist = math.hypot(xs - xe, ys - ye)

        self._windX = 0
        self._windY = 0

        while True:
            veloX, veloY = self._calcVelocity((xs, ys), (xe, ye), veloX, veloY, totalDist)
            xs += veloX
            ys += veloY

            w = round(max(randint(0, max(0, round(100/self.mouseSpeed)-1))*6, 5)*0.9)
            coordsAndDelay.append(( xs, ys, w ))

            if math.hypot(xs - xe, ys - ye) < 1:
                break

        if round(xe) != round(xs) or round(ye) != round(ys):
            coordsAndDelay.append(( round(xe), round(ye), 0 ))

        return coordsAndDelay

    def _calcVelocity(self, curCoords, endCoords, veloX, veloY, totalDist):
        xs, ys = curCoords
        xe, ye = endCoords
        dist = math.hypot(xs - xe, ys - ye)
        self.wind = max(min(self.wind, dist), 1)

        maxStep = None
        D = max(min(round(round(totalDist)*0.3)/7, 25), 5)
        rCnc = randint(0, 5)

        if rCnc == 1:
            D = 2

        if D <= round(dist):
            maxStep = D
        else:
            maxStep = round(dist)

        if dist >= self.targetError:
            self._windX = self._windX / math.sqrt(3) + (randint(0, round(self.wind) * 2) - self.wind) / math.sqrt(5)
            self._windY = self._windY / math.sqrt(3) + (randint(0, round(self.wind) * 2) - self.wind) / math.sqrt(5)
        else:
            self._windX = self._windX / math.sqrt(2)
            self._windY = self._windY / math.sqrt(2)

        veloX = veloX + self._windX
        veloY = veloY + self._windY
        
        if(dist != 0):
            veloX = veloX + self.gravity * (xe - xs) / dist
            veloY = veloY + self.gravity * (ye - ys) / dist

        if math.hypot(veloX, veloY) > maxStep:
            randomDist = maxStep / 2.0 + randint(0, math.floor(round(maxStep) / 2))
            veloMag = math.sqrt(veloX * veloX + veloY * veloY)
            veloX = (veloX / veloMag) * randomDist
            veloY = (veloY / veloMag) * randomDist

        return (veloX, veloY)


if __name__ == '__main__':
    mouse = PyMouse()
    width, height = mouse.screen_size()

    mouseSpeed = 30
    center = (width/2, height/2)
    topLeft = (0, 0)
    topRight = (width, 0)
    bottomLeft = (0, height)
    bottomRight = (width, height)

    mouseCalc = MouseMovementCalculator(7, 5, mouseSpeed, 10*mouseSpeed)
    coordsAndDelay = mouseCalc.calcCoordsAndDelay(center, topLeft)
    coordsAndDelay += mouseCalc.calcCoordsAndDelay(topLeft, center)
    coordsAndDelay += mouseCalc.calcCoordsAndDelay(center, topRight)
    coordsAndDelay += mouseCalc.calcCoordsAndDelay(topRight, center)
    coordsAndDelay += mouseCalc.calcCoordsAndDelay(center, bottomRight)
    coordsAndDelay += mouseCalc.calcCoordsAndDelay(bottomRight, center)
    coordsAndDelay += mouseCalc.calcCoordsAndDelay(center, bottomLeft)
    coordsAndDelay += mouseCalc.calcCoordsAndDelay(bottomLeft, center)

    mouse.move(round(center[0]), round(center[1]));

    for x, y, delay in coordsAndDelay:
        mouse.move(round(x), round(y))
        sleep(delay/1000)
