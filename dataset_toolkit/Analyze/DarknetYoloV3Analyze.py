import cv2
from pydarknet import Detector, Image

from dataset_toolkit.Model.AnnotationModel import AnnotationModel, AnnotationSize, AnnotationObjectModel


class DarknetYoloV3Analyze:

    def __init__(self):
        self.net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("wgt/yolov3.weights", encoding="utf-8"), 0,
                       bytes("cfg/coco.data", encoding="utf-8"))

    def analyze(self, filename: str, folder: str) -> AnnotationModel:
        path = folder+'/'+filename
        frame = cv2.imread(path)
        dark_frame = Image(frame)
        results = self.net.detect(dark_frame)
        aw, ah, ad = frame.shape
        annotation_size = AnnotationSize(aw, ah, ad)
        objects = []
        for cat, score, bounds in results:
            x, y, w, h = bounds
            bndbox = {
                'xmin': x,
                'xmax': x+w,
                'ymin': y,
                'ymax': y+h,
            }
            objects += [AnnotationObjectModel(str(cat), bndbox)]
        annotation_model = AnnotationModel(filename, folder, folder+'/'+filename,
                                           annotation_size, objects)
        return annotation_model
