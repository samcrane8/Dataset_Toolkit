from abc import ABC, abstractmethod

from dataset_toolkit.Model.AnnotationModel import AnnotationModel


class AbstractRead(ABC):

    @staticmethod
    def read(self, path: str) -> AnnotationModel:
        pass
