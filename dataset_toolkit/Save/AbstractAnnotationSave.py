import os


class AbstractAnnotationSave:

    @staticmethod
    def make_save_path(savedir, img_name, ann_format):
        img_name = img_name.split('.')
        del img_name[-1]
        img_name = '.'.join(img_name) + ann_format
        return os.path.join(savedir, img_name)

    @staticmethod
    def save(new_dataset_dir: str, new_annotations_dir: str, image_path: str, image_filename: str):
        pass
