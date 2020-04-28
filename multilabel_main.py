import time
import numpy as np
import os
from PIL import Image
import torch
import torchvision
from torchvision import transforms, datasets, models


def process(trays, backref=False):

    root = os.path.dirname(__file__)

    dishes = {"BBQ":{"rice":0,"vegetable":0,"meat":0},
    		  "Japan":{"rice":0},
    		  "Teppan":{"rice":0,"vegetable":0,"meat":0},
    		  "TwinDishes":{"rice":0,"vegetable":0,"meat":0},
    		  "White":{"rice":0,"vegetable":0,"meat":0}
    }

    dishesMap = {
        'bbq': "BBQ", 
        'japanese': "Japan",
        'teppanyaki': "Teppan",
        'delicacies': "White", 
        'two_choices': "TwinDishes"
    }

    ds_trans = transforms.Compose([transforms.Scale((224,224)),
                               transforms.CenterCrop(224),
                               transforms.ToTensor()
                               #,normalize
                               ])

    for dish, foodtypes in dishes.items():        
        for foodtype in foodtypes:
            foodtypes[foodtype] = models.resnext101_32x8d(pretrained=True)
            num_ftrs = foodtypes[foodtype].fc.in_features
            foodtypes[foodtype].fc = torch.nn.Linear(num_ftrs, 3)
            foodtypes[foodtype] = foodtypes[foodtype].cuda()
            print(dish+"_"+foodtype+".pth")
            load_path = os.path.join(root, dish+"_"+foodtype+".pth")
            foodtypes[foodtype].load_state_dict(torch.load(load_path))
            foodtypes[foodtype].train(False)
            foodtypes[foodtype].eval()

    for i, tray in enumerate(trays):

        output = {
            "rice_preds": None,
            "vegetable_preds": None,
            "meat_preds": None,            
            "rice_infer_time": 0,
            "vegetable_infer_time": 0,
            "meat_infer_time": 0,            
            "percentage": 0
        }

        before_dish = dishesMap[tray.dish]
        try:
            image_before = Image.open(tray.path)
        except:
            print("ERROR IN MULTILABEL!!!")
            yield (tray, output) if backref else output
            continue 

        image = ds_trans(image_before)
        image = torch.unsqueeze(image, dim=0)
        for foodtype, volume_net in dishes[before_dish].items():            
            time_start = time.time()
            outputs = volume_net(image.cuda())
            _, preds = torch.max(outputs.data, 1)
            output[foodtype + "_infer_time"] = time.time() - time_start
            output[foodtype + "_preds"] = preds

        yield (tray, output) if backref else output 

    '''
    for i, pair in enumerate(pairs):

        output = {
            "before_rice_preds": None,
            "before_vegetable_preds": None,
            "before_meat_preds": None,
            "after_rice_preds": None,
            "after_vegetable_preds": None,
            "after_meat_preds": None,
            "before_rice_infer_time": 0,
            "before_vegetable_infer_time": 0,
            "before_meat_infer_time": 0,
            "after_rice_infer_time": 0,
            "after_vegetable_infer_time": 0,
            "after_meat_infer_time": 0,
            "percentage": 0
        }

        before_dish = dishesMap[pair.before_tray.dish]
        image_before = Image.open(pair.before_tray.path)
        image = ds_trans(image_before)
        image = torch.unsqueeze(image, dim=0)
        for foodtype, volume_net in dishes[before_dish].items():            
            time_start = time.time()
            outputs = volume_net(image.cuda())
            _, preds = torch.max(outputs.data, 1)
            output["before_" + foodtype + "_infer_time"] = time.time() - time_start
            output["before_" + foodtype + "_preds"] = preds

        after_dish = dishesMap[pair.after_tray.dish]
        image_after = Image.open(pair.after_tray.path)
        image = ds_trans(image_after)
        image = torch.unsqueeze(image, dim=0)
        for foodtype, volume_net in dishes[after_dish].items():            
            time_start = time.time()
            outputs = volume_net(image.cuda())
            _, preds = torch.max(outputs.data, 1)
            output["after_" + foodtype + "_infer_time"] = time.time() - time_start
            output["after_" + foodtype + "_preds"] = preds

        output["percentage"] = (i+1)/len(pairs)
        yield (pair, output) if backref else output 
    '''
