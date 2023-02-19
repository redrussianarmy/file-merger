import os
import asyncio
import glob
import unittest
from unittest.mock import (AsyncMock,
                           patch)
from merge_files.mergers.async_ import AsyncFileMerger


class TestAsyncFileMerger(unittest.TestCase):
    """
    A test suite for the AsyncFileMerger class
    """

    def setUp(self):
        """
        Set up the test case by initializing test data and creating a file merger instance
        """
        self.input_dir = os.path.join(os.getcwd(), 'tests', 'data', 'input')
        self.filename = 'test_output.dat'
        self.output_dir = os.path.join(os.getcwd(), 'tests', 'data', 'output')
        self.output_file = os.path.join(self.output_dir, self.filename)
        self.chunk_size_file = 3
        self.chunk_size_line = 2
        self.file_merger = AsyncFileMerger(self.input_dir, self.output_dir, self.filename,
                                           self.chunk_size_file, self.chunk_size_line)
        self.chunks = self.file_merger._divide_files_into_chunks()

    def tearDown(self):
        """
        Clean up the test case by deleting the output file if it exists
        """
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    @patch.object(AsyncFileMerger, '_create_intermediate')
    def test_split_into_files(self, mock_create_intermediate):
        """
        Test that files are merged asynchronously and intermediate files are created
        """
        # Mock the coroutine so that it immediately returns
        mock_create_intermediate.coro.return_value = None

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Call merge_files_async
        _ = loop.run_until_complete(self.file_merger._split_into_files())

        file_extension = "*.dat"  # or "*.*" for all files

        # Combine the directory path with the file extension using glob
        files = glob.glob(os.path.join(self.input_dir, file_extension))

        # Count the number of files
        num_files = len(files)
        # Check that create_intermediate was called the expected number of times
        expected_num_calls = (num_files + self.chunk_size_file - 1) // self.chunk_size_file
        self.assertEqual(mock_create_intermediate.call_count, expected_num_calls)

        # Check that create_intermediate was called with the expected arguments
        calls = [call[0] for call in mock_create_intermediate.call_args_list]
        simplified_calls = [([os.path.basename(f) for f in file_list], os.path.basename(
            output_file)) for (file_list, output_file) in calls]
        expected_calls = [
            (['file1.dat', 'file2.dat', 'file3.dat'], 'test_output.dat.0'),
            (['file4.dat', 'file5.dat'], 'test_output.dat.1')
        ]
        self.assertCountEqual(simplified_calls, expected_calls)

    @patch.object(AsyncFileMerger, '_split_into_files', new_callable=AsyncMock)
    @patch.object(AsyncFileMerger, '_merge_intermediate_files')
    def test_merge_files_w_chunks(self, mock_merge_intermediate_files, mock_split_into_files):
        """
        Test that files are merged and intermediate files are merged with the expected argument
        """
        mock_split_into_files.return_value = []

        # Call merge_files
        self.file_merger.merge_files()

        # Assert that merge_files_async was called
        mock_split_into_files.assert_awaited_once()

        # Check that merge_intermediate_files was called with the expected argument
        mock_merge_intermediate_files.assert_called_once_with(
            [], delete=True)

    @patch.object(AsyncFileMerger, '_split_into_files', new_callable=AsyncMock)
    @patch.object(AsyncFileMerger, '_merge_intermediate_files')
    def test_merge_files_wout_chunks(self, mock_merge_intermediate_files, mock_split_into_files):
        """
        Test that files are merged and intermediate files are merged with the expected argument
        """
        mock_split_into_files.return_value = []

        self.file_merger.chunk_size_file = len(self.file_merger.input_files) + 1
        # Call merge_files
        self.file_merger.merge_files()

        # Assert that merge_files_async was called
        mock_split_into_files.assert_not_awaited()

        # Check that merge_intermediate_files was called with the expected argument
        mock_merge_intermediate_files.assert_called_once_with(
            self.file_merger.input_files)


if __name__ == '__main__':
    unittest.main()
