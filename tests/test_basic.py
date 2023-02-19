import unittest
from unittest.mock import patch

from merge_files.mergers.basic import BasicFileMerger


class BasicFileMergerTestCase(unittest.TestCase):
    def setUp(self):
        self.input_files = ['file1.txt', 'file2.txt', 'file3.txt']
        self.output_file = 'merged_file.txt'

    @patch('merge_files.mergers.basic.BasicFileMerger._merge_intermediate_files')
    def test_merge_files_calls_merge_intermediate_files(self, mock_merge):
        merger = BasicFileMerger(self.input_files, self.output_file)
        merger.merge_files()
        mock_merge.assert_called_once_with(self.input_files)
