import os
import cv2
from lxml import etree
import xml.etree.cElementTree as ET
from dataset_toolkit.Save.AbstractAnnotationSave import AbstractAnnotationSave
from dataset_toolkit.Model.DatasetPartitionModel import DatasetPartitionModel
from dataset_toolkit.Model.AnnotationModel import AnnotationModel


class XMLAnnotationSave(AbstractAnnotationSave):

    def save(self, new_dataset_dir: str, new_annotations_dir: str,
             old_annotation_data: dict, new_image_filename: str):
        if not os.path.isdir(new_annotations_dir):
            os.mkdir(new_annotations_dir)
        image_path = old_annotation_data['path']
        image = cv2.imread(image_path)
        height, width, depth = image.shape

        annotation = ET.Element('annotation')
        ET.SubElement(annotation, 'folder').text = new_dataset_dir
        ET.SubElement(annotation, 'filename').text = new_image_filename
        ET.SubElement(annotation, 'segmented').text = '0'
        size = ET.SubElement(annotation, 'size')
        ET.SubElement(size, 'width').text = str(width)
        ET.SubElement(size, 'height').text = str(height)
        ET.SubElement(size, 'depth').text = str(depth)
        for obj in old_annotation_data['objects']:
            ob = ET.SubElement(annotation, 'object')
            ET.SubElement(ob, 'name').text = obj
            ET.SubElement(ob, 'pose').text = 'Unspecified'
            ET.SubElement(ob, 'truncated').text = '0'
            ET.SubElement(ob, 'difficult').text = '0'
            bbox = ET.SubElement(ob, 'bndbox')
            ET.SubElement(bbox, 'xmin').text = str(obj.bndbox[0][0])
            ET.SubElement(bbox, 'ymin').text = str(obj.bndbox[0][1])
            ET.SubElement(bbox, 'xmax').text = str(obj.bndbox[1][0])
            ET.SubElement(bbox, 'ymax').text = str(obj.bndbox[1][1])
        xml_str = ET.tostring(annotation)
        root = etree.fromstring(xml_str)
        xml_str = etree.tostring(root, pretty_print=True)
        save_path = XMLAnnotationSave.make_save_path(new_annotations_dir, new_image_filename, '.xml')
        with open(save_path, 'wb') as temp_xml:
            temp_xml.write(xml_str)
