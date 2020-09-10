import os
from pathlib import Path
import tensorflow as tf
from PIL import Image
from numpy import asarray
import numpy as np
import random
from keras.preprocessing.image import img_to_array
from src.folder_preparation import clean_list


def stitch_two_images(image1, image2):
    """
    Stitch two images together and return a merged image (Pillow image)
    :param image1: Pillow image1
    :param image2: Pillow image2
    :return: Pillow image_1_2
    """
    img_array1 = img_to_array(image1)
    img_array2 = img_to_array(image2)

    img_array_1_2 = np.concatenate((img_array1, img_array2), axis=0)
    img_1_2 = Image.fromarray(img_array_1_2.astype('uint8'))
    return img_1_2


def stitch_all_images_in_two_folders(dir_1, dir_2, dir_target):
    """
    Stich all images of two directories (dire_1 and dir_2) and put the results in dir_target
    :param dir_1: Path first directory to extract images from
    :param dir_2: Path second directory to extract images from
    :param dir_target: Path target directory to input stitched images into
    :return: None stiched images will appear in dir_target
    """
    imgs_1 = clean_list(os.listdir(dir_1))
    imgs_2 = clean_list(os.listdir(dir_2))

    for img_1 in imgs_1:
        for img_2 in imgs_2:
            if ('stitched' not in img_1) and ('stitched' not in img_2):
                PIL_img_1 = Image.open(dir_1 / img_1)
                PIL_img_2 = Image.open(dir_2 / img_2)
                img_1_2 = stitch_two_images(image1=PIL_img_1, image2=PIL_img_2)
                img_1_2.save(dir_target / Path('stitched_' + os.path.splitext(img_1)[0] + '__' + os.path.splitext(img_2)[0] + '.png'))


def stitch_all_classes_in_root_directory(root_dir):
    """
    :param root_dir: Path directory which contains all classes
    :return: 
    """

    # reminder that class names need to be numbers for this function to work
    sub_dirs = os.listdir(root_dir)

    for sub_dir1 in sub_dirs:
        path_sub_dir1 = root_dir / Path(sub_dir1)
        for sub_dir2 in sub_dirs:
            path_sub_dir2 = root_dir / Path(sub_dir2)
            if int(sub_dir1) + int(sub_dir2) <= np.max(list(map(int, sub_dirs))):
                target_dir = root_dir / Path(str(int(sub_dir1) + int(sub_dir2)))
                stitch_all_images_in_two_folders(path_sub_dir1, path_sub_dir2, target_dir)
