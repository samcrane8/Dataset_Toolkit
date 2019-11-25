import cv2
from dataset_toolkit.Generate.AbstractGenerate import AbstractGenerate


class ShiftGenerate(AbstractGenerate):

    def __init__(self, xshift: int, yshift: int):
        self.xshift = xshift
        self.yshift = yshift

    def generate(self, img) -> list:
        pass
        #TODO implement shift generator

