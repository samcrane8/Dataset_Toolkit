import cv2
from dataset_toolkit.Generate.AbstractGenerate import AbstractGenerate


class FlipGenerate(AbstractGenerate):

    def __init__(self, horizontal: bool, vertical: bool):
        self.horizontal = int(horizontal)
        self.vertical = int(vertical)

    def generate(self, img) -> list:
        return cv2.flip(img, self.horizontal, self.vertical)
