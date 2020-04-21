def main():
    args = parse_arguments()

    dishes = {"SiuMe":{"rice":0,"vegetable":0,"meat":0},
    		  "Japan":{"rice":0},
    		  "Teppan":{"rice":0},
    		  "White":{},
    		  "TwoDishes":{}
              }

    dishesMap ={0:"SiuME",1:"Japan",2:"Teppan",3:"White",4:"TwoDishes"}

    dish_net=models.resnext101_32x8d(pretrained=True)
    num_ftrs = dish_net.fc.in_features
	dish_net.fc = torch.nn.Linear(num_ftrs, 5)
	dish_net.load_state_dict("dishes_classifier.pth")

	for dish,foodtypes in dishes:
		for foodtype, volume_net in foodtypes:
			volume_net = models.resnext101_32x8d(pretrained=True)
			num_ftrs = volume_net.fc.in_features
			volume_net.fc = torch.nn.Linear(num_ftrs, 3)
			volume_net.load_state_dict(dish+"_"+foodtype+".pth")
			volume_net.cuda()
			volume_net.eval()

    image_files = sorted(glob(os.path.join(args.images, f'*.{args.extension}')))


def parse_arguments():
    parser = argparse.ArgumentParser(description='Inference')
    parser.add_argument('-i', '--images', default=None, type=str,
                        help='Path to the images to be segmented')
    parser.add_argument('-o', '--output', default='outputs', type=str,  
                        help='Output Path')
    parser.add_argument('-e', '--extension', default='png', type=str,
                        help='The extension of the images to be segmented')
    args = parser.parse_args()
    return args