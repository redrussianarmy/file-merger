import os
import tempfile
import unittest
import asyncio
import shutil

from merge_files.mergers.base import FileMerger
from unittest.mock import patch


class TestFileMerger(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.input_dir = os.path.join(os.getcwd(), 'tests', 'data', 'input')
        cls.output_dir = os.path.join(
            os.getcwd(), 'tests', 'data', 'output')
        cls.filename = 'test_output.dat'
        cls.output_file = os.path.join(cls.output_dir, cls.filename)
        cls.chunk_size_file = 2
        cls.chunk_size_line = 2
        cls.file_merger = FileMerger(cls.input_dir, cls.output_dir, cls.filename,
                                     cls.chunk_size_file, cls.chunk_size_line)
        cls.chunks = cls.file_merger.divide_files_into_chunks()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.output_file):
            os.remove(cls.output_file)

    def test_divide_files_into_chunks(self):
        # Test that files are correctly divided into chunks
        expected_chunks = [[os.path.join(self.input_dir, 'file1.dat'),
                            os.path.join(self.input_dir, 'file2.dat')],
                           [os.path.join(self.input_dir, 'file3.dat'),
                            os.path.join(self.input_dir, 'file4.dat')],
                           [os.path.join(self.input_dir, 'file5.dat')]]
        self.assertSequenceEqual(self.chunks, expected_chunks)

    def test_create_intermediate(self):
        # Test that intermediate files are correctly created and written
        input_files = self.chunks[0]
        expected_output = 0
        for input_file in input_files:
            with open(input_file, 'r') as file:
                data = file.read().replace('\n', ' ')
                expected_output += len(data.split())
        with tempfile.TemporaryDirectory() as tempdir:
            output_file = os.path.join(tempdir, 'test_output.dat.0')
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(
                self.file_merger.create_intermediate(input_files, output_file))
            with open(output_file, 'r') as f:
                actual_output = f.readlines()
            self.assertEqual(len(actual_output), expected_output)

    @patch.object(FileMerger, "create_intermediate")
    def test_merge_intermediate_files(self, mock_create_intermediate):
        mock_create_intermediate.return_value = None
        with tempfile.TemporaryDirectory() as tempdir:

            intermediate_files = [os.path.join(
                self.output_dir, f"{self.filename}.{i}") for i in range(2)]
            for intermediate_file in intermediate_files:
                shutil.copy(intermediate_file, tempdir)
            self.file_merger.output_file = os.path.join(
                tempdir, self.filename)
            self.file_merger.merge_intermediate_files(2)

            expected_content = [chr(i) for i in range(ord('a'), ord('l')+1)]
            # Check that intermediate files were merged and sorted
            with open(self.file_merger.output_file, "r") as f:
                lines = [line.rstrip('\n') for line in f.readlines()]
                self.assertEqual(lines, expected_content)

    def test_merge_files_raises_not_implemented_error(self):
        with self.assertRaises(NotImplementedError):
            self.file_merger.merge_files()


if __name__ == '__main__':
    unittest.main()
