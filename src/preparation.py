import os
from pathlib import Path


def train_valid_split_directory(dir_path):
    """Split a folder containing classes and split an empty duplicate
    with train and validation empty subfolder
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
    for sub_dir in os.listdir(dir_path):
        os.mkdir(new_train_path / Path(sub_dir))
        os.mkdir(new_validation_path / Path(sub_dir))


def empty_folder_duplicate(target_dir, dest_dir):
    '''
    target_dir = directory which holds image categories
    dest_dir = directory which will hold simplified images in each category
    '''
    os.mkdir(Path(dest_dir))
    class_names = list(os.listdir(Path(target_dir)))
    # we want to exclude any hidden folders
    class_names = [i for i in class_names if '.' not in i]
    for i in class_names:
        os.mkdir(Path(dest_dir) / i)


def resize_images(target_dir, dest_dir):
    target_path = Path(target_dir)
    dest_path = Path(dest_dir)
    for i in class_names:
        class_path = os.path.join(dir_path / Path(i))
        class_path_dest = os.path.join(dest_dir / Path(i))
        for j in os.listdir(class_path):
            if 'png' in j:
                image = Image.open(class_path / Path(j))
                data = asarray(image)
                [ro, col, ch] = data.shape

                if ro > col:
                    new_ro = 255
                    new_col = int(np.ceil(col / ro * 255))
                else:
                    new_col = 255
                    new_ro = int(np.ceil(ro / col * new_col))
                data_reshaped = tf.image.resize(
                    data, size=[new_ro, new_col], method='bilinear')
                data = data_reshaped.numpy().astype('uint8')
                im = Image.fromarray(data)
                im.save(class_path_dest / Path(j))
