import os
import tempfile
import unittest
import asyncio
import shutil

from merge_files.mergers.base import FileMerger
from unittest.mock import patch


class TestFileMerger(unittest.TestCase):

    def setUp(self):
        self.input_dir = os.path.join(os.getcwd(), 'tests', 'data', 'input')
        self.output_dir = os.path.join(
            os.getcwd(), 'tests', 'data', 'output')
        self.filename = 'test_output.dat'
        self.output_file = os.path.join(self.output_dir, self.filename)
        self.chunk_size_file = 2
        self.chunk_size_line = 2
        self.file_merger = FileMerger(self.input_dir, self.output_dir, self.filename,
                                      self.chunk_size_file, self.chunk_size_line)
        self.chunks = self.file_merger.divide_files_into_chunks()

    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

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

    def test_merge_intermediate_files(self):
        with tempfile.TemporaryDirectory() as tempdir:
            with patch.object(self.file_merger, "create_intermediate") as mock_create_intermediate:
                mock_create_intermediate.return_value = None

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
