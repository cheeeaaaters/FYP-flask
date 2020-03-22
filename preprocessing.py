#!/usr/bin/env python
# coding: utf-8

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import os
import math
import time

def Enquiry(lis1): 
    return(np.array(lis1)) 

root = os.path.dirname(__file__)
rootdir = os.path.join(root, 'result')

def process(trays, back_ref=False):

    output = {
        'paths': [],
        'percentage': 0,
        'time': 0
    }

    total = len(trays)

    for count, tray in enumerate(trays):
        output["paths"].clear()
        output["percentage"] = (count + 1)/total
        start_time = time.time()
        filepath = tray.path
        subdir, filename = os.path.split(tray.path)
        folders = subdir.split("/") #subdir: result/recording_2019_10_30/bbq/cam_bbq-18000-18120
        folder = folders[-3] + '/' + folders[-2] + '/' + folders[-1]  #folder: recording_2019_10_30/bbq/cam_bbq-18000-18120
        try:
            img = cv.imread(filepath)
            #print(filepath)
        except cv.error as e:
            output["paths"].clear()
            output["time"] = time.time()-start_time            
            yield (tray, output) if back_ref else output
            continue
        
        canny = cv.Canny(img, 100, 200)
        minLineLength = 200
        maxLineGap = 10
        lines = cv.HoughLinesP(canny, 1, np.pi / 180, 100, minLineLength, maxLineGap)
        if Enquiry(lines).size>=4:
            #print(Enquiry(lines).size)
            lines1 = lines[:,0,:]
            max_length = 0
            index = 0
            i = 0
            for x1, y1, x2, y2 in lines1:
                length = (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)
                if length > max_length:
                    max_length = length
                    index = i
                i += 1
            
            [x1,y1,x2,y2]=lines1[index]
            #cv.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            #cv.imwrite('result/line/'+filename, img)
            #print(index)
            #print(lines1[index])

            degree = math.atan(abs(y1-y2)/abs(x1-x2))
            angle = degree*180/np.pi
            #print(angle)
            H, W = img.shape[:2]
            rotation_matrix = cv.getRotationMatrix2D((W/2, H/2), -angle, 1)
            img_rotation = cv.warpAffine(img, rotation_matrix, (W, H))
            #directory = 'normalized/' + folder + '/'
            #if not os.path.exists(directory):
            #    os.makedirs(directory)
            #cv.imwrite(directory + filename, img_rotation)
            #inverse black/white pixels
            gray = cv.cvtColor(img_rotation, cv.COLOR_BGR2GRAY)
            _, inv = cv.threshold(gray, 120, 255, cv.THRESH_BINARY_INV)
            #cv.imwrite("result/inverse/" + filename, inv)
        else:
            output["paths"].clear()
            output["time"] = time.time()-start_time            
            yield (tray, output) if back_ref else output
            continue
            #cv.imwrite('result/rotation/'+filename, img)
            #gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            #_, inv = cv.threshold(gray, 120, 255, cv.THRESH_BINARY_INV)
            #cv.imwrite("result/inverse/" + filename, inv)

        fn = filename[:-4]
        directory = 'four_angles/' + folder + '/'
        directory = os.path.join(root, directory)
        print(directory)
        scale = 1.0
        (h, w) = inv.shape[:2]
        # calculate the center of the image
        center = (w / 2, h / 2)
        y = int(2/3*h)
        crop_img = inv[y:h, 0:w]
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        cv.imwrite(directory + fn + '_0.jpg', crop_img)
        output['paths'].append(directory + fn + '_0.jpg')
        
        # 90 degrees
        M = cv.getRotationMatrix2D(center, 90, scale)
        rotated90 = cv.warpAffine(inv, M, (h, w))
        (h_90, w_90) = rotated90.shape[:2]
        y_90 = int(2/3*h_90)
        crop_img_90 = rotated90[y_90:h_90, 0:w_90]
        if not os.path.exists(directory):
            os.makedirs(directory)
        cv.imwrite(directory + fn + '_90.jpg', crop_img_90)
        output['paths'].append(directory + fn + '_90.jpg')

        # 180 degrees
        M = cv.getRotationMatrix2D(center, 180, scale)
        rotated180 = cv.warpAffine(inv, M, (w, h))
        (h_180, w_180) = rotated180.shape[:2]
        y_180 = int(2/3*h_180)
        crop_img_180 = rotated180[y_180:h_180, 0:w_180]
        if not os.path.exists(directory):
            os.makedirs(directory)
        cv.imwrite(directory + fn + '_180.jpg', crop_img_180)
        output['paths'].append(directory + fn + '_180.jpg')

        # 270 degrees
        M = cv.getRotationMatrix2D(center, 270, scale)
        rotated270 = cv.warpAffine(inv, M, (h, w)) 
        (h_270, w_270) = rotated270.shape[:2]
        y_270 = int(2/3*h_270)
        crop_img_270 = rotated270[y_270:h_270, 0:w_270]
        if not os.path.exists(directory):
            os.makedirs(directory)
        cv.imwrite(directory + fn + '_270.jpg', crop_img_270)
        output['paths'].append(directory + fn + '_270.jpg')
        output['time'] = time.time() - start_time      
        yield (tray, output) if back_ref else output
