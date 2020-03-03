import pyautogui as pag
from collections import namedtuple,Counter
import random

"""
https://asyncfor.com/posts/doc-pyautogui.html
screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()
pyautogui.moveTo(100, 150)
pyautogui.click()
#  鼠标向下移动10像素
pyautogui.moveRel(None, 10)
pyautogui.doubleClick()
#  用缓动/渐变函数让鼠标2秒后移动到(500,500)位置
#  use tweening/easing function to move mouse over 2 seconds.
pyautogui.moveTo(1800, 500, duration=2, tween=pyautogui.easeInOutQuad)
#  在每次输入之间暂停0.25秒
pyautogui.typewrite('Hello world!', interval=0.25)
pyautogui.press('esc')
pyautogui.keyDown('shift')
pyautogui.press(['left', 'left', 'left', 'left', 'left', 'left'])
pyautogui.keyUp('shift')
pyautogui.hotkey('ctrl', 'c')
"""

#("mouse","click",(10,100)) ,("mouse","move",(10,100)),("key","press","a")
#status 默认为 None
CMD = namedtuple("CMD",["device","action","code","status"],defaults=[None])

#status_device_action_map
sda_map = {"bc":["mouse","click"],
               "kd":["keyboard","keyDown"],
                "None":["mouse","move"]}
#status:target name
pag.FAILSAFE = False
PC_bind = {
    "mouse":{"move":pag.moveTo,"click":pag.click},
    "keyboard":{}
}

Andriod_bind = {}