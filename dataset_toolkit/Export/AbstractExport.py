from abc import ABC, abstractmethod

from dataset_toolkit.Model.AnnotationModel import AnnotationModel


class AbstractExport(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def append(self, new_dataset_dir: str, new_annotations_dir: str,
               annotation_model: AnnotationModel, new_annotation_filename: str):
        pass

    @abstractmethod
    def close(self):
        pass