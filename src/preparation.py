import os
from pathlib import Path

def train_valid_split_directory(dir_name):
    pass

def empty_folder_duplicate(target_dir,dest_dir):
    '''
    target_dir = directory which holds image categories
    dest_dir = directory which will hold simplified images in each category
    '''
    os.mkdir(Path(dest_dir))
    class_names = list(os.listdir(Path(target_dir)))
    # we want to exclude any hidden folders
    class_names = [i for i in class_names if '.' not in i]
    for i in class_names:
        os.mkdir(Path(dest_dir)/i)

def resize_images(target_dir,dest_dir):
    target_path = Path(target_dir)
    dest_path = Path(dest_dir)
    for i in class_names:
        class_path = os.path.join(dir_path/Path(i))
        class_path_dest = os.path.join(dest_dir/Path(i))
        for j in os.listdir(class_path):
            if 'png' in j:
                image = Image.open(class_path/Path(j))
                data = asarray(image)
                [ro,col,ch] = data.shape

                if ro>col:
                    new_ro = 255
                    new_col = int(np.ceil(col/ro*255))
                else:
                    new_col=255
                    new_ro = int(np.ceil(ro/col*new_col))
                data_reshaped = tf.image.resize(
                data,size=[new_ro,new_col],method='bilinear')
                data = data_reshaped.numpy().astype('uint8')
                im = Image.fromarray(data)
                im.save(class_path_dest/Path(j))