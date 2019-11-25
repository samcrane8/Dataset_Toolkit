import os
from dataset_toolkit.Save.AbstractAnnotationSave import AbstractAnnotationSave


class DarknetAnnotationSave(AbstractAnnotationSave):

    @staticmethod
    def save(new_dataset_dir: str, new_annotations_dir: str,
             old_annotation_data: dict, new_image_filename: str):
        if not os.path.isdir(new_annotations_dir):
            os.mkdir(new_annotations_dir)
        annotation_str = ""
        for object in old_annotation_data.objects:
            obj_dict = object.dict()
            object_class = 0
            bndbox = obj_dict['bndbox']
            x = bndbox['xmin']
            y = bndbox['ymin']
            width = bndbox['xmax'] - x
            height = bndbox['ymax'] - y
            # <object-class> <x> <y> <width> <height>
            object_annotation = "{0} {1} {2} {3} {4} \n".format(object_class, x, y, width, height)
            annotation_str += object_annotation
        save_path = DarknetAnnotationSave.make_save_path(new_annotations_dir, new_image_filename, '.txt')
        print("Save path: ", save_path)
        with open(save_path, 'w') as temp_xml:
            temp_xml.write(annotation_str)
