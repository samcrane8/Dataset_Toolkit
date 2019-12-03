from lxml import etree
from dataset_toolkit.Read.AbstractRead import AbstractRead
from dataset_toolkit.Model.AnnotationModel import AnnotationModel, AnnotationSize, AnnotationObjectModel


class XMLRead(AbstractRead):

    @staticmethod
    def read(file_name):
        root = etree.parse(file_name)
        filename = root.xpath('filename')[0].text
        folder = root.xpath('folder')[0].text
        path = folder + '/' + filename
        size = XMLRead.load_size(root.xpath('size')[0])
        objects_xml = root.xpath('object')
        objects = [XMLRead.load_object(x) for x in objects_xml]
        return AnnotationModel(filename, folder, path, size, objects)

    @staticmethod
    def load_size(size_xml):
        width = int(size_xml.xpath('width')[0].text)
        height = int(size_xml.xpath('height')[0].text)
        depth = int(size_xml.xpath('depth')[0].text)
        return AnnotationSize(width, height, depth)

    @staticmethod
    def load_object(object_xml):
        name = object_xml.xpath('name')[0].text
        bndbox = object_xml.xpath('bndbox')[0]
        bndbox = {
            'xmin': int(bndbox.xpath('xmin')[0].text),
            'xmax': int(bndbox.xpath('xmax')[0].text),
            'ymin': int(bndbox.xpath('ymin')[0].text),
            'ymax': int(bndbox.xpath('ymax')[0].text)
        }
        return AnnotationObjectModel(name, bndbox)
