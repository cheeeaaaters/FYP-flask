# coding=utf-8
import os
import shutil
import sys
import time

'''
Part below for recognizer
'''
################################
import pytesseract
################################

import cv2
import numpy as np
import tensorflow as tf

OCR_path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(1, OCR_path)
sys.path.append(os.getcwd())
from nets import model_train as model
from utils.rpn_msr.proposal_layer import proposal_layer
from utils.text_connector.detectors import TextDetector

root = os.path.dirname(OCR_path)

tf.app.flags.DEFINE_string('test_data_path', os.path.join(root, 'four_angles'), '')
tf.app.flags.DEFINE_string('output_path', os.path.join(root,'OCR_result'), '')
tf.app.flags.DEFINE_string('gpu', '0', '')
tf.app.flags.DEFINE_string('checkpoint_path', os.path.join(OCR_path,'checkpoints_mlt'), '')
FLAGS = tf.app.flags.FLAGS


def get_images():
    files = []
    exts = ['jpg', 'png', 'jpeg', 'JPG']
    for parent, dirnames, filenames in os.walk(FLAGS.test_data_path):
        for filename in filenames:
            for ext in exts:
                if filename.endswith(ext):
                    files.append(os.path.join(parent, filename))
                    break
    print('Find {} images'.format(len(files)))
    return files


def resize_image(img):
    img_size = img.shape
    im_size_min = np.min(img_size[0:2])
    im_size_max = np.max(img_size[0:2])

    im_scale = float(600) / float(im_size_min)
    if np.round(im_scale * im_size_max) > 1200:
        im_scale = float(1200) / float(im_size_max)
    new_h = int(img_size[0] * im_scale)
    new_w = int(img_size[1] * im_scale)

    new_h = new_h if new_h // 16 == 0 else (new_h // 16 + 1) * 16
    new_w = new_w if new_w // 16 == 0 else (new_w // 16 + 1) * 16

    re_im = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    return re_im, (new_h / img_size[0], new_w / img_size[1])


def process():

    output = {
        'path': None,
        'percentage': 0,
        'locate_time': 0,
        'ocr_time': 0,
        'ocr_text': [],
        'err': False
    }

    if os.path.exists(FLAGS.output_path):
        shutil.rmtree(FLAGS.output_path)
    os.makedirs(FLAGS.output_path)
    os.environ['CUDA_VISIBLE_DEVICES'] = FLAGS.gpu
    index = 0
    with tf.get_default_graph().as_default():
        input_image = tf.placeholder(tf.float32, shape=[None, None, None, 3], name='input_image')
        input_im_info = tf.placeholder(tf.float32, shape=[None, 3], name='input_im_info')

        global_step = tf.get_variable('global_step', [], initializer=tf.constant_initializer(0), trainable=False)

        bbox_pred, cls_pred, cls_prob = model.model(input_image)

        variable_averages = tf.train.ExponentialMovingAverage(0.997, global_step)
        saver = tf.train.Saver(variable_averages.variables_to_restore())

        with tf.Session(config=tf.ConfigProto(allow_soft_placement=True)) as sess:
            ckpt_state = tf.train.get_checkpoint_state(FLAGS.checkpoint_path)
            model_path = os.path.join(FLAGS.checkpoint_path, os.path.basename(ckpt_state.model_checkpoint_path))
            print('Restore from {}'.format(model_path))
            saver.restore(sess, model_path)
            #file_whole = open('data/res/text/whole.txt','w')
            im_fn_list = get_images()
            start_all = time.time()
            
            for count, im_fn in enumerate(im_fn_list):
                output["err"] = False
                output["path"] = im_fn
                output["ocr_text"].clear()
                output["percentage"] = count / len(im_fn_list)
                print('===============')
                print(im_fn) #im_fn: ../four_angles/recording_2019_10_30/bbq/cam_delicacies-17760-17880/73-500_0.jpg
                start = time.time()
                try:
                    im = cv2.imread(im_fn)[:, :, ::-1]
                except:
                    print("Error reading image {}!".format(im_fn))
                    output["err"] = True
                    yield output
                    continue

                img, (rh, rw) = resize_image(im)
                h, w, c = img.shape
                im_info = np.array([h, w, c]).reshape([1, 3])
                bbox_pred_val, cls_prob_val = sess.run([bbox_pred, cls_prob],
                                                       feed_dict={input_image: [img],
                                                                  input_im_info: im_info})

                textsegs, _ = proposal_layer(cls_prob_val, bbox_pred_val, im_info)
                scores = textsegs[:, 0]
                textsegs = textsegs[:, 1:5]

                textdetector = TextDetector(DETECT_MODE='H')
                # DETECT_MODE can be H / O depending on context
                boxes = textdetector.detect(textsegs, scores[:, np.newaxis], img.shape[:2])
                boxes = np.array(boxes, dtype=np.int)

                cost_time = (time.time() - start)
                output["locate_time"] = cost_time
                print("cost time: {:.2f}s".format(cost_time))
                '''
                Do the text recognition
                '''

                text_start = time.time()
                grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
                ########################################################
                for i, box in enumerate(boxes):
                    cv2.polylines(img, [box[:8].astype(np.int32).reshape((-1, 1, 2))], True, color=(0, 255, 0),
                                  thickness=2)
                    ###################################################
                    # First get the number id
                    startX = box[0]
                    startY = box[1]
                    endX = box[4]
                    endY = box[5]
                    ret,thresh = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
                    roi = thresh[startY:endY, startX:endX]
                    
                    ###################################################
                    # Single out the digit


                    ###################################################



                    # in order to apply Tesseract v4 to OCR text we must supply
                    # (1) a language, (2) an OEM flag of 4, indicating that the we
                    # wish to use the LSTM neural net model for OCR, and finally
                    # (3) an OEM value, in this case, 7 which implies that we are
					# treating the ROI as a single line of text

                    config = ("-l digits --oem 1 --psm 7")
					# config = ("--oem 0 -c tessedit_char_whitelist=0123456789")
                    text = pytesseract.image_to_string(roi, config=config)
                    output["ocr_text"].append(text)
                    # add the bounding box coordinates and OCR'd text to the list
                    # of results
                    # Only print if number is detected

                    #im_fn: ../four_angles/recording_2019_10_30/bbq/cam_delicacies-17760-17880/73-500_0.jpg
                    if text.isdigit():
                        print(text)
                        if len(text)==4:
                            data = im_fn.split("/")
                            fn = data[len(data)-1]  # 73-500_0.jpg
                            folder = data[len(data)-4] + '/' + data[len(data)-3] + '/' + data[len(data)-2] # recording_2019_10_30/bbq/cam_bbq-8000-18120
                            print(folder + '/' + fn)
                            fn_data = fn.split("-")
                            id_num = fn_data[0] #73
                            image_name = fn_data[1] #500_0.jpg
                            
                            directory = 'OCR_text/' + folder + '/'
                            directory = os.path.join(root, directory)
                            if not os.path.exists(directory):
                                os.makedirs(directory)
                            file_whole = open(directory + 'whole-' + id_num + '.txt','a')
                            file_whole.write(folder + '/' + fn + ':' + text+'\n')
                            file_whole.close()
                            #cv2.imwrite(str(index) + '.png', roi)
                            index += 1
	   					# results.append(((startX, startY, endX, endY), text))
                output["ocr_time"] = time.time() - text_start

                ########################################################
                '''
                img = cv2.resize(img, None, None, fx=1.0 / rh, fy=1.0 / rw, interpolation=cv2.INTER_LINEAR)
                cv2.imwrite(os.path.join(FLAGS.output_path, os.path.basename(im_fn)), img[:, :, ::-1])

                with open(os.path.join(FLAGS.output_path, os.path.splitext(os.path.basename(im_fn))[0]) + ".txt",
                          "w") as f:
                    for i, box in enumerate(boxes):
                        line = ",".join(str(box[k]) for k in range(8))
                        line += "," + str(scores[i]) + "\r\n"
                        f.writelines(line)
                '''
                yield output
            cost_time_all = (time.time() - start_all)
            print("Total cost time: {:.2f}s".format(cost_time_all))
            #file_whole.close()

if __name__ == '__main__':
    tf.app.run()
