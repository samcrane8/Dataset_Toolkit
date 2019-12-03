import os

from dataset_toolkit.Save.AbstractAnnotationSave import AbstractAnnotationSave


class DatasetModel:

    def __init__(self, data_dir: str, annotation_dir: str = None):
        self.data_dir = data_dir
        if not annotation_dir:
            self.annotations_dir = data_dir + '/annotations'
            print(self.annotations_dir)
        else:
            self.annotations_dir = annotation_dir

    def get_annotations(self):
        files = [os.path.join(self.annotations_dir, x) for x in os.listdir(self.annotations_dir)]
        return files

    def get_unannotated_image_filenames(self, ann_format):
        files = [x for x in os.listdir(self.data_dir)]
        unannotated_files = []
        for file in files:
            if not AbstractAnnotationSave.make_save_path("", file, ann_format) in files:
                unannotated_files += [file]
        return unannotated_files

    def get_image_filenames(self):
        files = [x for x in os.listdir(self.data_dir)]
        return files

    def get_image_paths(self):
        files = [os.path.join(self.data_dir, x) for x in os.listdir(self.data_dir)]
        return files
