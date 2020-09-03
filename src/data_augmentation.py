import os
from pathlib import Path
import tensorflow as tf
from PIL import Image
from numpy import asarray
import numpy as np
import random
from keras.preprocessing.image import img_to_array


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
