import time
import datetime
import numpy as np

from dataset_toolkit.Model.DatasetModel import DatasetModel
from dataset_toolkit.Model.AnnotationModel import AnnotationModel
from dataset_toolkit.Save.DarknetAnnotationSave import DarknetAnnotationSave
from dataset_toolkit.Save.DarknetAnnotationSave import DarknetAnnotationSave

from dataset_toolkit.Analyze.DarknetYoloV3Analyze import DarknetYoloV3Analyze


def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


def auto_annotate_from_model(dataset_dir):
    dataset = DatasetModel(dataset_dir)

    dyv3_analyze = DarknetYoloV3Analyze()

    counter = 0
    files = dataset.get_unannotated_image_filenames('.txt')
    start_time = time.time()
    last_time = start_time
    for file_name in files:
        print("filename: ", file_name)
        try:
            print("{}/{}".format(counter, len(files)))
            annotation_model = dyv3_analyze.analyze(file_name, dataset_dir)
            DarknetAnnotationSave.save(dataset_dir, dataset_dir, annotation_model, annotation_model.filename)
            counter += 1

            elapsed_time_one_file = time.time() - last_time
            total_time = time.time() - last_time
            print("Time elapsed for last file: ", elapsed_time_one_file)
            print("Total time: ", total_time)
            avg_time = total_time/counter
            last_time = time.time()
            print("Avg. time: ", avg_time)
            end_time = avg_time * (len(files) - counter)
            end_time = str(datetime.timedelta(seconds=end_time))
            print("End time: ", end_time)
        except Exception:
            print("filename failed: ", file_name)
            last_time = time.time()
            counter += 1


if __name__ == "__main__":
    print("ODT INITIALIZED")
    dataset_dir = "/mnt/sda/Datasets/daimler_people_counter/dpc_dataset"
    # dataset_dir = "/home/sam/Desktop/dpc_dataset"
    auto_annotate_from_model(dataset_dir)
