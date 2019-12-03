from dataset_toolkit.Model.AnnotationModel import AnnotationModel


class AbstractRead:

    def read(self, path: str) -> AnnotationModel:
        pass
