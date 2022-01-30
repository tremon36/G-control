import pyautogui
import time

def playpause(elTraductor):
    time.sleep(0.3)
    pyautogui.press('space')
    elTraductor.awake()
