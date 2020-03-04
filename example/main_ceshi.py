from collections import Counter

import robot
from robotparts import Executor,VisionSensor,PrintCallBack,DelayCallBack
from devicebind import PC_bind
import vision


import asyncio
import concurrent

from functools import partial

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

    #rb.work_forever("bz1",task_couter,100) #开始工作
    print(rb.__class__.active_robots.keys(),rb.__class__)
    return rb,task_couter

async def async_main():
    rb,task_couter = comm_task_on_pc(["test01"],10)
    print(rb.__class__.active_robots.keys(),rb.__class__)
    robot.Robot.active(rb)
    print(rb.__class__.active_robots.keys(),rb.__class__)
    #rb.work_forever("bz1",task_couter,100)
    worker = partial(rb.work_forever,count_point="bz1",counter=task_couter,max_step=100)

    loop = asyncio.get_running_loop()
    #with concurrent.futures.ProcessPoolExecutor() as pool:
    with concurrent.futures.ThreadPoolExecutor() as pool:
        #await loop.run_in_executor(pool, rb.work_forever,"bz1",task_couter,100)
        await loop.run_in_executor(pool, worker)
    print("Running!!!!!!!!!!!!!!!!!!")

# def main2():
#     rb,task_couter = comm_task_on_pc(["test01"],10)
#     print(rb.__class__.active_robots.keys(),rb.__class__)
#     robot.Robot.active(rb)
#     print(rb.__class__.active_robots.keys(),rb.__class__)
#     #rb.work_forever("bz1",task_couter,100)
#     worker = partial(rb.work_forever,count_point="bz1",counter=task_couter,max_step=100)

#     loop = asyncio.get_running_loop()
#     with concurrent.futures.ProcessPoolExecutor() as pool:
#         #await loop.run_in_executor(pool, rb.work_forever,"bz1",task_couter,100)
#         await loop.run_in_executor(pool, worker)
#     print("Running!!!!!!!!!!!!!!!!!!")

if __name__ == "__main__":
    #import fire
    #comm_task_on_pc(["test01"],10)
    asyncio.run(async_main())