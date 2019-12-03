import os
import cv2
from lxml import etree
import xml.etree.cElementTree as ET
from dataset_toolkit.Save.AbstractAnnotationSave import AbstractAnnotationSave
from dataset_toolkit.Model.AnnotationModel import AnnotationModel


class XMLAnnotationSave(AbstractAnnotationSave):

    @staticmethod
    def save(new_dataset_dir: str, new_annotations_dir: str,
             annotation_model: AnnotationModel, new_annotation_filename: str):
        if not os.path.isdir(new_annotations_dir):
            os.mkdir(new_annotations_dir)
        image_path = annotation_model.path
        image = cv2.imread(image_path)
        height, width, depth = image.shape

        annotation = ET.Element('annotation')
        ET.SubElement(annotation, 'folder').text = new_dataset_dir
        ET.SubElement(annotation, 'filename').text = new_annotation_filename
        ET.SubElement(annotation, 'segmented').text = '0'
        size = ET.SubElement(annotation, 'size')
        ET.SubElement(size, 'width').text = str(width)
        ET.SubElement(size, 'height').text = str(height)
        ET.SubElement(size, 'depth').text = str(depth)
        for obj in annotation_model.objects:
            ob = ET.SubElement(annotation, 'object')
            ET.SubElement(ob, 'name').text = obj.name
            ET.SubElement(ob, 'pose').text = 'Unspecified'
            ET.SubElement(ob, 'truncated').text = '0'
            ET.SubElement(ob, 'difficult').text = '0'
            bbox = ET.SubElement(ob, 'bndbox')
            ET.SubElement(bbox, 'xmin').text = str(int(obj.bndbox['xmin']))
            ET.SubElement(bbox, 'ymin').text = str(int(obj.bndbox['ymin']))
            ET.SubElement(bbox, 'xmax').text = str(int(obj.bndbox['xmax']))
            ET.SubElement(bbox, 'ymax').text = str(int(obj.bndbox['ymax']))
        xml_str = ET.tostring(annotation)
        root = etree.fromstring(xml_str)
        xml_str = etree.tostring(root, pretty_print=True)
        save_path = XMLAnnotationSave.make_save_path(new_annotations_dir, new_annotation_filename, '.xml')
        with open(save_path, 'wb') as temp_xml:
            temp_xml.write(xml_str)
