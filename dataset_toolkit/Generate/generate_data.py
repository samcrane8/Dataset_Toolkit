import os, sys
import cv2
from dataset_toolkit.Model.AnnotationModel import AnnotationModel
from dataset_toolkit.Save.XMLAnnotationSave import SaveXML

DEBUG = False


def generate_dataset(anntns_folder, new_dir, classification):
    for n, anntn_file in enumerate(os.scandir(anntns_folder)):
        annotation_data = AnnotationModel(anntn_file.path).dict()
        if DEBUG:
            print(annotation_data)
        img = cv2.imread(annotation_data['path'])
        for annotation_object in annotation_data['objects']:
            object_img = get_wheelchair(img, annotation_object)
            new_images = get_new_images(object_img, annotation_object)
            save_new_images(new_images, new_dir, annotation_data, annotation_object, classification)


def save_new_images(new_images, new_dir, annotation_data, annotation_object, classification):
    num = 0
    new_annotation_dir = new_dir + '/annotations'
    for new_image in new_images:
        base_filename = annotation_data['filename'].split('.')
        base_filename.insert(1, str(num))
        new_image_filename = '.'.join(base_filename)
        if DEBUG:
            print(new_image_filename)
        path = new_dir+'/'+new_image_filename
        if DEBUG:
            print(path)
        cv2.imwrite(path, new_image)
        width, height, _ = new_image.shape
        tl_list = [(0, 0)]
        br_list = [(height, width)]
        new_annotation_path = make_save_path(new_annotation_dir, new_image_filename)
        write_xml(new_dir, path, new_image_filename, [classification], tl_list, br_list, new_annotation_dir, new_annotation_path)
        num += 1
    return path


def get_new_images(object_img, annotation_object):
    new_images = [object_img]
    flip_img = flip_wheelchair(object_img)
    new_images += [flip_img]
    new_images += rotate_wheelchair(object_img)
    new_images += rotate_wheelchair(flip_img)
    if DEBUG:
        cv2.imshow(annotation_object['name'], object_img)
        num = 0
        for new_image in new_images:
            cv2.imshow(annotation_object['name'] + '-' + str(num), new_image)
            num += 1
        cv2.waitKey(0)
    if cv2.waitKey(1) == ord('q'):
        sys.exit(0)
    return new_images


def get_wheelchair(img, annotation_object):
    left = annotation_object['bndbox']['xmin']
    right = annotation_object['bndbox']['xmax']
    top = annotation_object['bndbox']['ymin']
    bottom = annotation_object['bndbox']['ymax']
    return img[top:bottom, left:right]


def augment_wheelchair():
    pass


def flip_wheelchair(img):
    return cv2.flip(img, 1)


def rotate_wheelchair(img):
    new_imgs = []
    rows, cols, _ = img.shape
    for theta in range(-45,45,15):
        M = cv2.getRotationMatrix2D((cols/2, rows/2), theta, 1)
        new_imgs += [cv2.warpAffine(img, M, (cols, rows))]
    return new_imgs


def remove_white_background(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    ## (2) Morph-op to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

    ## (3) Find the max-area contour
    cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnt = sorted(cnts, key=cv2.contourArea)[-1]

    ## (4) Crop and save it
    x, y, w, h = cv2.boundingRect(cnt)
    dst = img[y:y + h, x:x + w]
    return dst


def set_backgrounds():
    pass


if __name__ == '__main__':
    print('GENERATING DATASET')
    anntns_folder = '/mnt/sda/Datasets/wheelchair/annotations'
    new_dir = '/mnt/sda/Datasets/wheelchair_generated'
    classification = 'wheelchair'
    generate_dataset(anntns_folder, new_dir, classification)
