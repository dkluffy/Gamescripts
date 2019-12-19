# -*- coding: UTF-8 -*-
import glob
import os
import pdb
import random
import re
import time
from ctypes import windll
from time import sleep
import ConfigParser

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from PIL import ImageGrab as ig
from pykeyboard import PyKeyboard

#import win32clipboard
import win32gui as w32
from basev import *


__version__="3.0"
_CFG_FILENAME="bot.conf"

DefaultTH=0.8


class GameScreen:
    def __init__(self):
        print "Reading config of Screen..."
        cleancfg(_CFG_FILENAME)
        config = ConfigParser.RawConfigParser()
        config.read([_CFG_FILENAME])

        self.BIGSCREEN=bool(int(config.get('screen','BIGSCREEN'))>=1)

        self.MainScreenX=int(config.get('screen','MainScreenX'))
        self.MainScreenY=int(config.get('screen','MainScreenY'))

        self.LScreenX=int(config.get('screen','LScreenX'))
        self.LScreenY=int(config.get('screen','LScreenY'))

        self.MouseScreenX=int(config.get('screen','MouseScreenX'))
        self.MouseScreenY=int(config.get('screen','MouseScreenY'))

       
        self.GAMENAME=u"阴阳师-网易游戏" 
        self.multiplayer=(int(config.get('screen','multiplayer'))>0)
        
        print "Screen Initial Done!!!!"
        print "BIGSCREEN:",self.BIGSCREEN
        print "GameName(Hardcode):",self.GAMENAME.encode("GB18030")
        print "Mutil-player:",self.multiplayer
        

    def GetGameWindow(self):
        hwnd=w32.FindWindow(None,self.GAMENAME)
        l,t,r,b = (0,0,0,0)
        l,t,r,b = w32.GetWindowRect(hwnd)
        w=r-l
        h=b-t
        return w,h,(l,t),(r,b)

    def cropImg(self,im):
        im=np.array(im)
        im=im[:self.MainScreenY,self.LScreenX:]

        r=self.MouseScreenX*1.0/im.shape[1]
        dim=(self.MouseScreenX,int(im.shape[0]*r))

        im=cv.resize(im, dim, interpolation = cv.INTER_AREA)

        return im

    def GrabGameImage(self):
        im=None    
        if self.BIGSCREEN == True:
            im = grabscreen()
            try:
                im = self.cropImg(im)
            except Exception as e:
                print e
                im = np.array(ig.grab())
        else:
            im = np.array(ig.grab())
        return im
    
    
    def gstatus(self,imgdict,threshold=DefaultTH,
        strict=False,
        mp=False):
        
        ss=[]
        
        ww,wh,wlt,wrb = (0,0,0,0)

        if strict:
            ww,wh,wlt,wrb =  self.GetGameWindow()

        img_rgb = self.GrabGameImage()
        img_gray = cv.cvtColor(img_rgb,cv.COLOR_BGR2GRAY)

        for k in imgdict:
            w, h = imgdict[k].shape[::-1]
            try:
                nprint("*Checking status: ",k)
                
                pt = matchGray(img_gray,imgdict[k])[0]

                if strict:
                    pt=verify_point(pt,(ww,wh,wlt,wrb))

                nprint("*Found status: ",k)
                
                ss+=[(k,w,h,pt)]
                if not mp:
                    break
            except Exception as e:
                #print "---->Get Game stuatus Error:\n",e
                continue

        return ss


