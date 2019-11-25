import cv2
from dataset_toolkit.Generate.AbstractGenerate import AbstractGenerate


class RotationGenerate(AbstractGenerate):

    def __init__(self, lower_bound: int, upper_bound: int, step: int):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.step = step

    def generate(self, img) -> list:
        new_imgs = []
        rows, cols, _ = img.shape
        for theta in range(self.lower_bound, self.upper_bound, self.step):
            M = cv2.getRotationMatrix2D((cols / 2, rows / 2), theta, 1)
            new_imgs += [cv2.warpAffine(img, M, (cols, rows))]
        return new_imgs
