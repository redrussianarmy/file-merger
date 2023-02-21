from merge_files.mergers.base import FileMerger


class BasicFileMerger(FileMerger):
    def merge_files(self) -> None:
        """
        Merges all input files into a single sorted output file without splitting into chunks.
        """
        self._merge_intermediate_files(self.input_files)
