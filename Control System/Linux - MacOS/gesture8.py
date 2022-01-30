import pyautogui
import time
import threading

def close(elTraductor):
    with pyautogui.hold('alt'):
        pyautogui.press('f4')
    elTraductor.awake()
