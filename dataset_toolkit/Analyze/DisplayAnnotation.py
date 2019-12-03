import cv2
from pydarknet import Detector, Image

from dataset_toolkit.Model.AnnotationModel import AnnotationModel, AnnotationSize, AnnotationObjectModel


class DisplayAnnotation:

    def analyze(self, annotation_model: AnnotationModel):
        frame = cv2.imread(annotation_model.path)

        for obj in annotation_model.objects:
            bndbox = obj.bndbox
            print(bndbox)
            cv2.rectangle(frame, (int(bndbox['xmin']), int(bndbox['ymin'])), (int(bndbox['xmax']), int(bndbox['ymax'])), (255, 0, 0))
            cv2.putText(frame, str("person"), (int(bndbox['xmin']), int(bndbox['ymin'])), cv2.FONT_HERSHEY_COMPLEX, 1,
                        (255, 255, 0))
        cv2.imshow('send', frame)
        if cv2.waitKey(1)&0xFF == ord('q'):
            pass
        input("Press Enter to continue...")
