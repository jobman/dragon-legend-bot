import cv2
import time
import numpy as np
import pyscreenshot as ImageGrab
import pyautogui


def find_patt(image, patt, thres):
    img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (patt_H, patt_W) = patt.shape[:2]
    res = cv2.matchTemplate(img_grey, patt, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # loc_y, loc_x = int(np.mean(loc[0])),int(np.mean(loc[1]))
    print(min_val, max_val, min_loc, max_loc)
    top_left = min_loc
    bottom_right = (top_left[0] + patt_W, top_left[1] + patt_H)
    cv2.rectangle(image, top_left, bottom_right, 255, 2)
    cv2.imshow('patt', image)
    # return patt_H, patt_W, loc_y, loc_x


screenshot = ImageGrab.grab()
img = np.array(screenshot.getdata(), dtype='uint8').reshape((screenshot.size[1], screenshot.size[0], 3))
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
patt = cv2.imread('resources/battle_ready.JPG', 0)
# cv2.imshow('patt',img)
# h, w, points = find_patt(img, patt, 0.60)
find_patt(img, patt, 0.60)
cv2.waitKey(0)

start_time = time.time()
print("--- %s seconds ---" % (time.time() - start_time))

pyautogui.moveTo(800, 400, 0.2, pyautogui.easeOutQuad)
