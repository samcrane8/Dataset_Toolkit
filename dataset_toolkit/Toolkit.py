import os
from dataset_toolkit.Model.DatasetPartitionModel import DatasetPartitionModel
from dataset_toolkit.Model.DatasetModel import DatasetModel
from dataset_toolkit.GeneratorPipeline import GeneratorPipeline

from dataset_toolkit.Save.AbstractAnnotationSave import AbstractAnnotationSave
from dataset_toolkit.Save.TensorflowAnnotationSave import XMLAnnotationSave


def generate(old_dataset_dir: str, new_dataset_dir: str, partitions: list):

    part_sum = 0
    for partition in partitions:
        part_sum += partition[0]
    if part_sum != 1.0:
        print("Partitions do not add up to 1. Quitting.")
        return

    generator_pipelines = []
    size = len([name for name in os.listdir(old_dataset_dir) if os.path.isfile(os.path.join(old_dataset_dir, name))])
    lower_bound = 0
    for partition in partitions:
        partition_percentage = partition[0]
        upper_bound = partition_percentage * size
        bounds = (lower_bound, upper_bound)
        dataset_partition = DatasetPartitionModel(old_dataset_dir, XMLAnnotationSave(), size, bounds)
        del partition[0]
        generator_pipelines += [GeneratorPipeline.get_generator_pipeline(dataset_partition, new_dataset_dir, partition)]
        lower_bound = upper_bound+1


def annotate():
    pass


def convert(old_annotation_dir: str, new_annotation_dir: str, old_format: str, new_format: str):
    print("CONVERTING")

    old_annotation_format = generate_annotation_save(old_format)
    dataset_model = DatasetModel(data_dir="", annotation_format=old_annotation_format, annotations_dir=old_annotation_dir)


def generate_annotation_save(old_format: str) -> AbstractAnnotationSave:
    pass