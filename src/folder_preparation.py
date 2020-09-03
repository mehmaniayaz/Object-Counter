import os
from pathlib import Path
import tensorflow as tf
from PIL import Image
from numpy import asarray
import numpy as np
import random


def empty_train_valid_split_directory(dir_path):
    """Create an empty duplicate of a folder with class subdirectories
    that has train and validation folders
    :param dir_path:data directory path that needs to be splitted
    :return:
    """
    new_dir_path = Path('split_' + dir_path.name)
    if os.path.exists(new_dir_path):
        raise KeyError('{} already exists!'.format(new_dir_path.name))
    os.mkdir(new_dir_path)
    new_train_path = new_dir_path / Path('train')
    new_validation_path = new_dir_path / Path('validation')
    os.mkdir(new_train_path)
    os.mkdir(new_validation_path)

    empty_folder_duplicate(dir_path, new_train_path)
    empty_folder_duplicate(dir_path, new_validation_path)


def empty_folder_duplicate(target_dir, dest_dir):
    """
    Create an empty duplicate of the target_dir with at dest_dir
    :param target_dir: Path of directory to duplicate from
    :param dest_dir: Path of directory to duplicate to
    :return:
    """
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    class_names = list(os.listdir(target_dir))
    # we want to exclude any hidden folders
    class_names = [i for i in class_names if '.' not in i]
    for i in class_names:
        os.mkdir(Path(dest_dir) / i)


def move_images_to_train_valid_split_folders():
    pass


# Since resize_images moves images from one folder to another (as part of data size
# reduction we keep it in the folder_preparation folder.
def resize_images(target_dir, dest_dir, target_size=255, image_format='.png', img_ratio=1, img_list=[]):
    """
    Take images from target_dir and paste resizes of it in dest_dir
    :param target_dir: Path for target directory containing original images
    :param dest_dir: Path for destination directory where resized images will go
    :param target_size: size of the largest dimension (height or width) while maintaining
    the smaller dimension consistent with the original aspect ratio
    :param image_format: format of the original images
    :param img_ratio: ratio of images to be moved from target_dir to dest_dir
    :return:
    """
    if not img_list:
        img_list = random.sample(os.listdir(target_dir), int(len(os.listdir(target_dir)) * img_ratio))

    for img_name in img_list:
        if image_format in img_name:
            image = Image.open(target_dir / Path(img_name))
            img_array = asarray(image)
            [ro, col, ch] = img_array.shape

            if ro > col:
                new_ro = target_size
                new_col = int(np.ceil(col / ro * target_size))
            else:
                new_col = target_size
                new_ro = int(np.ceil(ro / col * new_col))
            data_reshaped = tf.image.resize(
                img_array, size=[new_ro, new_col], method='bilinear')
            data = data_reshaped.numpy().astype('uint8')
            img_image = Image.fromarray(data)
            img_image.save(dest_dir / Path(img_name))

def clean_list(img_list):
    """
    Take an img_list and make sure no hidden files ('.') or corrupt images are passed
    :param img_list: image list that needs to be cleaned
    :return: 
    """
    img_list = [i for i in img_list if '.' is not i[0]]
    return img_list


def resize_and_move_images_to_train_val_folders(target_dir, dest_dir, split_ratio=0.1,
                                                image_format='.png',target_size=255):
    """
    resize images and then move them to a dest_dir directorty where two train and validation
    subfolders exist
    :param image_format:
    :param target_dir: directory from each data is supposed to be extracted
    :param dest_dir: directory to which data is supposed to be moved
    :param split_ratio: validation to training ratio size (for each class independently implemented)
    :return: 
    """

    empty_train_valid_split_directory(target_dir)
    for sub_dir in os.listdir(target_dir):
        all_imgs = os.listdir(target_dir/sub_dir)
        train_list = random.sample(all_imgs, k=int((1-split_ratio) * len(all_imgs)))
        validation_list = [i for i in all_imgs if i not in train_list]
        train_list = clean_list(train_list)
        validation_list = clean_list(validation_list)
        resize_images(target_dir=target_dir/sub_dir,dest_dir=dest_dir/Path('train')/sub_dir,target_size=target_size,
                      image_format=image_format,img_list=train_list)
        resize_images(target_dir=target_dir/sub_dir,dest_dir=dest_dir/Path('validation')/sub_dir,target_size=target_size,
                      image_format=image_format,img_list=validation_list)

