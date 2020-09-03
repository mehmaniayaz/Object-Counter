import unittest
from src.folder_preparation import *
import shutil
import random


class TestPreparation(unittest.TestCase):
    def setUp(self) -> None:
        self.data_dir = Path('temp')
        self.new_data_dir = Path('split_temp')
        if os.path.exists(self.data_dir):
            shutil.rmtree(self.data_dir)
        if os.path.exists(self.new_data_dir):
            shutil.rmtree(self.new_data_dir)
        # create a temporary directory to host class folders
        os.mkdir(self.data_dir)
        # we have 10 classes in this project
        for i in range(10):
            sub_dir_path = Path(self.data_dir / Path(str(i + 1)))
            os.mkdir(sub_dir_path)
            for img_name in range(10):
                img_array = np.random.randint(255, size=(400, 200, 3)).astype('uint8')
                img_image = Image.fromarray(img_array)
                img_image.save(sub_dir_path / Path(str(img_name) + '.png'))

    def test_empty_folder_duplicate(self):
        empty_folder_duplicate(self.data_dir, self.new_data_dir)
        self.assertEqual(len(os.listdir(self.data_dir)), len(os.listdir(self.new_data_dir)))
        shutil.rmtree(self.new_data_dir)

    def test_empty_train_valid_split_directory(self):
        empty_train_valid_split_directory(self.data_dir)
        split_path = Path('split_' + self.data_dir.name)
        self.assertEqual(len(os.listdir(self.data_dir)), len(os.listdir(split_path / Path('train'))))
        self.assertEqual(len(os.listdir(self.data_dir)), len(os.listdir(split_path / Path('validation'))))
        shutil.rmtree(self.new_data_dir)

    def test_move_images_train_validation_folders(self):
        move_images_to_train_valid_split_folders()

    def test_resize_images(self):
        empty_train_valid_split_directory(self.data_dir)
        resize_images(target_dir=self.data_dir/Path('2'), dest_dir=self.new_data_dir / Path('train/2'), target_size=255,
                      image_format='.png')
        random_img_dir = self.new_data_dir / Path('train/2')
        random_img = Image.open(random_img_dir / Path(random.choice(os.listdir(random_img_dir))))
        self.assertEqual(np.max(asarray(random_img).shape), 255)
        shutil.rmtree(self.new_data_dir)

    def test_move_resized_images_to_train_val_folders(self):
        resize_and_move_images_to_train_val_folders(target_dir=self.data_dir, dest_dir=self.new_data_dir,
                                                    split_ratio=0.1,target_size=255,image_format='.png')

    def tearDown(self) -> None:
        shutil.rmtree(self.data_dir)
