from collections import Counter

import robot
from robotparts import Executor,VisionSensor,PrintCallBack,DelayCallBack
from devicebind import PC_bind
import vision


import asyncio
import concurrent

from functools import partial

from multiprocessing import Process
from pynput import keyboard

def comm_task_on_pc(targets,max_step=100,imgsdir="1080p"):
    #读取模板文件
    targets = vision.read_templates(targets,imgsdir)
    
    ###设置callback###
    #delay_exec - 单步延迟，delay_run - 命令组与命令组之间的延迟
    cb_delay = DelayCallBack("delay",delay_exec=3.0,delay_run=0.0)
    #计数和DEBUG用的callback
    task_couter = Counter()
    cb_print = PrintCallBack("printer",task_couter,False)
    
    #初始化executor，并绑定callback
    executor = Executor(PC_bind,[cb_print,cb_delay])
    
    #识别图像的感应器
    sensor = VisionSensor(vision.caper_pc,vision.matcher_comm,targets)

    #组装机器人
    rb = robot.Robot("rb01",executor,sensor)
    robot.Robot.active(rb) #激活机器人

    #rb.max_step = max_step #防止无限循环，可以不设置

    
    p0 = Process(target=rb.work_forever, args=("bz1",task_couter,100))
    p0.start()
    
    return p0


p_list=[]
def killer():
    print("Kill All...")
    for p in p_list:
        p.terminate()

def press_f12(key):
    if key == keyboard.Key["f12"]:
        killer()
        return False

if __name__ == "__main__":
    #import fire
    p_list.append(comm_task_on_pc(["test01"],10))
    with keyboard.Listener(on_press=press_f12) as listener:
        listener.run()
