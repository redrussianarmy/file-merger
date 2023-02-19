import os
import tempfile
import unittest

from merge_files.utils import list_files


class ListFilesTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_file = tempfile.NamedTemporaryFile(dir=self.temp_dir.name)
        self.dir_path = self.temp_dir.name

    def tearDown(self):
        self.temp_file.close()
        self.temp_dir.cleanup()

    def test_list_files_returns_list(self):
        files = list_files(self.dir_path)
        self.assertIsInstance(files, list)

    def test_list_files_returns_correct_files(self):
        expected_files = [self.temp_file.name]
        files = list_files(self.dir_path)
        self.assertListEqual(files, expected_files)

    def test_list_files_with_empty_dir(self):
        empty_dir = tempfile.TemporaryDirectory()
        empty_dir_path = empty_dir.name
        with self.assertRaises(ValueError):
            list_files(empty_dir_path)

    def test_list_files_with_invalid_dir(self):
        with self.assertRaises(FileNotFoundError):
            list_files('/invalid/path')

    def test_list_files_with_subdirectories(self):
        subdir_path = os.path.join(self.dir_path, 'subdir')
        os.mkdir(subdir_path)
        expected_files = [self.temp_file.name]
        files = list_files(self.dir_path)
        self.assertListEqual(files, expected_files)

    def test_list_files_excludes_subdirectories(self):
        subdir_path = os.path.join(self.dir_path, 'subdir')
        os.mkdir(subdir_path)
        expected_files = [self.temp_file.name]
        files = list_files(self.dir_path)
        self.assertListEqual(files, expected_files)

    def test_list_files_with_nonexistent_dir(self):
        nonexistent_dir = os.path.join(self.dir_path, 'nonexistent_dir')
        with self.assertRaises(FileNotFoundError):
            list_files(nonexistent_dir)

    def test_list_files_with_file_path(self):
        with self.assertRaises(FileNotFoundError):
            list_files(self.temp_file.name)

    def test_list_files_with_file(self):
        file_path = os.path.join(self.dir_path, 'file')
        with open(file_path, 'w') as f:
            f.write('test')
        with self.assertRaises(FileNotFoundError):
            list_files(file_path)
