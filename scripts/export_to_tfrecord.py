from dataset_toolkit import Toolkit

dataset_dir = "/mnt/sda/DataLake/Seafile/daimler_bus_dataset_tf/images/"
old_annotation_dir = "/mnt/sda/DataLake/Seafile/daimler_bus_dataset_tf/test"
old_format = "xml"

new_annotation_dir = "/mnt/sda/DataLake/Seafile/daimler_bus_dataset_tf/tfrecords"
new_format = "tfrecord"

Toolkit.export(dataset_dir, old_annotation_dir, old_format,
               new_annotation_dir, new_format)
