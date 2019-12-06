import os
import cv2
import hashlib
import numpy as np
from lxml import etree
import tensorflow as tf
import xml.etree.cElementTree as ET
from dataset_toolkit.Export.AbstractExport import AbstractExport
from dataset_toolkit.Model.AnnotationModel import AnnotationModel


class TFRecordAnnotationSave(AbstractExport):

    def __init__(self, file_path):
        self.file_path = file_path
        self.writer = None

    def start(self):
        self.writer = tf.io.TFRecordWriter(self.file_path)

    def append(self, new_dataset_dir: str, new_annotations_dir: str,
               annotation_model: AnnotationModel, new_annotation_filename: str):
        with tf.io.gfile.GFile(os.path.join(annotation_model.path), 'rb') as fid:
            encoded_jpg = fid.read()
        image_format = b'png'
        xmins = []
        xmaxs = []
        ymins = []
        ymaxs = []
        classes_text = []
        classes = []
        for obj in annotation_model.objects:
            xmins.append(obj.bndbox['xmin'] / annotation_model.size.width)
            xmaxs.append(obj.bndbox['xmax'] / annotation_model.size.width)
            ymins.append(obj.bndbox['ymin'] / annotation_model.size.height)
            ymaxs.append(obj.bndbox['ymax'] / annotation_model.size.height)
            classes_text.append("person".encode('utf8'))
            classes.append(1)

        key = hashlib.sha256(encoded_jpg).hexdigest()

        tf_example = tf.train.Example(features=tf.train.Features(feature={
            'image/height': TFRecordAnnotationSave.int64_feature(annotation_model.size.height),
            'image/width': TFRecordAnnotationSave.int64_feature(annotation_model.size.width),
            'image/depth': TFRecordAnnotationSave.int64_feature(annotation_model.size.depth),
            'image/filename': TFRecordAnnotationSave.bytes_feature(annotation_model.filename.encode('utf8')),
            'image/source_id': TFRecordAnnotationSave.bytes_feature(annotation_model.filename.encode('utf8')),
            'image/encoded': TFRecordAnnotationSave.bytes_feature(encoded_jpg),
            'image/format': TFRecordAnnotationSave.bytes_feature(image_format),
            'image/key/sha256': TFRecordAnnotationSave.bytes_feature(key.encode('utf8')),
            'image/object/bbox/xmin': TFRecordAnnotationSave.float_list_feature(xmins),
            'image/object/bbox/xmax': TFRecordAnnotationSave.float_list_feature(xmaxs),
            'image/object/bbox/ymin': TFRecordAnnotationSave.float_list_feature(ymins),
            'image/object/bbox/ymax': TFRecordAnnotationSave.float_list_feature(ymaxs),
            'image/object/class/text': TFRecordAnnotationSave.bytes_list_feature(classes_text),
            'image/object/class/label': TFRecordAnnotationSave.int64_list_feature(classes),
        }))
        self.writer.write(tf_example.SerializeToString())

    def close(self):
        self.writer.close()

    @staticmethod
    def load_image(addr):
        # read an image and resize to (224, 224)
        # cv2 load images as BGR, convert it to RGB
        img = cv2.imread(addr)
        img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_CUBIC)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32)
        return img

    @staticmethod
    def int64_feature(value):
        return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

    @staticmethod
    def int64_list_feature(value):
        return tf.train.Feature(int64_list=tf.train.Int64List(value=value))

    @staticmethod
    def bytes_feature(value):
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

    @staticmethod
    def bytes_list_feature(value):
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=value))

    @staticmethod
    def float_list_feature(value):
        return tf.train.Feature(float_list=tf.train.FloatList(value=value))