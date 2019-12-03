import os
import cv2
from lxml import etree
import xml.etree.cElementTree as ET
from dataset_toolkit.Save.AbstractAnnotationSave import AbstractAnnotationSave
from dataset_toolkit.Model.AnnotationModel import AnnotationModel


class TFRecordAnnotationSave(AbstractAnnotationSave):

    @staticmethod
    def save(new_dataset_dir: str, new_annotations_dir: str,
             annotation_model: AnnotationModel, new_annotation_filename: str):
        print("Hi!")
