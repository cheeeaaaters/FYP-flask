import argparse
import scipy
import os
import numpy as np
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from scipy import ndimage
from tqdm import tqdm
from math import ceil
from glob import glob
from PIL import Image
import dataloaders
import models
from utils.helpers import colorize_mask
from utils import palette
import time
import cv2

def pad_image(img, target_size):
    rows_to_pad = max(target_size[0] - img.shape[2], 0)
    cols_to_pad = max(target_size[1] - img.shape[3], 0)
    padded_img = F.pad(img, (0, cols_to_pad, 0, rows_to_pad), "constant", 0)
    return padded_img

def sliding_predict(model, image, num_classes, flip=True):
    image_size = image.shape
    tile_size = (int(image_size[2]//2.5), int(image_size[3]//2.5))
    overlap = 1/3

    stride = ceil(tile_size[0] * (1 - overlap))
    
    num_rows = int(ceil((image_size[2] - tile_size[0]) / stride) + 1)
    num_cols = int(ceil((image_size[3] - tile_size[1]) / stride) + 1)
    total_predictions = np.zeros((num_classes, image_size[2], image_size[3]))
    count_predictions = np.zeros((image_size[2], image_size[3]))
    tile_counter = 0

    for row in range(num_rows):
        for col in range(num_cols):
            x_min, y_min = int(col * stride), int(row * stride)
            x_max = min(x_min + tile_size[1], image_size[3])
            y_max = min(y_min + tile_size[0], image_size[2])

            img = image[:, :, y_min:y_max, x_min:x_max]
            padded_img = pad_image(img, tile_size)
            tile_counter += 1
            padded_prediction = model(padded_img)
            if flip:
                fliped_img = padded_img.flip(-1)
                fliped_predictions = model(padded_img.flip(-1))
                padded_prediction = 0.5 * (fliped_predictions.flip(-1) + padded_prediction)
            predictions = padded_prediction[:, :, :img.shape[2], :img.shape[3]]
            count_predictions[y_min:y_max, x_min:x_max] += 1
            total_predictions[:, y_min:y_max, x_min:x_max] += predictions.data.cpu().numpy().squeeze(0)

    total_predictions /= count_predictions
    return total_predictions


def multi_scale_predict(model, image, scales, num_classes, device, flip=False):
    input_size = (image.size(2), image.size(3))
    upsample = nn.Upsample(size=input_size, mode='bilinear', align_corners=True)
    total_predictions = np.zeros((num_classes, image.size(2), image.size(3)))

    image = image.data.data.cpu().numpy()
    for scale in scales:
        scaled_img = ndimage.zoom(image, (1.0, 1.0, float(scale), float(scale)), order=1, prefilter=False)
        scaled_img = torch.from_numpy(scaled_img).to(device)
        scaled_prediction = upsample(model(scaled_img).cpu())

        if flip:
            fliped_img = scaled_img.flip(-1).to(device)
            fliped_predictions = upsample(model(fliped_img).cpu())
            scaled_prediction = 0.5 * (fliped_predictions.flip(-1) + scaled_prediction)
        total_predictions += scaled_prediction.data.cpu().numpy().squeeze(0)

    total_predictions /= len(scales)
    return total_predictions


def save_images(image, mask, output_path, image_file, palette, original_size, output=None):
	# Saves the image, the model output and the results after the post processing
    zero_pad = 256 * 3 - len(palette)
    for i in range(zero_pad):
        palette.append(0)

    w, h = image.size

    if original_size:
        w, h =original_size

    if output:
        print(mask.shape)
        resize_mask = cv2.resize(mask, dsize=original_size, interpolation=cv2.INTER_NEAREST)
        print(resize_mask.shape)
        pc_0 = int(np.count_nonzero(resize_mask==0))
        pc_1 = int(np.count_nonzero(resize_mask==1))
        pc_2 = int(np.count_nonzero(resize_mask==2))
        pc_3 = int(np.count_nonzero(resize_mask==3))
        pc_total = pc_0 + pc_1 + pc_2 + pc_3
        output["pc_0"] = pc_0
        output["pc_1"] = pc_1
        output["pc_2"] = pc_2
        output["pc_3"] = pc_3
        output["pc_total"] = pc_total

    image_file = os.path.basename(image_file).split('.')[0]
    colorized_mask = colorize_mask(mask, palette)

    if image.size != original_size:
        image = image.resize(size=original_size, resample=Image.BILINEAR)
    if colorized_mask.size != original_size:
        colorized_mask = colorized_mask.resize(size=original_size, resample=Image.NEAREST)

    blend = Image.blend(image, colorized_mask.convert('RGB'), 0.5)

    mask_path = os.path.join(output_path, image_file+'.png')
    
    colorized_mask.save(mask_path)
    output_im = Image.new('RGB', (w*3, h))
    output_im.paste(image, (0,0))
    output_im.paste(colorized_mask, (w*1,0))
    output_im.paste(blend, (w*2,0))
    blend_path = os.path.join(output_path, image_file+'_colorized.png')
    output_im.save(blend_path)
    
    if output:
        output['mask'] = mask_path
        output['blend'] = blend_path

    # mask_img = Image.fromarray(mask, 'L')
    # mask_img.save(os.path.join(output_path, image_file+'.png'))



def main():
    args = parse_arguments()
    print(args)
    config = json.load(open(args.config))

    # Dataset used for training the model
    dataset_type = config['train_loader']['type']
    loader = getattr(dataloaders, config['train_loader']['type'])(**config['train_loader']['args'])
    to_tensor = transforms.ToTensor()
    #normalize = transforms.Normalize(loader.MEAN, loader.STD)
    num_classes = loader.dataset.num_classes
    palette = loader.dataset.palette
    base_size = loader.dataset.base_size

    # Model
    model = getattr(models, config['arch']['type'])(num_classes, **config['arch']['args'])
    availble_gpus = list(range(torch.cuda.device_count()))
    device = torch.device('cuda:0' if len(availble_gpus) > 0 else 'cpu')

    checkpoint = torch.load(args.model)
    if isinstance(checkpoint, dict) and 'state_dict' in checkpoint.keys():
        checkpoint = checkpoint['state_dict']
    if 'module' in list(checkpoint.keys())[0] and not isinstance(model, torch.nn.DataParallel):
        model = torch.nn.DataParallel(model)
    model.load_state_dict(checkpoint)
    model.to(device)
    model.eval()
    #test
    if args.half:
        model=model.half()

    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    image_files = sorted(glob(os.path.join(args.images, f'*.{args.extension}')))
    with torch.no_grad():
        tbar = tqdm(image_files, ncols=100)

        Total_Inference_Time=0
        for img_file in tbar:      
            image = Image.open(img_file).convert('RGB')
            original_size=image.size

            if base_size:
                image = image.resize(size=(base_size, base_size), resample=Image.BILINEAR)

            #input = normalize(to_tensor(image)).unsqueeze(0)
            input = to_tensor(image).unsqueeze(0)
            if args.half:
                input = input.half()
            ticks = time.time()
            if args.mode == 'multiscale':
                prediction = multi_scale_predict(model, input, scales, num_classes, device)
            elif args.mode == 'sliding':
                prediction = sliding_predict(model, input, num_classes)
            else:
                prediction = model(input.to(device))
                Total_Inference_Time += time.time()-ticks
                if config['arch']['type'][:2] == 'IC':
                    prediction = prediction[0]
                elif config['arch']['type'][-3:] == 'OCR':
                    prediction = prediction[0] 
                elif config['arch']['type'][:3] == 'Enc':
                    prediction = prediction[0]
                elif config['arch']['type'][:5] == 'DANet':
                    prediction = prediction[0]

                if args.half:
                    prediction = prediction.squeeze(0).float().cpu().numpy() 
                else:
                    prediction = prediction.squeeze(0).cpu().numpy()  

            prediction = F.softmax(torch.from_numpy(prediction), dim=0).argmax(0).cpu().numpy()
            save_images(image, prediction, args.output, img_file, palette, original_size)

        print("time used: {}".format(Total_Inference_Time))

def process(trays, model='HRNet', backref=False):

    args = {
        "mode": "normal",
        "model_uneaten": "",  
        "model_eaten": "", 
        "config_uneaten": "",
        "config_eaten": "",       
        "half": False,
        "output": "outputs"
    }

    if model == 'HRNet':
        args['model_uneaten'] = ''
        args['model_eaten'] = ''
    elif model == 'BiSeNet':
        args['model_uneaten'] = ''
        args['model_eaten'] = ''

    models = {
        "eaten": None,
        "uneaten": None
    }

    for ue in ['uneaten', 'eaten']:
        config = json.load(open(args["config_" + ue]))
        root = os.path.dirname(__file__)
        # Dataset used for training the model
        dataset_type = config['train_loader']['type']
        loader = getattr(dataloaders, config['train_loader']['type'])(**config['train_loader']['args'])
        to_tensor = transforms.ToTensor()
        #normalize = transforms.Normalize(loader.MEAN, loader.STD)
        num_classes = loader.dataset.num_classes
        palette = loader.dataset.palette
        base_size = loader.dataset.base_size
        # Model
        model = getattr(models, config['arch']['type'])(num_classes, **config['arch']['args'])
        availble_gpus = list(range(torch.cuda.device_count()))
        device = torch.device('cuda:0' if len(availble_gpus) > 0 else 'cpu')
        checkpoint = torch.load(args['model'])
        if isinstance(checkpoint, dict) and 'state_dict' in checkpoint.keys():
            checkpoint = checkpoint['state_dict']
        if 'module' in list(checkpoint.keys())[0] and not isinstance(model, torch.nn.DataParallel):
            model = torch.nn.DataParallel(model)
        model.load_state_dict(checkpoint)
        model.to(device)
        model.eval()
        #test        
        if args['half']:
            model=model.half()
        models[ue] = model

    output_dir = os.path.join(root, 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with torch.no_grad():
        tbar = tqdm(trays, ncols=100)
        Total_Inference_Time=0
        for c, img_file in enumerate(tbar):     
            output = {
                "mask": None,
                "blend": None,
                "percentage": (c+1)/len(trays),
                "infer_time": 0,
                "pc_0": 0,
                "pc_1": 0,
                "pc_2": 0,
                "pc_3": 0,
                "pc_total": 0
            } 

            if img_file.eaten:
                model = models["eaten"]
            else:
                model = models["uneaten"]

            image = Image.open(img_file.path).convert('RGB')
            original_size=image.size

            if base_size:
                image = image.resize(size=(base_size, base_size), resample=Image.BILINEAR)

            #input = normalize(to_tensor(image)).unsqueeze(0)
            input = to_tensor(image).unsqueeze(0)
            if args['half']:
                input = input.half()
            ticks = time.time()
            if args['mode'] == 'multiscale':
                prediction = multi_scale_predict(model, input, scales, num_classes, device)
            elif args['mode'] == 'sliding':
                prediction = sliding_predict(model, input, num_classes)
            else:
                prediction = model(input.to(device))
                output["infer_time"] = time.time()-ticks
                Total_Inference_Time += output["infer_time"]
                if arch_type[:2] == 'IC':
                    prediction = prediction[0]
                elif arch_type[-3:] == 'OCR':
                    prediction = prediction[0] 
                elif arch_type[:3] == 'Enc':
                    prediction = prediction[0]
                elif arch_type[:5] == 'DANet':
                    prediction = prediction[0]

                if args['half']:
                    prediction = prediction.squeeze(0).float().cpu().numpy() 
                else:
                    prediction = prediction.squeeze(0).cpu().numpy()  

            prediction = F.softmax(torch.from_numpy(prediction), dim=0).argmax(0).cpu().numpy()
            
            save_images(image, prediction, output_dir, img_file.path, pal, original_size, output)
           
            yield (img_file, output) if backref else output

        print("time used: {}".format(Total_Inference_Time))

'''
def process(trays, backref=False):

    root = os.path.dirname(__file__)
    train_loader_type = "TM2"
    train_loader_args = {
        "data_dir": "/home/ubuntu/TM2",
        "batch_size": 8,
        "base_size": 512,
        "crop_size": False,
        "augment": True,
        "shuffle": True,
        "scale": False,
        "flip": False,
        "rotate": False,
        "blur": False,
        "split": "train",
        "num_workers": 8
    }
    arch_type = "HRNetV2_OCR"
    arch_args = {
        "backbone": "resnet18",
        "freeze_bn": False,
        "freeze_backbone": False
    }
    args = {
        "mode": "normal",
        "model": "/home/ubuntu/FYP-Seg/weights/checkpoint-epoch250.pth",        
        "half": False,
        "output": "outputs"
    }

    # Dataset used for training the model
    #dataset_type = train_loader_type
    #loader = getattr(dataloaders, train_loader_type)(**train_loader_args)
    to_tensor = transforms.ToTensor()
    #normalize = transforms.Normalize(loader.MEAN, loader.STD)
    num_classes = 4
    pal = palette.COCO_palette
    base_size = train_loader_args["base_size"]

    # Model
    model = getattr(models, arch_type)(num_classes, **arch_args)
    availble_gpus = list(range(torch.cuda.device_count()))
    device = torch.device('cuda:0' if len(availble_gpus) > 0 else 'cpu')

    checkpoint = torch.load(args['model'])
    if isinstance(checkpoint, dict) and 'state_dict' in checkpoint.keys():
        checkpoint = checkpoint['state_dict']
    if 'module' in list(checkpoint.keys())[0] and not isinstance(model, torch.nn.DataParallel):
        model = torch.nn.DataParallel(model)
    model.load_state_dict(checkpoint)
    model.to(device)
    model.eval()
    #test
    if args['half']:
        model=model.half()

    output_dir = os.path.join(root, args['output'])
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with torch.no_grad():
        tbar = tqdm(trays, ncols=100)
        Total_Inference_Time=0
        for c, img_file in enumerate(tbar):     
            output = {
                "mask": None,
                "blend": None,
                "percentage": (c+1)/len(trays),
                "infer_time": 0,
                "pc_0": 0,
                "pc_1": 0,
                "pc_2": 0,
                "pc_3": 0,
                "pc_total": 0
            } 
            image = Image.open(img_file.path).convert('RGB')
            original_size=image.size

            if base_size:
                image = image.resize(size=(base_size, base_size), resample=Image.BILINEAR)

            #input = normalize(to_tensor(image)).unsqueeze(0)
            input = to_tensor(image).unsqueeze(0)
            if args['half']:
                input = input.half()
            ticks = time.time()
            if args['mode'] == 'multiscale':
                prediction = multi_scale_predict(model, input, scales, num_classes, device)
            elif args['mode'] == 'sliding':
                prediction = sliding_predict(model, input, num_classes)
            else:
                prediction = model(input.to(device))
                output["infer_time"] = time.time()-ticks
                Total_Inference_Time += output["infer_time"]
                if arch_type[:2] == 'IC':
                    prediction = prediction[0]
                elif arch_type[-3:] == 'OCR':
                    prediction = prediction[0] 
                elif arch_type[:3] == 'Enc':
                    prediction = prediction[0]
                elif arch_type[:5] == 'DANet':
                    prediction = prediction[0]

                if args['half']:
                    prediction = prediction.squeeze(0).float().cpu().numpy() 
                else:
                    prediction = prediction.squeeze(0).cpu().numpy()  

            prediction = F.softmax(torch.from_numpy(prediction), dim=0).argmax(0).cpu().numpy()
            
            save_images(image, prediction, output_dir, img_file.path, pal, original_size, output)
           
            yield (img_file, output) if backref else output

        print("time used: {}".format(Total_Inference_Time))
'''

def parse_arguments():
    parser = argparse.ArgumentParser(description='Inference')
    parser.add_argument('-c', '--config', default='VOC',type=str,
                        help='The config used to train the model')
    parser.add_argument('-mo', '--mode', default='normal', type=str,
                        help='Mode used for prediction: either [multiscale, sliding]')
    parser.add_argument('-m', '--model', default='model_weights.pth', type=str,
                        help='Path to the .pth model checkpoint to be used in the prediction')
    parser.add_argument('-i', '--images', default=None, type=str,
                        help='Path to the images to be segmented')
    parser.add_argument('--half', action='store_true', help='half precision FP16 inference')
    parser.add_argument('-o', '--output', default='outputs', type=str,  
                        help='Output Path')
    parser.add_argument('-e', '--extension', default='png', type=str,
                        help='The extension of the images to be segmented')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()
