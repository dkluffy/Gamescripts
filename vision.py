import numpy as np
import pyautogui as pag
import cv2 as cv
import os


ON_DEBUG = False

# methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
#             'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
T_Method = cv.TM_CCOEFF_NORMED
T_Thredshold = 0.8
T_Filter = True

Validate_IMG_EXT = ["png","jpeg","jpg"]

def caper_pc():
    """
    return: 图片数组 shape(h,w,c)
    """
    img = pag.screenshot()
    return np.array(img)[...,0]

def read_templates(status_names,imgsdir):
    """
    只返回有对应图片的status
    """
    imdict={}
    images = os.listdir(imgsdir)

    #过滤图片名
    val_images = []
    for im in images:
        sn = im.split(".")
        if sn[0] in status_names and (sn[-1].lower() in Validate_IMG_EXT):
            val_images.append(im)
    
    #检查
    sn_new = [im.split(".")[0] for im in val_images]
    if len(sn_new) != len(status_names):
        print("Warning: some status, don't have valide image")
    
    #读取
    for sn in val_images:
        imdir = os.path.join(imgsdir,sn)   
        print("Reading image:",imdir)
        im_rgb=cv.imread(imdir,0)
        imdict[sn.split(".")[0]]=im_rgb

    return imdict

# def calc_iou(h,w,pt1,pt2):
#     box1_x1,box1_y1 = pt1
#     box1_x2,box1_y2 = box1_x1+w,box1_y1+h

#     box2_x1,box2_y1 = pt2
#     box2_x2,box2_y2 = box2_x1+w,box2_y1+h

#     xi1 = max(box1_x2,box2_x2)
#     yi1 = max(box1_y2,box2_y2)
#     xi2 = min(box1_x1,box2_x1)
#     yi2 = min(box1_y1,box2_y1)

#     inter_width = (box1_x2-box1_x1+box2_x2-box2_x1)-(xi1-xi2)
#     inter_height = (box1_y2-box1_y1+box2_y2-box2_y1)-(yi1-yi2)
#     inter_area = max(inter_width,0)*max(inter_height,0)

#     box1_area = (box1_y2-box1_y1)*(box1_x2-box1_x1)
#     box2_area = (box2_y2-box2_y1)*(box2_x2-box2_x1)
#     union_area = box1_area+box2_area-inter_area

#     # compute the IoU
#     iou = inter_area/union_area
    
#     return iou

# def filter_non_max(func):
#     def filter(*args):
#         h,w,pts = func(*args)
#         #迭代计算IOU代价有点大
#         return h,w,pts[:1]
#     return filter

def filter_simple(func):
    #TODO(11):先用这个简单的代替,实现划分区域后TODO(10)，一样可以加速多开
    def filter(*args):
        pts = func(*args)
        return pts[:1]
    return filter
                
@filter_simple
def match_gray(img_gray,template,threshold=T_Thredshold,method=T_Method):
    #TODO(12):这个匹配算法，受大小变化影响很大，可以用SIFT改进，不要想用深度卷积网络了，代价太大
    #https://docs.opencv.org/master/dc/dc3/tutorial_py_matcher.html
    #https://www.pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
    pts=[]
    #h,w = template.shape
    res = cv.matchTemplate(img_gray,template,method)	
    loc = np.where( res >= threshold)

    pts=zip(*loc[::-1])

    return list(pts)


def shift_coords(func):
    def shifter(*args):
        co,st = func(*args)
        # if ON_DEBUG:
        #     return co,st
        co = np.array(co)
        co_dalt = np.random.randint(0,20,co.shape)
        co = co + co_dalt
        return co,st
    return shifter

#@shift_coords
def matcher_comm(input_img,targets):
    coords = []
    status = []
    for t in targets.keys():
        pts = match_gray(input_img,targets[t])
        if len(pts)>0:
            coords+=pts
            status+=([t]*len(pts))
    return coords,status