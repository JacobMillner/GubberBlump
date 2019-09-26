import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from PIL import ImageGrab
import time
import keyboard
import pyautogui
import random

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
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        print("min val: " + str(min_val))
        print("max val: " + str(max_val))
        print("min loc: " + str(min_loc))
        print("max loc: " + str(max_loc))

        top_left = max_loc
        pyautogui.moveTo((top_left[0]+x_margin), (top_left[1]+y_margin), duration = 1)
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv.rectangle(img,top_left, bottom_right, 255, 2)
        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle('cv.TM_CCOEFF_NORMED')
        #plt.show()