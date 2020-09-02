import unittest
from src.preparation import *
import shutil

class TestPreparation(unittest.TestCase):


    def setUp(self) -> None:
        self.data_dir = Path('temp')
        if os.path.exists(self.data_dir):
            shutil.rm(self.data_dir)
        #create a temporary directory to host class folders
        os.mkdir(self.data_dir)
        #we have 10 classes in this project
        for i in range(10):
            os.mkdir(Path(self.data_dir/Path(str(i+1))))

    def test_train_valid_split_directory(self):
        pass

    def tearDown(self) -> None:
        shutil.rmtree(self.data_dir)


