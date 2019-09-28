import keyboard
from time import sleep
from BobberSeeker import BobberSeeker
from PIL import ImageGrab
import random
import cv2 as cv

threshold = 0.65
fish_key = '1'

while True:
    if keyboard.is_pressed('ctrl+q'):
        print(":: Quiting ::")
        break
    if keyboard.is_pressed(fish_key):
        seeking_bobber = True
        seeker = BobberSeeker()
        
        # sleep before looking
        sleep_time = random.randint(1,4)
        print('Sleep Time:' + str(sleep_time))
        sleep(sleep_time)

        # take a screenshot
        screenshot = ImageGrab.grab()
        screenshot.save("sreengrab.jpg")
        img = cv.imread("sreengrab.jpg",0)
        img2 = img.copy()
        
        # TODO: break this out into json file and load/loop over the templates and thresholds

        # dark water
        if seeking_bobber:
            template = cv.imread('Templates/test_bobber.jpg',0)
            bobber_found = seeker.FindBobber(img2, template, threshold)
            if bobber_found:
                print("We got it!")
                seeking_bobber = False
        
        # blue water
        if seeking_bobber:
            template = cv.imread('Templates/bobber2.jpg',0)
            bobber_found = seeker.FindBobber(img2, template, 0.50)
            if bobber_found:
                print("We got it!")
                seeking_bobber = False
        
        # above with fish
        if seeking_bobber:
            template = cv.imread('Templates/bobber_above.jpg',0)
            bobber_found = seeker.FindBobber(img2, template, threshold)
            if bobber_found:
                print("We got it!")
                seeking_bobber = False

        # above with fish
        if seeking_bobber:
            template = cv.imread('Templates/bobber_above_fish.jpg',0)
            bobber_found = seeker.FindBobber(img2, template, threshold)
            if bobber_found:
                print("We got it!")
                seeking_bobber = False
        