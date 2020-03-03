# -*- coding: UTF-8 -*-
import re
import cv2 as cv
import numpy as np
import random
import glob
import os
from time import sleep
import time
import pdb
from PIL import ImageGrab as ig
from matplotlib import pyplot as plt
from pykeyboard import PyKeyboard
from ctypes import windll
import sys

#import win32clipboard
import win32gui as w32

isDebug = True

import cStringIO, functools
def MuteStdout(retCache=False):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			savedStdout = sys.stdout
			if retCache:
				sys.stdout = cStringIO.StringIO()
			try:
				ret=func(*args, **kwargs)
			finally:
				sys.stdout = savedStdout
			return ret
		return wrapper
	return decorator

@MuteStdout(isDebug)
def pprint(s):
    sys.stdout.write(s)
    sys.stdout.flush()

@MuteStdout(not isDebug)
def nprint(s,*args):
    print s,args

def cleancfg(fname):
    content = open(fname).read()  
    #Window下用记事本打开配置文件并修改保存后，编码为UNICODE或UTF-8的文件的文件头  
    #会被相应的加上\xff\xfe（\xff\xfe）或\xef\xbb\xbf，然后再传递给ConfigParser解析的时候会出错  
    #，因此解析之前，先替换掉  
    content = re.sub(r"\xfe\xff","", content)  
    content = re.sub(r"\xff\xfe","", content)  
    content = re.sub(r"\xef\xbb\xbf","", content)  
    open(fname, 'w').write(content)

def grabscreen(i=0):
    if i>10: return None
    img_rgb=ig.grabclipboard()
    if not img_rgb is None:
        """
        Must run as admin
        """
        windll.user32.OpenClipboard()
        windll.user32.EmptyClipboard()
        windll.user32.CloseClipboard()
        #print "---->Clipboard Cleaned!"

    kb=PyKeyboard()
    kb.press_key(kb.print_screen_key)
    sleep(1)
    img_rgb=ig.grabclipboard()
    if img_rgb == None:
        print "---->grab error!",i
        i+=1
        grabscreen(i)
    return img_rgb


def uniqpts(w,h,pts):
    pass

@MuteStdout(not isDebug)
def verify_point(pt,window_info):
    w,h,lt,rb = window_info
    l,t = lt
    r,b = rb
    
    print "verify point ..."
    x,y=pt
    if (x>l and x<r) and (y>t and y<b):
        return (x,y)
    return []
    
def showimgs(imgs=[]):
    for i in imgs:
        plt.imshow(i)
        plt.show()
            
def paint(w,h,pts,screen):
    img_rgb=screen.GrabGameImage()
    
    for pt in pts:
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    showimgs([img_rgb])

def readimgs(blist,imgsdir):
    imdict={}
    for b in blist:
        imdir=os.path.join(imgsdir,b+".png")
        print "Reading image:",imdir
        im=cv.imread(imdir,0)
        imdict[b]=im
    return imdict



def delay(s=1,mini=0):
    t=random.random()*s+mini
    sleep(t)

def bclick(mouse,w,h,pt):
    mx,my = pt
    if w*h == 0:
        w=10
        h=10

    mx=int(mx+w*random.random())
    my=int(my+h*random.random())

    mouse.click(mx,my,1,1)
    print "\n*click: ",(mx,my)
    delay(1)

    #move mouse random
    rx,ry=mouse.screen_size()
    rx=int(random.random()*rx)
    ry=int(random.random()*ry)
    mouse.move(rx,ry)


methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

def matchGray(img_gray,template,threshold=0.8):
    pts=[]
    # w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)	
    loc = np.where( res >= threshold)

    pts=zip(*loc[::-1])

    return pts

