import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pdb
import sys
import os
from pykeyboard import PyKeyboard
from pymouse import PyMouse
m = PyMouse()

from PIL import ImageGrab as ig
kb=PyKeyboard()
kb.press_key(kb.print_screen_key)
img_rgb = ig.grabclipboard()
#img_rgb = ig.grab()
print "image size:",img_rgb.width,img_rgb.height
print m.screen_size()

img_rgb = np.array(img_rgb)
#img_rgb = cv.imread('1.png')


img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
template = cv.imread(sys.argv[1],0)
w, h = template.shape[::-1]


methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

#res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)

threshold = 0.8

res = cv.matchTemplate(img_gray,template,eval(methods[1]))	
loc = np.where( res >= threshold)


#pdb.set_trace()
zpoints = zip(*loc[::-1])
m2p=zpoints[0]
mx=int(m2p[0]+w/2)
my=int(m2p[1]+h/2)
#nmx,nmy = p2m(mx,my)


m.click(mx,my,1,2)
cv.circle(img_rgb,(mx,my),w/4,(0,0,255), 2)


#pdb.set_trace()
for pt in zpoints:
	cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
	#cv.circle(img_rgb,(pt[0]+w/2,pt[1]+h/2),w/4,(0,0,255),-1)
#cv.imwrite(methods[1]+'.png',img_rgb)
plt.imshow(img_rgb)
plt.show()

