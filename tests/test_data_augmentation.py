import unittest
import unittest
from src.data_augmentation import *
from src.folder_preparation import *
import shutil
import random


class TestDataAugmentation(unittest.TestCase):
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

        resize_and_move_images_to_train_val_folders(target_dir=self.data_dir, dest_dir=self.new_data_dir,
                                                    split_ratio=0.1)

    def test_stitch_two_images(self):
        dir_1 = self.new_data_dir / Path('train/1')
        dir_2 = self.new_data_dir / Path('train/2')
        image_1 = Image.open(dir_1 / Path(random.choice(os.listdir(dir_1))))
        image_2 = Image.open(dir_2 / Path(random.choice(os.listdir(dir_2))))

        image_1_2 = stitch_two_images(image1=image_1, image2=image_2)
        h1, w1, c1 = asarray(image_1).shape
        h12, w12, c12 = asarray(image_1_2).shape
        self.assertEquals((2 * h1, w1, c1), (h12, w12, c12))

    def test_stitch_all_images_in_two_folders(self):
        dir_1 = self.new_data_dir / Path('train/1')
        dir_2 = self.new_data_dir / Path('train/2')
        dir_target = self.new_data_dir / Path('train/3')
        all_target_ims_orig = clean_list(os.listdir(dir_target))
        stitch_all_images_in_two_folders(dir_1=dir_1, dir_2=dir_2, dir_target=dir_target)
        all_target_imgs = clean_list(os.listdir(dir_target))
        dir1_imgs = clean_list(os.listdir(dir_1))
        dir2_imgs = clean_list(os.listdir(dir_2))
        self.assertEqual(len(all_target_imgs), len(dir1_imgs) * len(dir2_imgs) + len(all_target_ims_orig))
        shutil.rmtree(self.new_data_dir)

    def test_stitch_all_classes_in_root_directory(self):
        stitch_all_classes_in_root_directory(root_dir=self.new_data_dir / Path('train'))
        dir_1 = self.new_data_dir / Path('train/1')
        dir_2 = self.new_data_dir / Path('train/2')
        dir1_imgs = clean_list(os.listdir(dir_1))
        dir2_imgs = clean_list(os.listdir(dir_2))
        self.assertEqual(len(dir2_imgs), len(dir1_imgs) * len(dir1_imgs) + len(dir1_imgs))
        shutil.rmtree(self.new_data_dir)

    def test_auto_augment_classes_in_root_directory(self):
        stitch_all_classes_in_root_directory(root_dir=self.new_data_dir / Path('train'))
        auto_augment_classes_in_root_directory(root_dir=self.new_data_dir / Path('train'))
        shutil.rmtree(self.new_data_dir)
        pass

    def test_dataframe_root_directory(self):
        stitch_all_classes_in_root_directory(root_dir=self.new_data_dir / Path('train'))
        auto_augment_classes_in_root_directory(root_dir=self.new_data_dir / Path('train'))
        df_class = dataframe_root_directory(root_dir=self.new_data_dir / Path('train'))
        pass

    def tearDown(self) -> None:
        shutil.rmtree(self.data_dir)
