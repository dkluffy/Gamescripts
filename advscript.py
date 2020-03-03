import os
import random
import time

from pymouse import PyMouse


from commscript import Robot
from basev import *

import ConfigParser

STUCKLIST=["bxz", "bfail1","cancelm"]
_CFG_FILENAME="bot.conf"
###########################################################################
def yhcomm(t,confname='yhconf'):
    print "Reading config :::  {} ...".format(confname)
    cleancfg(_CFG_FILENAME)
    config = ConfigParser.RawConfigParser()
    config.read([_CFG_FILENAME])
    blist = []
    comlist=config.get(confname,'comlist').split()
    _STUCKLIST=config.get(confname,'STUCKLIST').split()

    print "comlist,stucklist: ",comlist,_STUCKLIST
    
    rb = Robot(blist,comlist,_STUCKLIST)
    rb.multiplayer = (int(config.get(confname,'multiplayer'))>0)
    rb.bstart = comlist[0]
    rb.mainbot(t)

def yhsolo(t):
    blist = []
    comlist= ["btz","bwin2"]
    rb = Robot(blist,comlist,STUCKLIST)
    #rb.strict=True
    rb.mainbot(t)

def story(t):
    blist=[]
    comlist=["bst1","bst2","bst3","bst4","bst5","bzb","btscomm","bwin2"]
    rb = Robot(blist,comlist,STUCKLIST)
    ##==============================
    rb.multiplayer = True
    rb.mainbot(t)
    
def tsimg(t):
    print "Reading config of yhconf..."
    cleancfg(_CFG_FILENAME)
    config = ConfigParser.RawConfigParser()
    config.read([_CFG_FILENAME])
    blist = []
    comlist=config.get('yhconf','comlist').split()
    _STUCKLIST=config.get('yhconf','STUCKLIST').split()

    print "comlist,stucklist: ",comlist,_STUCKLIST

    class Tsimg(Robot):
        def mainbot(self,t):
            img_rgb = self.screen.GrabGameImage()
            showimgs([img_rgb])

    rb = Tsimg(blist,comlist,_STUCKLIST)
    rb.multiplayer = (int(config.get('yhconf','multiplayer'))>0)
    rb.bstart = "bwin2"
    rb.mainbot(t)




###########################################################################
def jwardg(t):
    class Jwd(Robot):
        def beforefunc(self):
            nprint("---->Try to Refresh")
            ss=self.screen.gstatus(self.bdict,threshold=self.DefaultTH,
                strict=self.strict,
                mp=self.multiplayer)
            #pdb.set_trace()
            try:
                s,w,h,pt=ss[0]
                x,y=pt
                self.m.move(int(x),int(y))
                self.m.scroll(-10,None,None)
                
                nprint("Scroll~!")
            except:
                pass
            

            
    blist =  ["jjs","jjf"]
    comlist= ["bjjk","bwin2","bzb","bqd","bjg"]

    rb=Jwd(blist,comlist,STUCKLIST)
    rb.bstart="bwin2"
    rb.DefaultTH=0.6
    rb.strict=True
    #pdb.set_trace()
    rb.mainbot(t)


