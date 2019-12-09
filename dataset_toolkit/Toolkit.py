import os
from dataset_toolkit.Model.DatasetPartitionModel import DatasetPartitionModel
from dataset_toolkit.Model.DatasetModel import DatasetModel
from dataset_toolkit.Model.AnnotationModel import AnnotationModel

from dataset_toolkit.Read.AbstractRead import AbstractRead
from dataset_toolkit.Read.XMLRead import XMLRead

from dataset_toolkit.Save.AbstractAnnotationSave import AbstractAnnotationSave
from dataset_toolkit.Save.XMLAnnotationSave import XMLAnnotationSave
from dataset_toolkit.Save.DarknetAnnotationSave import DarknetAnnotationSave

from dataset_toolkit.Export.AbstractExport import AbstractExport
from dataset_toolkit.Export.TFRecordExport import TFRecordAnnotationSave

from dataset_toolkit.utils.ProgressBar import ProgressBar


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


def export(dataset_dir: str, old_annotation_dir: str, old_format: str, export_file: str, new_format: str):
    dataset = DatasetModel(dataset_dir, annotation_dir=old_annotation_dir)

    files = dataset.get_annotations()
    progress_bar = ProgressBar(len(files))

    if old_format == 'xml':
        AnnotationRead: AbstractRead = XMLRead
    else:
        print("No recognizable input format.")
        return

    if new_format == 'tfrecord':
        exporter: AbstractExport = TFRecordAnnotationSave(export_file)
        exporter.start()
    else:
        print("No recognizable output format.")
        return

    for annotation_filename in files:
        print("filename: ", annotation_filename)
        # try:
        annotation_model: AnnotationModel = AnnotationRead.read(annotation_filename)
        if len(annotation_model.objects) > 0:
            exporter.append(dataset_dir, new_annotation_dir, annotation_model, annotation_model.filename)
        # except Exception:
        # print("filename failed: ", annotation_filename)
        progress_bar.lap()

    exporter.close()


def generate_annotation_save(old_format: str) -> AbstractAnnotationSave:
    pass
