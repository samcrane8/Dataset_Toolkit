from dataset_toolkit.Read.XMLRead import XMLRead
from dataset_toolkit.Model.DatasetModel import DatasetModel
from dataset_toolkit.Model.AnnotationModel import AnnotationModel
from dataset_toolkit.Save.DarknetAnnotationSave import DarknetAnnotationSave


def convert_tensorflow_to_darknet(dataset_dir, new_annotation_dir):
    old_dataset = DatasetModel(dataset_dir)

    for file_name in old_dataset.get_annotations():
        print("filename: ", file_name)
        annotation: AnnotationModel = XMLRead.read(file_name)
        print(annotation.objects)
        darknet_save = DarknetAnnotationSave.save(dataset_dir, new_annotation_dir, annotation, annotation.filename)


if __name__ == "__main__":
    print("ODT INITIALIZED")
    old_dataset_dir = "/mnt/sda/Datasets/daimler_wheelchair/wheelchair_dataset"
    new_dataset_dir = "/mnt/sda/Datasets/daimler_wheelchair/annotations-darknet"
    old_format = "tensorflow"
    new_format = "darknet"

    convert_tensorflow_to_darknet(old_dataset_dir, new_dataset_dir)
