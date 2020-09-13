import os
from pathlib import Path
import tensorflow as tf
from PIL import Image
from numpy import asarray
import numpy as np
import random
from keras.preprocessing.image import img_to_array, ImageDataGenerator, load_img
from src.folder_preparation import clean_list
from tqdm import tqdm
import pandas as pd


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
                img_1_2.save(dir_target / Path(
                    'stitched_' + os.path.splitext(img_1)[0] + '__' + os.path.splitext(img_2)[0] + '.png'))


def stitch_all_classes_in_root_directory(root_dir):
    """
    :param root_dir: Path directory which contains all classes
    :return: 
    """

    # reminder that class names need to be numbers for this function to work
    sub_dirs = clean_list(os.listdir(root_dir))

    for sub_dir1 in sub_dirs:
        path_sub_dir1 = root_dir / Path(sub_dir1)
        for sub_dir2 in sub_dirs:
            print('sub_dir1: ', sub_dir1)
            print('sub_dir2: ', sub_dir2)
            print('------------------------')
            path_sub_dir2 = root_dir / Path(sub_dir2)
            if int(sub_dir1) + int(sub_dir2) <= np.max(list(map(int, sub_dirs))):
                target_dir = root_dir / Path(str(int(sub_dir1) + int(sub_dir2)))
                stitch_all_images_in_two_folders(path_sub_dir1, path_sub_dir2, target_dir)


def auto_augment_classes_in_root_directory(root_dir):
    """
    conduct an automatic data augmentation of the images in a root directory to compensate
    for the class imbalance resulted from manual data augmentation
    :param root_dir: Path directory which conatains all classes
    :return:
    """
    datagen = ImageDataGenerator(
        rotation_range=40,
        shear_range=0.2,
        horizontal_flip=True,
        vertical_flip=True,
        brightness_range=[0.5, 1.5],
        fill_mode='nearest')

    all_classes = list(map(int, clean_list(os.listdir(root_dir))))
    n_class_max = len(clean_list(os.listdir(root_dir / Path((str(np.max(all_classes)))))))

    for class_id in range(np.min(all_classes), np.max(all_classes)):
        print(class_id)
        img_list = clean_list(os.listdir(root_dir / Path((str(class_id)))))
        n_img_orig = len([x for x in img_list if 'stitched' not in x])
        n_img_stitched = len([x for x in img_list if 'stitched' in x])
        gen_dir = root_dir / Path((str(class_id)))
        for index in clean_list(os.listdir(gen_dir)):
            if 'stitched' not in index:
                img = load_img(gen_dir / Path(index))
                x = img_to_array(img)
                x = x.reshape((1,) + x.shape)
                i = 0
                for batch in datagen.flow(x, batch_size=1,
                                          save_to_dir=gen_dir, save_prefix='auto_' + index.split('.')[0] + '__',
                                          save_format='png'):
                    i += 1
                    if i > (n_class_max - n_img_stitched) // n_img_orig:
                        break


def dataframe_root_directory(root_dir):
    """
    return a dataframe that classifies all images in a root directory
    :param root_dir: Path to directorty that has class directories with three image types in them:
    stitched: manual images resulted from stitching together images from "smaller numbered" folders
    auto: additional images created from auto-generating images inside each class
    :return: df_class
    """
    class_dirs = clean_list(os.listdir(root_dir))
    df_class = pd.DataFrame(columns=['image_name', 'class', 'type'])
    for class_dir in class_dirs:
        print(class_dir)
        img_list = clean_list(os.listdir(root_dir / Path(class_dir)))
        for img in img_list:
            if ('stitched' not in img) and ('auto' not in img):
                img_type = 'original'
            elif 'stitched' in img:
                img_type = 'stitched'
            elif 'auto' in img:
                img_type = 'automatic'
            df_class = df_class.append({'image_name': img,'class': class_dir, 'type': img_type}, ignore_index=True)
            return df_class
