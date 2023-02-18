import os
import shutil
import tempfile
import tarfile
import zipfile
import unittest
from merge_files.utils import check_valid_path


class TestCheckValidPath(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        with open(os.path.join(self.test_dir, "test.txt"), 'w') as f:
            f.write('Hello, world!')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_check_valid_path_with_folder(self):
        folder_path = os.path.join(self.test_dir, "my_folder")
        os.mkdir(folder_path)
        result = check_valid_path(folder_path)
        self.assertEqual(result, folder_path)

    def test_check_valid_path_with_zip_file(self):
        zip_path = os.path.join(self.test_dir, "my_folder.zip")
        with zipfile.ZipFile(zip_path, 'w') as myzip:
            myzip.write(os.path.join(self.test_dir, "test.txt"))

        result = check_valid_path(zip_path)
        self.assertEqual(os.path.basename(result), "my_folder")
        self.assertTrue(os.path.isdir(result))

    def test_check_valid_path_with_tar_file(self):
        tar_path = os.path.join(self.test_dir, "my_folder.tar")
        with tarfile.open(tar_path, 'w') as mytar:
            mytar.add(os.path.join(self.test_dir, "test.txt"))

        result = check_valid_path(tar_path)
        self.assertEqual(os.path.basename(result), "my_folder")
        self.assertTrue(os.path.isdir(result))

    def test_check_valid_path_with_invalid_path(self):
        # create an invalid path
        invalid_path = os.path.join(self.test_dir, "my_folder.tar")
        with open(invalid_path, "w") as f:
            f.write("this is an invalid file")

        # test that an error is raised
        with self.assertRaises(ValueError):
            check_valid_path(invalid_path)
