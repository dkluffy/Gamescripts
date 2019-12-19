import os
import random
import time

from pymouse import PyMouse

from botv import *
from commscript import *
import ConfigParser

STUCKLIST=["bxz", "bfail1","cancelm"]
_CFG_FILENAME="bot.conf"
###########################################################################
def yhcomm(t):
    print "Reading config of yhconf..."
    cleancfg(_CFG_FILENAME)
    config = ConfigParser.RawConfigParser()
    config.read([_CFG_FILENAME])
    blist = []
    comlist=config.get('yhconf','comlist').split()
    _STUCKLIST=config.get('yhconf','STUCKLIST').split()
    multiplayer = (int(config.get('yhconf','multiplayer'))>0)
    print "comlist,stucklist: ",comlist,_STUCKLIST
    print "Multiplayer:",multiplayer

    rb = Robot(blist,comlist,_STUCKLIST)
    rb.cc = not multiplayer
    rb.bstart = "bwin2"
    rb.mainbot(t)

def yhsolo(t):
    blist = []
    comlist= ["btz","bwin2"]
    rb = Robot(blist,comlist,STUCKLIST)
    rb.mainbot(t)

def story(t):
    blist=[]
    comlist=["bst1","bst2","bst3","bst4","bst5","bzb","btscomm","bwin2"]
    rb = Robot(blist,comlist,STUCKLIST)
    rb.mainbot(t)

###########################################################################
def tssolo(t):
    blist=["btsbox"]
    comlist=["btsboss","btscomm","bts","bwin2","bts_c8","tsstandby",]
    
    class TsRobot(Robot):
        dt=1
        dtmax=10
        dtcount=0
        def beforefunc(self):
            f=chkk("btsboss",self.commdict,self.m,self.screen)
            if not f:
                f=chkk("btscomm",self.commdict,self.m,self.screen)
            
            #box
            f=chkk("btsbox",self.bdict,self.m,self.screen)
            while f:
                f=chkk("btsbox",self.bdict,self.m,self.screen)
            
            #walking
            img_rgb = self.screen.GrabGameImage()
            bflag,w,h,pts = findimg(self.commdict["tsstandby"],img_rgb)
            if bflag:         
                x0=0
                y0=0
                try:
                    x0,y0=pts[0]
                    if self.dt>0:
                        mx=int(x0-w*random.random())
                        my=int(y0-h*random.random())
                        self.m.click(mx,my,1,1)
                        print "-----> walking!"
                        self.dtcount += 1
                        if self.dtcount>self.dtmax:
                            self.dtcount=0
                            self.dt=-1*self.dt

                    if self.dt<0:
                        mx=int(x0-w*random.random()-1.5*w)
                        my=int(y0-h*random.random())
                        self.m.click(mx,my,1,1)
                        print "walking!<-----"
                        self.dtcount+=1
                        if self.dtcount>self.dtmax:
                            self.dtcount=0
                            self.dt=-1*self.dt
                except Exception as e:
                    print e


    rb = TsRobot(blist,comlist,STUCKLIST)
    rb.bstart = "tsstandby"
    rb.mainbot(t)

###########################################################################
def jwardb(t,pljj=False):
    jwarda(t,pljj)

def jwarda(t,pljj = True):
    blist =  ["bsx","bqd","jjk","jjs","jjf","bjg"]
    comlist= ["jjt","bwin2","bzb"]

    
    class Jwd(Robot):
        def refresh(self,pt=None,wc=0,fc=0,pcount=0):
            if pljj:
                if wc>=3 or fc>5 or pcount<3:
                    chkk("bsx",self.bdict,self.m,self.screen)
                    waitchkk("bqd",self.bdict,self.m,self.screen)
            else:
                if pcount < 1:
                    x = int(pt[0])
                    y = int(pt[1])
                    self.m.move(x,y)
                    self.m.scroll(-10,None,None)
            print "---->Refresh wc,fc,pcount:",wc,fc,pcount

        def checkwf(self):
            wincount=0
            failcount=0
            try:
                img_rgb = self.screen.GrabGameImage()
                wf,ww,wh,wpts = findimg(self.bdict["jjs"],img_rgb)
                wincount =len(wpts)

                ff,fw,fh,fpts = findimg(self.bdict["jjf"],img_rgb,0.9)
                failcount =len(fpts)
            except:
                pass

            return wincount,failcount

        def beforefunc(self):
            
            wc,fc = self.checkwf()
            
            img_rgb = self.screen.GrabGameImage()
            f,w,h,pts = findimg(self.bdict["jjk"],img_rgb,0.5)
            pcount = len(pts)
            pt=pts[0]
            
            self.refresh(pt,wc,fc)

            pt=pts[random.randint(0,pcount-1)]
            print "---->Jward:pcount,wc,fc: ",pcount,wc,fc    
            mx,my = Getpoint(w,h,[pt],0.5)
            self.m.click(mx,my,1,1)
            
            waitchkk("bjg",self.bdict,self.m,self.screen,0.8,5,5)
            
            
            

        def afterfunc_no(self):
            interval=150
            nowtime=time.time()
            elstime=nowtime - self.starttime
            if elstime<interval:
                print "Sleeping....................",interval-elstime
                time.sleep(interval-elstime)
                self.starttime=time.time()
            
          
    rb=Jwd(blist,comlist,STUCKLIST)
    rb.bstart="jjt"
    #pdb.set_trace()
    rb.mainbot(t)
