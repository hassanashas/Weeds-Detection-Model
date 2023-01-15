import torch
import os
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
# from detectron2.structures import BoxMode
# import fiftyone as fo
# import fiftyone.zoo as foz
# import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

# cfg = get_cfg()
# cfg.merge_from_file(model_zoo.get_config_file(
#     "COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml"))
# cfg.DATASETS.TRAIN = ("fiftyone_train",)
# cfg.DATASETS.TEST = ()
# cfg.DATALOADER.NUM_WORKERS = 2
# cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
#     "COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml")  # Let training initialize from model zoo
# # This is the real "batch size" commonly known to deep learning people
# cfg.SOLVER.IMS_PER_BATCH = 2
# cfg.SOLVER.BASE_LR = 0.00025  # pick a good LR
# # 300 iterations seems good enough for this toy dataset; you will need to train longer for a practical dataset
# cfg.SOLVER.MAX_ITER = 10000
# cfg.SOLVER.STEPS = []        # do not decay learning rate
# # The "RoIHead batch size". 128 is faster, and good enough for this toy dataset (default: 512)
# cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128
# # only has one class (weed). (see https://detectron2.readthedocs.io/tutorials/datasets.html#update-the-config-for-new-datasets)
# cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
# # NOTE: this config means the number of classes, but a few popular unofficial tutorials incorrect uses num_classes+1 here.
# predictor = DefaultPredictor(cfg)

# PATH = "model_final.pth"


model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                          'imageNetProject/model_final.pth')
image_path = os.path.dirname(os.path.dirname(__file__))


from detectron2.engine import DefaultTrainer

cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml"))
# cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
# cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml")  # Let training initialize from model zoo
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5   # set a custom testing threshold
cfg.MODEL.WEIGHTS = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                          'imageNetProject/model_final.pth')
cfg.MODEL.DEVICE = "cpu"
cfg.DATASETS.TRAIN = ("fiftyone_train",)
cfg.DATASETS.TEST = ()
cfg.DATALOADER.NUM_WORKERS = 2
# cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml")  # Let training initialize from model zoo
cfg.SOLVER.IMS_PER_BATCH = 2  # This is the real "batch size" commonly known to deep learning people
cfg.SOLVER.BASE_LR = 0.00025  # pick a good LR
cfg.SOLVER.MAX_ITER = 10000   # 300 iterations seems good enough for this toy dataset; you will need to train longer for a practical dataset
cfg.SOLVER.STEPS = []        # do not decay learning rate
cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128   # The "RoIHead batch size". 128 is faster, and good enough for this toy dataset (default: 512)
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1  # only has one class (weed). (see https://detectron2.readthedocs.io/tutorials/datasets.html#update-the-config-for-new-datasets)
# NOTE: this config means the number of classes, but a few popular unofficial tutorials incorrect uses num_classes+1 here.

predictor = DefaultPredictor(cfg)

def show_img(path, extra=False):
    path = path.replace('/', '\\')
    im = cv2.imread(image_path + path)
    # im =cv2.LoadImage(image_path+path)
    outputs = predictor(im)
    if extra:
        print("\n\nHERE:", outputs["instances"].pred_classes)
        print(outputs["instances"].pred_boxes)
    v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    out = out.get_image()[:, :, ::-1]
    arr = {"weed": len(outputs["instances"].pred_classes)}
    return out, arr, 1

# show_img(image_path)

# model = torch.load(model_path, map_location=lambda storage, Loc: storage)
# model.eval()
# model.load_state_dict(checkpoint['state_dict'])


# class Net(nn.Module):

#     def _init_(self):
#         super(Net, self)._init_()
#         self.fc1 = nn.Linear(input_size, hidden_size)
#         self.fc2 = nn.Linear(hidden_size, hidden_size)
#         self.fc3 = nn.Linear(hidden_size, output_size)

#     def forward(self, x):
#         x = torch.sigmoid(self.fc1(x))
#         x = torch.sigmoid(self.fc2(x))
#         x = self.fc3(x)

#         return F.log_softmax(x, dim=-1)


# model = Net()  # <---------------------------- Extra thing added
# # <---- if running on a CPU, else 'cuda'
# model = torch.load('model.pth', map_location=torch.device('cpu'))

aug = transforms.Compose([
    transforms.Resize((224, 224)),
    # transforms.CenterCrop(10),
    transforms.RandomAffine(degrees=0, translate=None, scale=(
                            1, 1.5), shear=None),
    transforms.RandomHorizontalFlip(), transforms.RandomVerticalFlip(
    ), transforms.RandomRotation(360),
    transforms.ToTensor(),
    transforms.Normalize([0.5820, 0.4512, 0.4023], [
        0.2217, 0.1858, 0.1705]),

])


# def image_pred(url):
#     new_url = image_path+url
#     img = Image.open(new_url)
#     img = img.convert(mode='RGB')
#     image = aug(img)

#     image = image.unsqueeze(0)
#     type(image)
#     print("Bye")
#     print(type(model))
#     out = model(image)
#     print(out)
#     out = out.detach().numpy
#     out = numpy.argmax(out)
#     return out
