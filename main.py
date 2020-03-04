from collections import Counter

from liverbot import robot
from liverbot.robotparts import Executor,VisionSensor,PrintCallBack,DelayCallBack
from liverbot.devicebind import PC_bind
from liverbot import vision


import asyncio
import concurrent

from functools import partial

from multiprocessing import Process
#from multiprocessing import freeze_support
from pynput import keyboard

p_list=[] #用于存储进程

def comm_task_on_pc(targets,max_step=100,count_point="bc_tz",imgsdir="yys1080p"):
    #读取模板文件
    targets = targets.split()
    targets = vision.read_templates(targets,imgsdir)
    
    ###设置callback###
    #delay_exec - 单步延迟，delay_run - 命令组与命令组之间的延迟
    cb_delay = DelayCallBack("delay",delay_exec=3.0,delay_run=0.0)
    #计数和DEBUG用的callback
    task_couter = Counter()
    cb_print = PrintCallBack("printer",task_couter,False)
    #为了计数准确，初始化task_couter
    for k in targets.keys():
        task_couter[k]=0
    
    #初始化executor，并绑定callback
    executor = Executor(PC_bind,[cb_print,cb_delay])
    
    #识别图像的感应器
    sensor = VisionSensor(vision.caper_pc,vision.matcher_comm,targets)

    #组装机器人
    rb = robot.Robot("rb01",executor,sensor)
    robot.Robot.active(rb) #激活机器人

    #rb.max_step = max_step #防止无限循环，可以不设置    
    p0 = Process(target=rb.work_forever, args=(count_point,task_couter,max_step))
    p0.start()
    p_list.append(p0)

    #不能有返回值，否则和fire以及Listener冲突，导致热键无效

def killer():
    print("Kill All...")
    for p in p_list:
        p.terminate()

def press_f12(key):
    if key == keyboard.Key["f12"]:
        killer()
        return False

if __name__ == "__main__":
    import fire
    #freeze_support()
    fire.Fire(comm_task_on_pc)
    with keyboard.Listener(on_press=press_f12) as listener:
        listener.run()

