# Photo Show
# 1007: basic photo show from NAS is tested OK
import os
import sys
import time
import numpy as np
import cv2 as cv
from itertools import cycle

# SCREEN RES 1366 x 768
COLS_SCR = 1366
ROWS_SCR =  768
# DISPLAY TIME in ms
DISP_TMS = 500

# for test
# ffpath = "/home/zhao/Pictures/Show/"

# NAS mout on /mnt/nas
ffpath = '/mnt/nas/Photo_2020'

# -----------------------------------------------
# function 1, show the image
def imageShow(img_bkg, fname) :

    if not(fname.endswith(('jpg','png','jpeg','bmp','JPG','PNG','JPEG','BMP'))) :
        print('None-image: ',fname)
        return

    print(fname)
    img_src = cv.imread(fname)
    img_new = imgResize(img_bkg, img_src)   # resize the photo
    
    cv.namedWindow('img',cv.WINDOW_NORMAL)
    cv.setWindowProperty('img', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    cv.imshow('img',img_new)  

    key = cv.waitKey(DISP_TMS)
    keyExit(key)
# -----------------------------------------------

# -----------------------------------------------
# function 2, Resize the photo
def imgResize(img_bkgrd, img_photo):

    # 根据小图像的大小，在大图像上创建感兴趣区域roi（放置位置任意取）
    row0, col0 = img_bkgrd.shape[:2] # 获取bkgrd的高度、宽度
    row1, col1 = img_photo.shape[:2] # 获取photo的高度、宽度

    print(' photo.shape ',img_photo.shape)

    ratio_bkg = row0 / col0
    ratio_src = row1 / col1
#    print('ratio_bkg ',ratio_bkg)
#    print('ratio_src ',ratio_src)

    ratio_resize = row0 / row1
    if ratio_src > ratio_bkg :
        if   row1 > row0 :
            ratio_resize = row0 / row1
        elif col1 > col0 :
            ratio_resize = col0 / col1
        else :
            ratio_resize = row0 / row1
    else :
        if   row1 > row0 :
            ratio_resize = col0 / col1
        elif col1 > col0 :
            ratio_resize = row0 / row1
        else :
            ratio_resize = col0 / col1

    img_resize = cv.resize(img_photo,(0,0),fx= ratio_resize, fy= ratio_resize) #resize

            
    print('resize.shape ',img_resize.shape)
        
    row1, col1 = img_resize.shape[:2]          # 获取photo的高度、宽度
    roi = img_bkgrd[0:row1, 0:col1]

    dst = cv.addWeighted(img_resize,1,roi,0,0) # 图像融合
    add_img = img_bkgrd.copy()                 # 对原图像进行拷贝

    row_off = int((row0-row1)/2)        # central offset
    col_off = int((col0-col1)/2)        # central offset
    add_img[row_off:row1+row_off, col_off:col1+col_off] = dst   # 融合后的区域放进原图

    return add_img
# -----------------------------------------------

# -----------------------------------------------
# function 3, exit when press ESC
def keyExit(key) :
    if key & 0xFF == 27 :
        cv.destroyAllWindows()
        sys.exit()
# -----------------------------------------------

# -----------------------------------------------
# main function, walk the path and load image show

# make a black backgroud image
bkg = np.zeros((ROWS_SCR, COLS_SCR, 3), np.uint8)
bkg.fill(0x00)   # black

#print('bkgrd.shape ', bkg.shape)

paths = os.walk(ffpath)
for path, dir_lst, file_lst in paths:
    for file_name in file_lst:
        imageShow(bkg, os.path.join(path, file_name))
            
cv.destroyAllWindows()            
# -----------------------------------------------
