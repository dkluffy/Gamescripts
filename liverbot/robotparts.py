from time import sleep
from collections import namedtuple,Counter
import random

from liverbot.devicebind import sda_map,CMD

class ExecutorCallBack(object):
    """
    用于实现，统计，延迟,通信等功能
    """
    def __init__(self,name):
        self.name = name

    def on_execute_begin(self,cmd):
        pass
    
    def on_execute_end(self,cmd):
        pass

    def on_run_begin(self,**kwargs):
        pass

    def on_run_end(self,**kwargs):
        pass

class Executor(object):
    """
    执行方法
    """
    def __init__(self,devicebind,callbacks=None):
        self.callbacks = []
        if callbacks:
            self.callbacks = callbacks
        self.devicebind = devicebind

    def _run_callback(self,method,cmd):
        for cb in self.callbacks:
            cb.__getattribute__(method)(cmd)
        
    def exec_cmd(self,cmd):
        #默认的执行方法
        self._run_callback("on_execute_begin",cmd)
        self.devicebind[cmd.device][cmd.action](cmd.code)
        self._run_callback("on_execute_end",cmd)

    def run(self,cmds):
        for cmd in cmds:
            try:
                self.exec_cmd(cmd)
            except Exception as e:
                print(e,"failed to exec cmd:",cmd)
                continue
        return 0

    def __call__(self,cmds):
        return self.run(cmds)

class PrintCallBack(ExecutorCallBack):
    """
    实现计数,打印
    """
    def __init__(self,name,counter,verbose=True):
        self.counter = counter
        self.counter["total"] = 0
        self.verbose = verbose
        
    def on_execute_begin(self,cmd):
        if self.verbose:
            print("...Runing CMD: ",cmd)
    
    def on_execute_end(self,cmd):
        self.counter[cmd.device]+=1
        self.counter[cmd.status]+=1
        self.counter["total"]+=1

        if self.verbose:
            print("...Totoal executed: ",self.counter["total"])
    
class DelayCallBack(ExecutorCallBack):
    """
    延迟功能
    """
    def __init__(self,name,delay_exec=1.0,delay_run=0.0):
        self.name = name
        self.delay_exec = delay_exec
        self.delay_run = delay_run

    def on_execute_end(self,cmd):
        sleep(self.delay_exec+random.random())

    def on_run_end(self,**kwargs):
        sleep(self.delay_run)


class VisionSensor(object):
    """
    通过caper抓取图片给matcher
    matcher匹配后返回　坐标和状态
    """
    def __init__(self,caper,matcher,targets):
        self.caper = caper
        self.matcher = matcher
        self.targets = targets

    def run(self):
        """
        return: 坐标和状态
        """
        #TODO(10):限定抓取范围
        input_img = self.caper()
        return self.matcher(input_img,self.targets)
               
    def __call__(self):
        return self.run()