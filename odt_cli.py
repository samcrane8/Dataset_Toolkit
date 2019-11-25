from dataset_toolkit import Toolkit


if __name__ == "__main__":
    print("ODT INITIALIZED")
    old_dataset_dir = ""
    new_dataset_dir = ""
    old_format = "tensorflow"
    new_format = "darknet"

    Toolkit.convert(old_dataset_dir, new_dataset_dir, old_format, new_format)