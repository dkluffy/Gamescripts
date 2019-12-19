import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pdb
import sys
import os

from pymouse import PyMouse
m = PyMouse()

from PIL import ImageGrab as ig
#ig.grabclipboard()
#img_rgb = ig.grabclipboard()
img_rgb = ig.grab()
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

threshold = 0.5

res = cv.matchTemplate(img_gray,template,eval(methods[1]))	
loc = np.where( res >= threshold)



zpoints = zip(*loc[::-1])

zpoints.sort()
x0,y1=zpoints[0]
zpoints.sort(key=lambda x:x[1])
x1,y0=zpoints[0]


print x0,y1
print x1,y0


#for pt in zpoints:
	#cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
	#cv.circle(img_rgb,(pt[0]+w/2,pt[1]+h/2),w/4,(0,0,255),-1)
	
#cv.imwrite(methods[1]+'.png',img_rgb)

cv.rectangle(img_rgb, (x0,y1), (x0 + w, y1 + h), (0,0,255), 1)
cv.rectangle(img_rgb, (x1,y0), (x1 + w, y0 + h), (0,0,255), 1)
cv.circle(img_rgb,(x0,y1),w/8,(0,0,255),1)
cv.circle(img_rgb,(x1,y0),w/8,(0,0,255),1)
cv.circle(img_rgb,(x0,y0),w/8,(0,0,255),1)
plt.imshow(img_rgb)
plt.show()

