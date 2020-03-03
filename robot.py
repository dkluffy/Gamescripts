from collections import Counter
from devicebind import CMD,sda_map
import random
from tqdm import tqdm


class Robot:
    """
    负责:
        通过sensor 获取 coords,status
        按照coords,status 通过bind生成CMD list
        通过executor 执行 获取的 cmd list
    """

    active_robots = {}
    dummy_cmds = [CMD("mouse","move",(0,0))]

    def __init__(self,name,executor,sensor=None,sda=sda_map):
        """
        每个机器人实例必须有一个executor，可以没有sensor
        executor可以共享，比如同一台机器，只有一套输入设备
        如果没有 sensor，由外部sensor更新cmd_queue,供 executor执行
        如果有 sensor，则忽略cmd_queue,只执行自己的sensor获得的cmd

        这样可以实现，分布式机器人:),比如向多台机器发送一样的命令
        """

        self.name = name
        self.sda = sda
        self.cmd_queue = [] #多线程/进程情况下，数组安全么？

        self.max_step = 99999 #最大命令组数，不管是否有效，都算一组
        self.quiet = False
        
        self.sensor = sensor
        self.executor = executor
        self.couters = {}

        #TODO:如果接收到的coords不在domain_area中，拒绝执行
        #因为getWindowsRectByName有BUG存在，暂时不做
        self.domain_area = None
    
    @classmethod
    def active(cls,robot):
        #激活子机器人
        cls.active_robots[robot.name] = robot

    @classmethod
    def deactive(cls,name):
        #停止子机器人
        cls.active_robots.pop(name,None)

    @staticmethod
    def gen_dummy_cmds():
        #TODO:按屏幕大小生成
        x = random.randint(10,100)
        return [CMD("mouse","move",(x,x+10))]

    def bind_status(self,coords,status):
        """
        TODO:读取rule生成CMD
        目前直接读取sda来生成
        """
        cmds = []
        if len(coords) != len(status):
            return cmds
        for c,s in zip(coords,status):
            if s is None:
                sda = self.sda["None"]
            else:
                sda = self.sda[s[:2]]
            cmd = CMD(sda[0],sda[1],c,s)
            cmds.append(cmd)
        return cmds

    def shutdown(self):
        #关闭自己
        self.__class__.active_robots.pop(self.name,None)

    def co_worker(self):
        while len(self.cmd_queue)>0:
            cmd = self.cmd_queue.pop(0)
            self.executor([cmd])
        self.executor(self.__class__.dummy_cmds)
        
    def solo_worker(self):

        coords,status = self.sensor()
        cmds = self.bind_status(coords,status)

        if len(cmds)==0 or cmds is None:
            self.executor(self.gen_dummy_cmds())
        else:
            self.executor(cmds)

    def work_forever(self,count_point=None,counter=None,max_step=-1):
        """要么不设置任何参数，要么三个参数全部设置"""
     
        worker = self.solo_worker
        if self.sensor is None:
            worker = self.co_worker
        
        if count_point is None:
            print("Warning: didn't set `max_step` and counter.")
            max_step = self.max_step
            print("Fallback to use `self.max_step`",max_step)

        if not self.quiet:
            for _ in tqdm(range(max_step),desc=self.name,ascii=True):
                # 这个特性限制了并发，应该禁用
                # 只能在ThreadPoolExecutor下使用并发，多线程并发不行
                # active_rb = self.__class__.active_robots.keys()
                # if not self.name in active_rb:
                #     print("Dead:shutdown from outside!!")
                #     break
                if count_point and counter[count_point]>max_step:
                    print("Dead:Max step reached!!!")
                    break
                worker()






        
