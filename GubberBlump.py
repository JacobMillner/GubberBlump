from time import sleep
from BobberSeeker import BobberSeeker
from PIL import ImageGrab
import random
import json
import cv2 as cv

threshold = 0.65
fish_key = '1'

# load our templates from the json file
templateData = {}
with open('TemplateConfig.json') as json_file:
    templateData = json.load(json_file)

while True:
    seeking_bobber = True
    seeker = BobberSeeker()
    
    # sleep before looking
    sleep_time = random.randint(1,4)
    print('Sleep Time: ' + str(sleep_time))
    sleep(sleep_time)

    # take a screenshot
    screenshot = ImageGrab.grab(bbox=(0,0,1920,1080))
    screenshot.save("sreengrab.jpg")
    img = cv.imread("sreengrab.jpg",0)
    img2 = img.copy()
    
    # TODO: break this out into json file and load/loop over the templates and thresholds

    # brown water
    print("brown water")
    if seeking_bobber:
        template = cv.imread('Templates/brown_water.JPG', 0)
        print('template: ')
        print(template)
        bobber_found = seeker.FindBobber(img2, template, threshold)
        if bobber_found:
            print("We got it!")
            seeking_bobber = False

    print("blue water")
    # blue water
    if seeking_bobber:
        template = cv.imread('Templates/blue_water.JPG',0)
        bobber_found = seeker.FindBobber(img2, template, 0.50)
        if bobber_found:
            print("We got it!")
            seeking_bobber = False

    print("above")
    # above
    if seeking_bobber:
        template = cv.imread('Templates/bobber_above.JPG',0)
        bobber_found = seeker.FindBobber(img2, template, threshold)
        if bobber_found:
            print("We got it!")
            seeking_bobber = False

    # above with fish
    print("above with fish")
    if seeking_bobber:
        template = cv.imread('Templates/bobber_above_fish.JPG',0)
        bobber_found = seeker.FindBobber(img2, template, threshold)
        if bobber_found:
            print("We got it!")
            seeking_bobber = False
    sleep(1)