import time
import datetime
import numpy as np

from dataset_toolkit.Model.DatasetModel import DatasetModel
from dataset_toolkit.Model.AnnotationModel import AnnotationModel
from dataset_toolkit.Save.XMLAnnotationSave import XMLAnnotationSave

from dataset_toolkit.Analyze.DarknetYoloV3Analyze import DarknetYoloV3Analyze

from dataset_toolkit.utils.ProgressBar import ProgressBar


def auto_annotate_from_model(dataset_dir, annotation_dir):
    dataset = DatasetModel(dataset_dir, annotation_dir=annotation_dir)

    dyv3_analyze = DarknetYoloV3Analyze()

    files = dataset.get_unannotated_image_filenames('.xml')
    progress_bar = ProgressBar(len(files))
    for file_name in files:
        print("filename: ", file_name)
        try:
            annotation_model: AnnotationModel = dyv3_analyze.analyze(file_name, dataset_dir)
            if len(annotation_model.objects) > 0:
                XMLAnnotationSave.save(dataset_dir, annotation_dir, annotation_model, annotation_model.filename)

            progress_bar.lap()
        except Exception:
            print("filename failed: ", file_name)
            progress_bar.lap()


if __name__ == "__main__":
    print("ODT INITIALIZED")
    dataset_dir = "/mnt/sda/DataLake/Seafile/daimler_bus_dataset_tf/images/"
    annotation_dir = "/mnt/sda/DataLake/Seafile/daimler_bus_dataset_tf/annotations/"
    auto_annotate_from_model(dataset_dir, annotation_dir)
