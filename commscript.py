import os
import random
import time
import ConfigParser
from pymouse import PyMouse

from GameScreen import GameScreen
from basev import *

CFG_FILENAME="bot.conf"
_version="""
Vsersion=2.0
Update=2018.8.22
"""
class Robot:

    def __init__(self,brachlist,commlist,stucklist):
        print "Init Bot..."
        print _version
        print "Reading Config of botsetting..."
        
        cleancfg(CFG_FILENAME)
        config = ConfigParser.RawConfigParser()
        config.read([CFG_FILENAME])
        self.BIMGDIR=config.get('botsetting','BIMGDIR')
        self.DefaultTH=float(config.get('botsetting','DefaultTH'))

        self.bdict=readimgs(brachlist,self.BIMGDIR)
        self.commdict=readimgs(commlist,self.BIMGDIR)
        self.bstuckdict=readimgs(stucklist,self.BIMGDIR)

        self.bwin="bwin2"
        self.bstart="btz"
        self.botdelay=1
        
        #self.st_all = dict(self.bdict.items()+self.commdict.items())
        self.m = PyMouse()
        self.screen = GameScreen()

        self.multiplayer = False
        self.strict = False

        self.starttime=time.time()
        self.lasttime=time.time()
         
        print "Bot initial done!!!"
        

    def beforefunc(self):
        nprint("---->No status Found! Call beforefunc!\n")
    
    def afterfunc(self,st,sltime):
        print "\n======================"
        self.lasttime=time.time()
        print "Time For this Loop: ",int(self.lasttime-sltime)
        print "Avg time per Loop: ",int(self.lasttime-self.starttime)/st
        print "Total time: ",int(self.lasttime-self.starttime),"For Loop Count: ",st
        #put statics and others here
        print "======================\n"

    def mainbot(self,t):
        if t == 0:
            t = 1000
        st=0
        cnt=0
        while t-st>0:
            sltime=time.time()
            cnt+=1
            prgbar="**** Looping Count ({}/{}): {}% ***\r".format(cnt,st,st*100.0/t*1.0)
            pprint(prgbar)

            delay(self.botdelay)
            ss=self.screen.gstatus(self.commdict,threshold=self.DefaultTH,
                strict=self.strict,
                mp=self.multiplayer)
            
            if len(ss)==0:
                nprint("---->Checking stuck!\t\n")
                ss=self.screen.gstatus(self.bstuckdict,threshold=self.DefaultTH,
                    strict=self.strict,
                    mp=self.multiplayer)
                if len(ss)==0:
                    self.beforefunc()
                    continue

            for s,w,h,pt in ss:
                if s.startswith("b"):
                    bclick(self.m,w,h,pt)
            
               
                if s == self.bstart:                    
                    st+=1
                    self.afterfunc(st,sltime)
        #end while            
        print "---->Quite script as MAX hit!"
                       
               

