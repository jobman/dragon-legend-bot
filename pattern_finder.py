import cv2
import numpy as np
import pyscreenshot as ImageGrab


def make_screenshot():
    screenshot = ImageGrab.grab()
    img = np.array(screenshot.getdata(), dtype='uint8').reshape((screenshot.size[1], screenshot.size[0], 3))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img


h_min_val, h_max_val, s_min_val, s_max_val, v_min_val, v_max_val = 0, 179, 0, 255, 0, 255


def refresh():
    lower = np.array([h_min_val, s_min_val, v_min_val])
    upper = np.array([h_max_val, s_max_val, v_max_val])

    mask = cv2.inRange(imgHSV, lower, upper)
    cv2.imshow('mask', mask)
    result = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow('res', result)


def h_min(value):
    global h_min_val
    h_min_val = value
    print('hue min = ', value)
    refresh()


def h_max(value):
    global h_max_val
    h_max_val = value
    print('h_max', value)
    refresh()


def s_min(value):
    global s_min_val
    s_min_val = value
    print('s_min', value)
    refresh()


def s_max(value):
    global s_max_val
    s_max_val = value
    print('s_max', value)
    refresh()


def v_min(value):
    global v_min_val
    v_min_val = value
    print('v_min', value)
    refresh()


def v_max(value):
    global v_max_val
    v_max_val = value
    print('v_max', value)
    refresh()


cv2.namedWindow('trackBars')
cv2.resizeWindow('trackBars', 640, 240)
cv2.createTrackbar('hue min', 'trackBars', 0, 179, h_min)
cv2.createTrackbar('hue max', 'trackBars', 179, 179, h_max)
cv2.createTrackbar('sat min', 'trackBars', 0, 255, s_min)
cv2.createTrackbar('sat max', 'trackBars', 255, 255, s_max)
cv2.createTrackbar('val min', 'trackBars', 0, 255, v_min)
cv2.createTrackbar('val max', 'trackBars', 255, 255, v_max)

img = make_screenshot()
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

refresh()
cv2.waitKey(0)
