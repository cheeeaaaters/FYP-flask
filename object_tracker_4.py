from models import *
from utils import *

import os, sys, time, datetime, random
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torch.autograd import Variable

from PIL import Image
import cv2
from sort import *

import time
import eventlet

path_to_darknet = '/home/ubuntu/darknet'
sys.path.insert(1, path_to_darknet)
import darknet

root = os.path.dirname(__file__)

# load weights and set defaults
#config_path='/home/ubuntu/prune_12000/prune.cfg'
config_path=os.path.join(root, 'config/prune.cfg')
#weights_path='/home/ubuntu/prune_12000/prune_last.weights'
weights_path=os.path.join(root, 'config/prune_last.weights')
#config_path='config/yolov3-voc.cfg'
#weights_path='config/yolov3-voc_20000.weights'
class_path=os.path.join(root, 'config/voc.names')
img_size=416
conf_thres=0.3
nms_thres=0.3
#conf_thres=0.8
#nms_thres=0.4

test_title = 'ra darknet pruned'

classes = utils.load_classes(class_path)
Tensor = torch.cuda.FloatTensor

total_dets = 0

def convert(detections, vh, vw):
    global total_dets
    #detections: 
    #list of (class, confidence, objectness, (bounding_box_x_px, bounding_box_y_px, bounding_box_width_px, bounding_box_height_px))
    if len(detections)>0:
        res = torch.empty((len(detections), 7))
        for i,detection in enumerate(detections):        
            (label, conf, obj, (x, y, w, h)) = detection
            ratio_w = vw/img_size
            ratio_h = vh/img_size
            x1,x2,y1,y2 = x-w/2,x+w/2,y-h/2,y+h/2
            res[i] = torch.tensor([x1*ratio_w, y1*ratio_h, x2*ratio_w, y2*ratio_h, obj, conf, label])  
            total_dets += 1
        return res              
    return []

def detect_image(img, vh, vw):

    # run inference on the model and get detections
    detections = darknet.performDetect_2(img, conf_thres, nms_thres, config_path, weights_path)
    detection = convert(detections, vh, vw)

    return detection
    #tensor([[x1, y1, x2, y2, obj_conf, class_conf, class_pred]])
    #max object confidence
#videopath = 'data/videos/cam_one-09000-09120.mov'
#folderpath = 'data/videos/'

def process(videos, back_ref=False):
    count = 0    
    output = {
        'path': None,
        'obj_id': 0,
        'count': count,
        'percentage': 0,
        'infer_time': 0,
    }
    
    for video in videos:
        frames = 0
        subdir, filename = os.path.split(video.path)
        outputpath = os.path.join(root ,'data/output/', filename)
        vid = cv2.VideoCapture(video.path)
        vidCopy = cv2.VideoCapture(video.path)
        total_num_frames = 0
        while(True):
            ret, f = vidCopy.read()
            if not ret:
                break
            else:
                total_num_frames += 1
        total_num_frames -= 1
        #total_num_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
        mot_tracker = Sort(max_age=3,min_hits=0) 

        ret,frame=vid.read()
            
        vw = frame.shape[1]
        vh = frame.shape[0]
        print ("Video size", vw,vh)
                
        pre_unique_labels = []
        flag = False
        while(True):
            eventlet.sleep(0)
            ret, frame = vid.read()
            if not ret:
                break
            frames += 1
            print(frames)
            output["percentage"] = frames/total_num_frames
            output["path"] = None
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            infer_time = time.time()
            detections = detect_image(frame, vh, vw)
            infer_time = (time.time() - infer_time)
            output["infer_time"] = infer_time

            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            if len(detections) > 0:

                unique_labels = detections[:, -1].cpu().unique()
                n_cls_preds = len(unique_labels)

                tracked_objects = mot_tracker.update(detections.cpu())
                if unique_labels.data[0]==0: 
                    for x1, y1, x2, y2, obj_id, cls_pred in tracked_objects:
                        output["obj_id"] = obj_id
                        cls = classes[int(cls_pred)]
                        crop_img = frame[int(y1):int(y2), int(x1):int(x2)]
                        parts = subdir.split('/')
                        new_folder = parts[-2] + '/' + parts[-1] + '/'
                        directory = 'result/' + new_folder + filename[:-4] + '/'
                        directory = os.path.join(root, directory)
                        if cls == "w/ food":
                            if not os.path.exists(directory):
                                os.makedirs(directory)					
                            f_name =  str(int(obj_id)) + '-' + str(count)
                            try:
                                write_path = directory + f_name + '.jpg'
                                cv2.imwrite(write_path, crop_img)
                                count += 1
                                output["path"] = write_path
                                output["count"] = count
                                print("==================================================" , count, frames, total_num_frames)
                            except:
                                print("Exception in object tracker")

            if back_ref:
                yield (video, output)
            else:
                yield output
                            

'''
import cv2
from sort import *
colors=[(255,0,0),(0,255,0),(0,0,255),(255,0,255),(128,0,0),(0,128,0),(0,0,128),(128,0,128),(128,128,0),(0,128,128)]

rootdir = 'data/videos'
count = 0
frames = 0
starttime = time.time()
total_infer_time = 0

for subdir, dirs, files in os.walk(rootdir):
    for filename in files:
        print(filename) #cfilename: am_bbq-24960-25080.mov
        print (subdir) #subdir: data/videos/recording_2019_10_30/bbq
    
        videopath = os.path.join(subdir, filename)
        outputpath = os.path.join('data/output/', filename)
        vid = cv2.VideoCapture(videopath)
        mot_tracker = Sort(max_age=3,min_hits=0) 

        ##cv2.namedWindow('Stream',cv2.WINDOW_NORMAL)
        ##cv2.resizeWindow('Stream', (800,600))

        ##fourcc = cv2.VideoWriter_fourcc(*'XVID')
        ret,frame=vid.read()
        
        vw = frame.shape[1]
        vh = frame.shape[0]
        print ("Video size", vw,vh)
        ##outvideo = cv2.VideoWriter(outputpath.replace(".mov", "-det.mov"),fourcc,20.0,(vw,vh))
        
        pre_unique_labels = []
        flag = False
        while(True):
            ret, frame = vid.read()
            if not ret:
                break
            frames += 1
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ##pilimg = Image.fromarray(frame)

            infer_time = time.time()
            detections = detect_image(frame, vh, vw)
            total_infer_time += (time.time() - infer_time)

            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            ##img = np.array(pilimg)

            if len(detections) > 0:
		
                #tracked_objects = mot_tracker.update(detections.cpu())
                unique_labels = detections[:, -1].cpu().unique()
                n_cls_preds = len(unique_labels)
                #print(unique_labels)
                #print("Tracker:\n")
                #print(tracked_objects)
                #print("Detector:\n")
                #print(detections.cpu())

                tracked_objects = mot_tracker.update(detections.cpu())
                if unique_labels.data[0]==0: 
                    #print("Tracker number: %d", tracked_objects)
                    for x1, y1, x2, y2, obj_id, cls_pred in tracked_objects:
                        cls = classes[int(cls_pred)]
		            #if cls == "w/o food":
		            #    continue		    
                        #cv2.rectangle(frame, (x1, y1), (x1+box_w, y1+box_h), color, 4)
                        #cv2.rectangle(frame, (x1, y1-35), (x1+len(cls)*19+80, y1), color, -1)
                        crop_img = frame[int(y1):int(y2), int(x1):int(x2)]
                        #filename: cam_bbq-24960-25080.mov
                        #subdir: data/videos/recording_2019_10_30/bbq
                        parts = subdir.split('/')
                        new_folder = parts[-2] + '/' + parts[-1] + '/'
                        directory = 'result/' + new_folder + filename[:-4] + '/'
                        if cls == "w/ food":
                            if not os.path.exists(directory):
                                os.makedirs(directory)					
                            f_name =  str(int(obj_id)) + '-' + str(count)
                            try:
                                cv2.imwrite(directory + f_name + '.jpg', crop_img)
                                count += 1
                            except:
                                pass
                                #print("???????????????????????????????????????????????????????")
                                #print(crop_img)
                                #print(x1, y1, x2, y2)		    

            ##cv2.imshow('Stream', frame)
            ##outvideo.write(frame)

totaltime = time.time()-starttime
print(frames, "frames", totaltime/frames, "s/frame", count, "total cropped images")
print(total_infer_time/frames, "average inference time")
print(total_dets, "total detections")

fo = open("test_result.txt", "a")
fo.write("\n\n"+test_title + "\n")
fo.write("totaltime: %f\n" % totaltime)
fo.write("frames: %d\n" % frames)
fo.write("fps: %f\n" % (frames/totaltime))
fo.write("total cropped images: %d\n" % count)
fo.write("average inference time: %f\n" % (total_infer_time/frames))
fo.write("total detections: %d\n" % total_dets)
fo.close()

##cv2.destroyAllWindows()
##outvideo.release()

'''
#[[1.1593e+02, 2.8065e+02, 1.8692e+02, 3.2196e+02, 3.0290e-01, 9.9992e-01, 1.0000e+00]]