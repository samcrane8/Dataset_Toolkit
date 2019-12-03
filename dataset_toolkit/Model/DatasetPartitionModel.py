import os

from dataset_toolkit.Save.AbstractAnnotationSave import AbstractAnnotationSave
from dataset_toolkit.Model.DatasetModel import DatasetModel


class DatasetPartitionModel(DatasetModel):

    def __init__(self, data_dir: str, annotation_save_format: AbstractAnnotationSave, size: int, bounds: (int, int) = None,
                 annotation_dir: str = None):
        DatasetModel.__init__(self, data_dir, annotation_dir)
        self.size = size
        self.bounds = bounds
        self.annotation_save_format = annotation_save_format