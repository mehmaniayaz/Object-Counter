import unittest
import unittest
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


    def tearDown(self) -> None:
