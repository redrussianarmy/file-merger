import os
import asyncio
import unittest
import tempfile

from merge_files.mergers.async_ import AsyncFileMerger


class TestAsyncFileMerger(unittest.TestCase):

    def setUp(self):
        self.input_dir = os.path.join(os.getcwd(), 'tests', 'data', 'input')
        self.filename = 'test_output.dat'
        self.output_dir = os.path.join(os.getcwd(), 'tests', 'data', 'output')
        self.output_file = os.path.join(self.output_dir, self.filename)
        self.chunk_size_file = 2
        self.chunk_size_line = 2
        self.file_merger = AsyncFileMerger(self.input_dir, self.output_dir, self.filename,
                                           self.chunk_size_file, self.chunk_size_line)
        self.chunks = self.file_merger.divide_files_into_chunks()

    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_merge_files_async(self):
        with tempfile.TemporaryDirectory() as tempdir:
            self.file_merger.output_file = os.path.join(tempdir, self.filename)
            number_of_intermediate = asyncio.run(
                self.file_merger.merge_files_async())
        self.assertEqual(number_of_intermediate, len(self.chunks))

    def test_merge_files(self):
        # Test that all input files are correctly merged into a single sorted output file
        with tempfile.TemporaryDirectory() as tempdir:
            self.file_merger.output_file = os.path.join(tempdir, self.filename)
            self.file_merger.merge_files()
            expected_content = [chr(i) for i in range(ord('a'), ord('o')+1)]
            with open(self.file_merger.output_file, "r") as f:
                lines = [line.rstrip('\n') for line in f.readlines()]
                self.assertEqual(lines, expected_content)

    def test_merge_files_with_existing_output(self):
        # Test that an existing output file is correctly overwritten when merging files
        with tempfile.TemporaryDirectory() as tempdir:
            self.file_merger.output_file = os.path.join(tempdir, self.filename)
            with open(self.file_merger.output_file, "w") as f:
                f.write("This is existing content.\n")
            self.file_merger.merge_files()
            expected_content = [chr(i) for i in range(ord('a'), ord('o')+1)]
            with open(self.file_merger.output_file, "r") as f:
                lines = [line.rstrip('\n') for line in f.readlines()]
                self.assertEqual(lines, expected_content)


if __name__ == '__main__':
    unittest.main()
