import os
from dataset_toolkit.Save.AbstractAnnotationSave import AbstractAnnotationSave
from dataset_toolkit.Model.AnnotationModel import AnnotationModel

class DarknetAnnotationSave(AbstractAnnotationSave):

    @staticmethod
    def save(new_dataset_dir: str, new_annotations_dir: str,
             annotation_model: AnnotationModel, new_annotation_filename: str):
        if not os.path.isdir(new_annotations_dir):
            os.mkdir(new_annotations_dir)
        annotation_str = ""
        total_width = annotation_model.size.width
        total_height = annotation_model.size.height
        for object in annotation_model.objects:
            obj_dict = object.dict()
            object_class = 0
            bndbox = obj_dict['bndbox']
            x = bndbox['xmin']
            y = bndbox['ymin']
            width = bndbox['xmax'] - x
            height = bndbox['ymax'] - y
            center_x = x + width/2
            center_y = y + height/2
            width /= total_width
            height /= total_height
            center_x /= total_width
            center_y /= total_height
            # <object-class> <x> <y> <width> <height>
            object_annotation = "{0} {1} {2} {3} {4} \n".format(object_class, center_x, center_y, width, height)
            # print("save: ", object_annotation)
            # print("tot w,h: ", total_width, total_height)
            annotation_str += object_annotation
        save_path = DarknetAnnotationSave.make_save_path(new_annotations_dir, new_annotation_filename, '.txt')
        with open(save_path, 'w') as temp_xml:
            temp_xml.write(annotation_str)
