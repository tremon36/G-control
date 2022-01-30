import math
import time
import pynput
from pynput.keyboard import Key, Controller


def run(elTraductor):
    keyboard = Controller()
    i = 0
    while checkCondition(elTraductor.data) and i < 100:
        keyboard.press(Key.right)
        if i > 1:
            print("pressed")
        i = i + 1
        time.sleep(0.2)
    keyboard.release(Key.right)
    elTraductor.awake()


def checkCondition(lastFramePositions):
    result = calculateDistance((lastFramePositions[0][420],lastFramePositions[0][421]), (lastFramePositions[0][426],lastFramePositions[0][427])) / calculateDistance((lastFramePositions[0][420],lastFramePositions[0][421]),(0,0))
    return result < 4 #from testing




def calculateDistance(a, b):
    result = math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2))
    return result
