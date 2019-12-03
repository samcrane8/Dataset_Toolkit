# import os
# import cv2
# from dataset_toolkit.Model.DatasetPartitionModel import DatasetPartitionModel
#
# from dataset_toolkit.Generate.AbstractGenerate import AbstractGenerate
# from dataset_toolkit.Generate.RotationGenerate import RotationGenerate
# from dataset_toolkit.Generate.FlipGenerate import FlipGenerate
# from dataset_toolkit.Generate.ShiftGenerate import ShiftGenerate
#
# from dataset_toolkit.Model.AnnotationModel import AnnotationModel
#
#
# class GeneratorPipeline:
#
#     def __init__(self, dataset_partition: DatasetPartitionModel, new_dataset_dir: str,
#                  generators: list[AbstractGenerate]):
#         self.dataset_partition = dataset_partition
#         self.new_dataset_dir = new_dataset_dir
#         self.generators = generators
#
#     @staticmethod
#     def get_generator_pipeline(dataset_partition: DatasetPartitionModel, new_dataset_partition: str,
#                                generators: list):
#         generator_list = []
#         for generator in generators:
#             if generator == 'rotate':
#                 generator_list += RotationGenerate(-45, 45, 15)
#             elif generator == 'flip':
#                 generator_list += FlipGenerate(horizontal=True, vertical=False)
#             elif generator == 'shift':
#                 generator_list += ShiftGenerate(2, 2)
#         return GeneratorPipeline(dataset_partition, new_dataset_partition, generator_list)
#
#     @staticmethod
#     def get_annotated_area(img, annotation_object):
#         left = annotation_object['bndbox']['xmin']
#         right = annotation_object['bndbox']['xmax']
#         top = annotation_object['bndbox']['ymin']
#         bottom = annotation_object['bndbox']['ymax']
#         return img[top:bottom, left:right]
#
#     def synthesize_images(self, object_img):
#         synthetic_image_list = [object_img]
#         for generator in self.generators:
#             synthetic_image_list += generator.generate(object_img)
#         return synthetic_image_list
#
#     def save_images_and_annotations(self, new_synthetic_images, old_annotation_data):
#         num = 0
#         new_annotation_dir = self.new_dataset_dir + '/annotations'
#         for new_image in new_synthetic_images:
#             base_filename = old_annotation_data['filename'].split('.')
#             base_filename.insert(1, str(num))
#             new_image_filename = '.'.join(base_filename)
#             new_image_path = os.path.join(self.new_dataset_dir, new_image_filename)
#             cv2.imwrite(new_image_path, new_image)
#             self.dataset_partition.annotation_format.save(self.new_dataset_dir, new_annotation_dir,
#                                                           old_annotation_data, new_image_filename)
#             num += 1
#
#     def generate(self):
#         for annotation_path in self.dataset_partition.get_annotations():
#             try:
#                 annotation_data = AnnotationModel(annotation_path).dict()
#                 img = cv2.imread(annotation_data['path'])
#                 for annotation_object in annotation_data['objects']:
#                     object_img = GeneratorPipeline.get_annotated_area(img, annotation_object)
#                     new_synthetic_images = self.synthesize_images(object_img)
#                     self.save_images_and_annotations(new_synthetic_images, annotation_data)
#             except:
#                 print("ERROR SCANNING PARTITION")
