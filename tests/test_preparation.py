import unittest
from unittest.mock import patch
from src.preparation import *
import shutil


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
            os.mkdir(Path(self.data_dir / Path(str(i + 1))))

    def test_train_valid_split_directory(self):
        train_valid_split_directory(self.data_dir)
        split_path = Path('split_' + self.data_dir.name)
        self.assertEqual(len(os.listdir(self.data_dir)), len(os.listdir(split_path/Path('train'))))
        self.assertEqual(len(os.listdir(self.data_dir)), len(os.listdir(split_path / Path('validation'))))

    def tearDown(self) -> None:
        shutil.rmtree(self.data_dir)
        shutil.rmtree(self.new_data_dir)
