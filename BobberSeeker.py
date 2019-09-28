import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from time import sleep
import keyboard
import pyautogui
from pymouse import PyMouse
import random
from MouseMovement import MouseMovementCalculator

class BobberSeeker:
    def FindBobber(self, img2, template, threshold):
        print(":: Finding Bobber ::")

        x_margin = random.randint(10,40)
        y_margin = random.randint(10,40)

        w, h = template.shape[::-1]

        img = img2.copy()
        method = eval('cv.TM_CCOEFF_NORMED')
        # Apply template Matching
        res = cv.matchTemplate(img,template,method)

        # a threshold to prevent false detection
        
        loc = np.where( res >= threshold)
        if len(loc[0]) != 0:
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            cur_pos = pyautogui.position()
            bobber_pos = ((max_loc[0]+x_margin), (max_loc[1]+y_margin))
            mouse = PyMouse()
            mouseSpeed = 19
            coordsAndDelay = list()
            mouseCalc = MouseMovementCalculator(7, 5, mouseSpeed, 10*mouseSpeed)

            # set up some random crap to make mousemovement more variable
            extra_movement = random.randint(0,100)
            if extra_movement >= 75: # we accidentally missed
                print("and I oop...")
                x_oops = random.randint(200,400)
                y_oops = random.randint(200,400)
                oops_sleep = (random.randint(200, 1500) / 1000)
                oops_loc = bobber_pos = ((max_loc[0]+x_oops), (max_loc[1]+y_oops))
                coordsAndDelay += mouseCalc.calcCoordsAndDelay(cur_pos, oops_loc)
                sleep(oops_sleep)
                coordsAndDelay += mouseCalc.calcCoordsAndDelay(oops_loc, bobber_pos)
            else:
                # just normal mouse move
                coordsAndDelay += mouseCalc.calcCoordsAndDelay(cur_pos, bobber_pos)
            
            # fire 'er off!
            for x, y, delay in coordsAndDelay:
                mouse.move(round(x), round(y))
                sleep(delay/1000)
            return True
        else:
            # we failed to detect the object
            print(":: Mission failed!")
            return False