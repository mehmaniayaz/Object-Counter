import os
from pathlib import Path
import tensorflow as tf
from PIL import Image
from numpy import asarray
import numpy as np


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

    empty_folder_duplicate(dir_path,new_train_path)
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


def resize_images(target_dir, dest_dir,target_size=255,image_format='.png'):
    """
    Take images from target_dir and paste resizes of it in dest_dir
    :param target_dir: Path for target directory containing original images
    :param dest_dir: Path for destination directory where resized images will go
    :param target_size: size of the largest dimension (height or width) while maintaining
    the smaller dimension consistent with the original aspect ratio
    :param image_format: format of the original images
    :return:
    """
    for img_name in os.listdir(target_dir):
        if 'png' in img_name:
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
            im = Image.fromarray(data)
            im.save(dest_dir / Path(img_name))
