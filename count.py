import os
import cv2 as cv
from collections import Counter

root = os.path.dirname(__file__)
rootdir = os.path.join(root, 'OCR_text')

def process():
    f_count = 0
    for subdir, dirs, files in os.walk(rootdir):
        for filename in files:
            f_count += 1
    
    j = 0
    for subdir, dirs, files in os.walk(rootdir):
        for filename in files:
            j += 1
            output = {
                'regex': None,
                'ocr': None,
                'object_id': None,
                'percentage': j/(f_count+0.0001)
            }            

            path_parts = os.path.normpath(subdir).split(os.path.sep)
            vid = path_parts[-1]
            area = path_parts[-2]
            date = path_parts[-3]
            regex = date + '/' + area + '/' + vid
            output["regex"] = regex
            fn_rm_ext = filename.split('.')[0]
            obj_id = fn_rm_ext.split('-')[1]
            output["object_id"] = obj_id

            filepath = os.path.join(subdir, filename) #filepath: OCR_text/recording_2019_10_30/bbq/cam_bbq-00000-00120/whole-1.txt
            folders = subdir.split("/")
            dates = folders[len(folders)-3] # recording_2019_10_30
            date_parts = dates.split('_')
            year = date_parts[1]
            month = date_parts[2]
            day = date_parts[3]
            Date = year + '-' + month + '-' + day
            position = folders[len(folders)-2]
            folder = folders[len(folders)-3] + '/' + folders[len(folders)-2] + '/' + folders[len(folders)-1] #folder: cam_bbq-00000-00120
            print(folder)
            parts = folder.split("-")
            i = parts[len(parts)-1]
            minutes = int(i)/60
            hours = int(minutes)//60
            rmd = int(minutes%60)
            if rmd < 30:
                hour = 7 + hours
                minute = 30 + rmd
            else:
                hour = 8 + hours
                minute = (30 + rmd)%60
            time = str(hour) + ':' + str(minute)
            
            id_list = []
            name_list = []

            with open(filepath) as fp:
                line = fp.readline()
                while line:
                    # recording_2019_10_30/bbq/cam_bbq-8000-18120/73-500_0.jpg:text
                    line_parts = line.split(":")
                    first = line_parts[0]
                    second = line_parts[1]
                    id_list.append(second)
                    first_parts = first.split("/")
                    fn = first_parts[3]
                    name_list.append(fn)
                    line = fp.readline()

            result_name_list = []
            most_common,num_most_common = Counter(id_list).most_common(1)[0] # 4, 6 times
            print(most_common)
            output["ocr"] = most_common 
            yield output
            '''
            if int(most_common)>1000:
                continue
            cnt = 0
            for ids in id_list:
                if ids == most_common:
                    temp = name_list[cnt].split("_")
                    name = temp[0] + '.jpg'
                    result_name_list.append(name)
                cnt += 1
            result_name_list = list(set(result_name_list))
            #folder: cam_bbq-00000-00120
            new_folder = 'result_images/' + Date + '_' + position + '_' + time + '_' + most_common + '/'
            directory = 'result/' + folder + '/'
            for files in os.listdir(directory):
                if files in result_name_list:
                    img = cv.imread(directory + files)
                    if not os.path.exists(new_folder):
                        os.makedirs(new_folder)
                    cv.imwrite(new_folder + files, img)
            print(most_common, num_most_common)
            print(result_name_list)
            print(time)
            '''