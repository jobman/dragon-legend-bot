import cv2
import time
import numpy as np
import pyscreenshot as ImageGrab
import pyautogui
import math
import random

POS_BLUE_SWORD = (411, 399)
POS_MIDDL_ATTACK = (473, 419)
POS_HIGH_ATTACK = (455, 370)
POS_LOW_ATTACK = (449, 466)
POS_EXIT = (489, 421)
POS_BUTTON_HUNT = (662, 135)
POS_BUTTON_ATTACK = (328, 225)
POS_BUTTON_REFRESH = (72, 59)

# ENEMYS
mad_dog = ('resources/mad_dog.JPG', (48, 48, 91, 255, 255, 255))
crats_leader = ('resources/crats_leader.JPG', (48, 48, 91, 255, 255, 255))
fire_spider = ('resources/fire_spider.JPG', (48, 48, 91, 255, 255, 255))
shalnoy_pes = ('resources/shalnoy_pes.JPG', (60, 60, 255, 255, 255, 255))


def in_delta_epsilon(point1, point2, delta_epsilon):
    delta = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    if delta < delta_epsilon:
        return True
    else:
        return False


def make_screenshot():
    screenshot = ImageGrab.grab()
    img = np.array(screenshot.getdata(), dtype='uint8').reshape((screenshot.size[1], screenshot.size[0], 3))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img


def find_blue_sword():
    img = make_screenshot()

    patt = cv2.imread('resources/battle_ready.JPG', 0)
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_grey_croped = img_grey[300:300 +300, 300:300 + 300]
    cv2.imshow('croped', img_grey_croped)
    res = cv2.matchTemplate(img_grey_croped, patt, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    points = [pt for pt in zip(*loc[::-1]) if pt[1] > 300]
    for _ in zip(*loc[::-1]):
        print('Find :)')
        return True

    else:
        print('Not find :(')
        return False

    cv2.imshow('patt', img)
    # return patt_H, patt_W, loc_y, loc_x


def find_enemy(enemy):
    pattern_img, color = enemy
    # screen = cv2.imread('resources/test_hunt.JPG', 0)
    img = make_screenshot()
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Бешеный пес
    h_min_val, h_max_val, s_min_val, s_max_val, v_min_val, v_max_val = color
    lower = np.array([h_min_val, s_min_val, v_min_val])
    upper = np.array([h_max_val, s_max_val, v_max_val])

    mask = cv2.inRange(imgHSV, lower, upper)
    # cv2.imshow('mask', mask)
    result = cv2.bitwise_and(img, img, mask=mask)

    # cv2.imshow('res', result)

    img_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(pattern_img, 0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    points = [pt for pt in zip(*loc[::-1]) if pt[1] > 300]
    for pt in zip(*loc[::-1]):
        cv2.rectangle(result, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    corrected_points = []
    for pt in points:
        corrected_points.append((pt[0] + w // 2, pt[1] - 20))

    return corrected_points


def click_to(point, delta=random.randint(2, 10)):
    delta = delta - delta // 2
    pyautogui.moveTo(point[0] + delta, point[1] + delta, 0.2, pyautogui.easeOutQuad)
    pyautogui.click()


# find_blue_sword()

def action_controller():
    # tactic_actions = [POS_HIGH_ATTACK, POS_MIDDL_ATTACK, POS_LOW_ATTACK]
    tactic_actions = [POS_LOW_ATTACK, POS_LOW_ATTACK, POS_LOW_ATTACK]
    while True:
        rand = random.randint(0, len(tactic_actions) - 1)
        action = tactic_actions.pop(rand)
        yield action
        tactic_actions.append(action)


def game_cycle():
    enemy_not_find_times = 0
    while True:
        click_to(POS_BUTTON_HUNT)
        time.sleep(3)
        enemies = find_enemy(shalnoy_pes)
        if enemies:
            enemy_not_find_times = 0
            enemy = random.choice(enemies)
            click_to(enemy)
            time.sleep(1)
            click_to(POS_BUTTON_ATTACK)
            time.sleep(10)
            not_find_times = 0
            controller = action_controller()
            start_time = time.time()
            while True:
                if find_blue_sword():
                    print("--- %s seconds ---" % (time.time() - start_time))
                    not_find_times = 0
                    click_to(next(controller))
                    time.sleep(9)
                else:
                    print("--- %s seconds ---" % (time.time() - start_time))
                    not_find_times += 1
                if not_find_times > 3:
                    break
                start_time = time.time()
        else:
            enemy_not_find_times += 1

        if enemy_not_find_times > 5:
            click_to(POS_BUTTON_REFRESH)
            enemy_not_find_times = 0
            time.sleep(5)


game_cycle()
