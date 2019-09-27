import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from PIL import ImageGrab
import time
import keyboard
import pyautogui
from pymouse import PyMouse
import random
from MouseMovement import MouseMovementCalculator

while True:
    if keyboard.is_pressed('q'):
        break
    if keyboard.is_pressed('1'):
        sleep_time = random.randint(1,4)
        x_margin = random.randint(10,40)
        y_margin = random.randint(10,40)

        print('Sleep Time:' + str(sleep_time))
        print('x margin: ' + str(x_margin))
        print('y margin: ' + str(y_margin))
        time.sleep(sleep_time)
        screenshot = ImageGrab.grab()
        screenshot.save("sreengrab.jpg")
        img = cv.imread("sreengrab.jpg",0)
        img2 = img.copy()
        template = cv.imread('test_bobber.jpg',0)
        w, h = template.shape[::-1]

        img = img2.copy()
        method = eval('cv.TM_CCOEFF_NORMED')
        # Apply template Matching
        res = cv.matchTemplate(img,template,method)
        # debugging
        #threshhold = 0.70
        #loc = np.where( res >= threshhold)
        #print("loc thresh: " + str(loc))
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        cur_pos = pyautogui.position()
        bobber_pos = ((max_loc[0]+x_margin), (max_loc[1]+y_margin))
        mouse = PyMouse()
        mouseSpeed = 30
        mouseCalc = MouseMovementCalculator(7, 5, mouseSpeed, 10*mouseSpeed)
        coordsAndDelay = mouseCalc.calcCoordsAndDelay(cur_pos, bobber_pos)
        for x, y, delay in coordsAndDelay:
            mouse.move(round(x), round(y))
            time.sleep(delay/1000)
        print("Current Mouse Position: " + str(cur_pos))
        print("min val: " + str(min_val))
        print("max val: " + str(max_val))
        print("min loc: " + str(min_loc))
        print("max loc: " + str(max_loc))