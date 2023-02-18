import os
import unittest
import asyncio
from unittest.mock import Mock, patch, call
from merge_files.mergers.parallel import ParallelFileMerger


class TestParallelFileMerger(unittest.TestCase):

    def setUp(self):
        self.input_dir = os.path.join(os.getcwd(), 'tests', 'data', 'input')
        self.filename = 'test_output.dat'
        self.output_dir = os.path.join(os.getcwd(), 'tests', 'data', 'output')
        self.output_file = os.path.join(self.output_dir, self.filename)
        self.chunk_size_file = 3
        self.chunk_size_line = 2
        self.num_processes = 2
        self.file_merger = ParallelFileMerger(self.input_dir, self.output_dir, self.filename,
                                              self.chunk_size_file, self.chunk_size_line, self.num_processes)
        self.chunks = self.file_merger.divide_files_into_chunks()

    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_merge_chunks_async(self):
        chunk = ["file1.txt", "file2.txt"]
        output_file = "output.txt"
        with patch.object(ParallelFileMerger, 'create_intermediate') as mock_create_intermediate:
            asyncio.run(self.file_merger.merge_chunks_async(
                chunk, output_file))
            mock_create_intermediate.assert_called_once_with(
                chunk, output_file)

    @patch('multiprocessing.Pool')
    def test_merge_files(self, mock_pool):
        # Create a Mock object for apply_async
        mock_apply_async = Mock()
        mock_apply_async.return_value.get.return_value = None
        mock_pool.return_value.__enter__.return_value.apply_async = mock_apply_async

        # Mock the merge_intermediate_files method
        mock_merge_intermediate_files = Mock()
        self.file_merger.merge_intermediate_files = mock_merge_intermediate_files

        # Call merge_files
        self.file_merger.merge_files()

        # Check that apply_async was called for each chunk
        expected_calls = [
            call(self.file_merger.merge_chunks_async,
                 args=(chunk, f"{self.output_file}.{i}"))
            for i, chunk in enumerate(self.chunks)
        ]

        # Assign the call count of pool.apply_async to mock_apply_async.call_count
        mock_apply_async.assert_has_calls(expected_calls)

        # Check that merge_intermediate_files was called with the correct argument
        self.file_merger.merge_intermediate_files.assert_called_once_with(
            len(self.chunks))

    @patch('multiprocessing.Pool')
    def test_merge_files_with_fewer_processes(self, mock_pool):
        # Test that merging files with fewer processes still works correctly
        # Mock the merge_intermediate_files method
        mock_merge_intermediate_files = Mock()
        self.file_merger.merge_intermediate_files = mock_merge_intermediate_files

        # set ParallelFileMerger with fewer processes
        self.file_merger.num_processes = 1
        self.file_merger.merge_files()

        # check that Pool was called with the expected number of processes
        mock_pool.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
