import pyautogui
import time
import cv2
import numpy as np
import pyscreenshot as ImageGrab

# screen = cv2.imread('resources/test_hunt.JPG', 0)
patt = cv2.imread('resources/mad_dog.JPG', 0)
screenshot = ImageGrab.grab()
img = np.array(screenshot.getdata(), dtype='uint8').reshape((screenshot.size[1], screenshot.size[0], 3))
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Бешеный пес
h_min_val, h_max_val, s_min_val, s_max_val, v_min_val, v_max_val = 48, 48, 91, 255, 255, 255
lower = np.array([h_min_val, s_min_val, v_min_val])
upper = np.array([h_max_val, s_max_val, v_max_val])

mask = cv2.inRange(imgHSV, lower, upper)
cv2.imshow('mask', mask)
result = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow('res', result)

img_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
template = cv2.imread('resources/mad_dog.JPG', 0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where(res >= threshold)
points = [pt for pt in zip(*loc[::-1]) if pt[1] > 300]
for pt in zip(*loc[::-1]):
    cv2.rectangle(result, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

cv2.imshow('RES RECT', result)
cv2.waitKey(0)
