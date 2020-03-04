import pytest
import vision
import os

import cv2 as cv

test_imgdir = "I:\\Code_Public\\try_yolov3\\images"

bc_tz_gray = cv.imread(os.path.join(test_imgdir,"yys0008.jpg"),0)
bc_tz = cv.imread(os.path.join(test_imgdir,"yys0006.jpg"),0)

imdir = "yys1080p"

targets = ["bc_tz2","bc_zb","bc_win1","bc_win2","testicon01"]

@pytest.fixture()
def test_read():
    imdict = vision.read_templates(targets,imdir)
    print(imdict.keys())
    assert type(imdict) is dict
    assert len(imdict.keys()) == len(targets)
    return imdict


# def test_match_gray(test_read):
#     #img = vision.caper_pc()
#     img = cv.imread("I:\\Code_Public\\Gamescripts\\1080p\\test\\test01.jpg",0)
#     pts = vision.match_gray(img,test_read["testicon01"],0.8)
#     pts = [x for x in pts ]
#     print(test_read.keys(),"////shape:",test_read["bc_tz2"].shape,img.shape)
#     print("pts---",list(pts)[:10],len(list(pts)))
#     assert len(list(pts)) > 1
#     assert 0

# def test_match_gray(test_read):
#     #img = vision.caper_pc()
#     img = cv.imread("I:\\Code_Public\\Gamescripts\\1080p\\test\\test01.jpg",0)
#     loc = vision.match_gray(img,test_read["testicon01"],0.8)
#     print("////",loc[:10])
#     print("////shape:",loc.shape)
#     assert 0

def test_match_comm(test_read):
    import numpy as np
    img = cv.imread("I:\\Code_Public\\Gamescripts\\yys1080p\\test\\test01.jpg",0)
    co,st = vision.matcher_comm(img,test_read)
    print(co,st)

    vision.ON_DEBUG =True
    co1,st1 = vision.matcher_comm(img,test_read)
    print(co1,st1)

    assert "testicon01" in st
    assert len(co) == len(st)
    assert np.sum(co1-co)<0

    



    
    
    


