import time
import datetime
import numpy as np

from dataset_toolkit.Model.DatasetModel import DatasetModel
from dataset_toolkit.Model.AnnotationModel import AnnotationModel
from dataset_toolkit.Save.XMLAnnotationSave import XMLAnnotationSave

from dataset_toolkit.Read.XMLRead import XMLRead

from dataset_toolkit.Analyze.DisplayAnnotation import DisplayAnnotation


def auto_annotate_from_model(dataset_dir, annotation_dir):
    dataset = DatasetModel(dataset_dir, annotation_dir=annotation_dir)

    display_ann = DisplayAnnotation()

    counter = 0
    files = dataset.get_annotations()
    start_time = time.time()
    last_time = start_time
    for file_name in files:
        print("filename: ", file_name)
        # try:
        print("{}/{}".format(counter, len(files)))
        annotation_model = XMLRead.read(file_name)
        counter += 1
        display_ann.analyze(annotation_model)
        elapsed_time_one_file = time.time() - last_time
        total_time = time.time() - start_time
        print("Time elapsed for last file: ", elapsed_time_one_file)
        print("Total time: ", total_time)
        avg_time = total_time/counter
        last_time = time.time()
        print("Avg. time: ", avg_time)
        end_time = avg_time * (len(files) - counter)
        end_time = str(datetime.timedelta(seconds=end_time))
        print("End time: ", end_time)
        # except Exception:
        #     print("filename failed: ", file_name)
        #     last_time = time.time()
        #     counter += 1


if __name__ == "__main__":
    print("ODT INITIALIZED")
    dataset_dir = "/mnt/sda/DataLake/Seafile/daimler_bus_dataset_tf/images/"
    annotation_dir = "/mnt/sda/DataLake/Seafile/daimler_bus_dataset_tf/annotations/"
    auto_annotate_from_model(dataset_dir, annotation_dir)
