import unittest
import unittest
from src.data_augmentation import *
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

    def test_stitch_two_images(self):
        image_1_2 = stitch_two_images(image1=,image2=)

    def test_stitch_all_images_in_two_folders(self):
        stitch_all_images_in_two_folders(dir_1=,dir_2=,dir_target=)

    def test_stitch_all_classes_in_root_directory(self):
        stitch_all_classes_in_root_directory(root_dir = self.new_data_dir/Path('train'))

    def tearDown(self) -> None:
        shutil.rmtree(self.data_dir)
        shutil.rmtree(self.new_data_dir)
