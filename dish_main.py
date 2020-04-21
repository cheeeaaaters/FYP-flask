import time
import numpy as np
import os
from PIL import Image
import torch
import torchvision
from torchvision import transforms, datasets, models

def process(trays, backref=False):
    root = os.path.dirname(__file__)
    load_path = os.path.join(root, 'dishes_classifier.pth')

    ds_trans = transforms.Compose([transforms.Scale((224,224)),
                               transforms.CenterCrop(224),
                               transforms.ToTensor()
                               #,normalize
                               ])

    model = models.resnext101_32x8d(pretrained=True)    
    num_ftrs = model.fc.in_features
    model.fc = torch.nn.Linear(num_ftrs, 5)
    model = model.cuda()    
    model.load_state_dict(torch.load(load_path))
    model.train(False)
    model.eval()

    output = {
        "preds": None,
        "infer_time": 0,
        "percentage": 0
    }

    for i, tray in enumerate(trays):        
        image = Image.open(tray.path)
        image = ds_trans(image)
        image = torch.unsqueeze(image, dim=0)
        time_start = time.time()
        outputs = model(image.cuda())
        _, preds = torch.max(outputs.data, 1)
        output["infer_time"] = time.time() - time_start
        output["preds"] = preds
        output["percentage"] = (i+1)/len(trays)
        yield (tray, output) if backref else output