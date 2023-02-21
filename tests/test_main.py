import unittest
import os
from unittest.mock import (patch,
                           call,
                           Mock)
from merge_files.main import merge


@patch('merge_files.main.check_valid_path')
@patch('merge_files.main.list_files')
@patch('merge_files.main.ParallelFileMerger')
@patch('merge_files.main.AsyncFileMerger')
@patch('merge_files.main.BasicFileMerger')
@patch('merge_files.main.print')
class TestMainFunction(unittest.TestCase):
    def setUp(self):
        # Set up mocks and inputs
        self.input_dir = 'input_dir'
        self.output_dir = 'output_dir'
        self.filename = 'output.txt'
        self.chunk_file = 2
        self.chunk_line = 5000
        self.use_parallel = True
        self.n_of_process = 4
        self.input_files = ['file1.txt', 'file2.txt', 'file3.txt']

    def test_parallel_file_merger_when_use_parallel_is_true(self, print_mock, basic_mock, async_mock, parallel_mock,
                                                            list_files_mock, check_valid_path_mock):

        check_valid_path_mock.return_value = self.input_dir
        list_files_mock.return_value = self.input_files
        parallel_mock.return_value = Mock()
        file_merger_mock = parallel_mock.return_value
        file_merger_mock.merge_files.return_value = None

        # Call the function being tested
        merge(self.input_dir, self.output_dir, self.filename, self.chunk_file,
              self.chunk_line, self.use_parallel, self.n_of_process)

        # Assert that the appropriate classes were called with the correct arguments
        parallel_mock.assert_called_once_with(
            self.input_files, self.output_dir, self.filename, self.chunk_file, self.chunk_line, self.n_of_process)
        async_mock.assert_not_called()
        basic_mock.assert_not_called()
        # Assert that merge_files was called once and in the correct place in the code
        expected_calls = [call('Operation is successful. The output file has been saved here:',
                               os.path.join(self.output_dir, self.filename))]
        print_mock.assert_has_calls(expected_calls, any_order=False)
        file_merger_mock.merge_files.assert_called_once()

    def test_async_file_merger_when_use_parallel_is_false(self, print_mock, basic_mock, async_mock, parallel_mock,
                                                          list_files_mock, check_valid_path_mock):
        self.use_parallel = False
        check_valid_path_mock.return_value = self.input_dir
        list_files_mock.return_value = self.input_files
        async_mock.return_value = Mock()
        file_merger_mock = async_mock.return_value
        file_merger_mock.merge_files.return_value = None

       # Call the function being tested
        merge(self.input_dir, self.output_dir, self.filename, self.chunk_file,
              self.chunk_line, self.use_parallel, self.n_of_process)

        # Assert that the appropriate classes were called with the correct arguments
        async_mock.assert_called_once_with(
            self.input_files, self.output_dir, self.filename, self.chunk_file, self.chunk_line)
        parallel_mock.assert_not_called()
        basic_mock.assert_not_called()

        # Assert that merge_files was called once and in the correct place in the code
        expected_calls = [call('Operation is successful. The output file has been saved here:',
                               os.path.join(self.output_dir, self.filename))]
        print_mock.assert_has_calls(expected_calls, any_order=False)
        file_merger_mock.merge_files.assert_called_once()

    def test_basic_file_merger_when_chunk_file_greater_than_num_files(self, print_mock, basic_mock, async_mock,
                                                                      parallel_mock, list_files_mock,
                                                                      check_valid_path_mock):
        self.use_parallel = False
        self.chunk_file = 10
        check_valid_path_mock.return_value = self.input_dir
        list_files_mock.return_value = self.input_files
        basic_mock.return_value = Mock()
        file_merger_mock = basic_mock.return_value
        file_merger_mock.merge_files.return_value = None

       # Call the function being tested
        merge(self.input_dir, self.output_dir, self.filename, self.chunk_file,
              self.chunk_line, self.use_parallel, self.n_of_process)

        # Assert that the appropriate classes were called with the correct arguments
        basic_mock.assert_called_once_with(
            self.input_files, self.output_dir, self.filename, self.chunk_file, self.chunk_line)
        parallel_mock.assert_not_called()
        async_mock.assert_not_called()

        # Assert that merge_files was called once and in the correct place in the code
        expected_calls = [call('Operation is successful. The output file has been saved here:',
                               os.path.join(self.output_dir, self.filename))]
        print_mock.assert_has_calls(expected_calls, any_order=False)
        file_merger_mock.merge_files.assert_called_once()

    def test_raise_exception(self, print_mock, basic_mock, async_mock, parallel_mock, list_files_mock,
                             check_valid_path_mock):
        self.use_parallel = False
        self.chunk_file = 10
        check_valid_path_mock.return_value = self.input_dir
        list_files_mock.return_value = self.input_files
        basic_mock.return_value = Mock()
        file_merger_mock = basic_mock.return_value
        file_merger_mock.merge_files.side_effect = Exception("Something went wrong")

       # Call the function being tested
        with self.assertRaises(Exception):
            merge(self.input_dir, self.output_dir, self.filename, self.chunk_file,
                  self.chunk_line, self.use_parallel, self.n_of_process)
