import os
import heapq
import itertools
import tempfile
from typing import List


class FileMerger:
    """
    Class for merging multiple text files into a single, sorted output file.

    Args:
        input_dir (str): Directory containing input files.
        output_dir (str): Path of output file.
        filename (str, optional): Name of output file. Defaults to output.txt
        file_chunk_size (int, optional): Number of files to process at once. Defaults to 1024.
        line_chunk_size (int, optional): Number of lines to process at once. Defaults to 1024.
        use_parallel (bool, optional): Use multiprocessing for merging operations. Defaults to False.
        num_processes (int, optional): Number of processes to use. Defaults to 4.
    """

    def __init__(self, input_dir: str, output_dir: str, filename: str = "output.txt", file_chunk_size: int = 1024, line_chunk_size: int = 1024) -> None:
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.filename = filename
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, self.filename)
        self.output_file = os.path.join(self.output_dir, self.filename)
        self.chunk_size_file = file_chunk_size
        self.chunk_size_line = line_chunk_size
        self.input_files = [os.path.join(self.input_dir, f) for f in os.listdir(
            self.input_dir) if os.path.isfile(os.path.join(self.input_dir, f))]

    def _divide_files_into_chunks(self) -> List[List[str]]:
        """
        Divides input files into chunks for processing.

        Returns:
            list: List of lists, where each inner list contains a subset of input files.
        """
        return [self.input_files[i:i+self.chunk_size_file]
                for i in range(0, len(self.input_files), self.chunk_size_file)]

    async def _create_intermediate(self, input_files: List[str], output_file: str) -> None:
        """
        Asynchronously merges a subset of input files into a sorted intermediate file.

        Args:
            input_files (list): List of input file paths.
            output_file (str): Path and filename of intermediate output file.
        """
        # Open all input files and create iterators for their contents
        input_handles = [open(file) for file in input_files]
        input_iters = [iter(handle) for handle in input_handles]

        with open(output_file, "w") as output_handle:

            # Merge sorted lists of words from input files in chunks
            while True:
                # Get next chunk of words from input files
                chunks = [list(itertools.islice(iter, self.chunk_size_line))
                          for iter in input_iters]

                # Check if all chunks are empty
                if all(not chunk for chunk in chunks):
                    break

                # Merge sorted chunks of words
                sorted_chunk = sorted(heapq.merge(*chunks),
                                      key=lambda x: x.strip())

                # Write merged chunk of words to output file
                for word in sorted_chunk:
                    output_handle.write(word)

        for handle in input_handles:
            handle.close()

    def _merge_intermediate_files(self, number_of_intermediate: int, temp_file: str) -> None:
        """
        Merges the intermediate files into the final output file.

        Args:
            num_files (int): Number of intermediate files to merge.
            temp_file (str): A temp file in the path of temporary directory containing intermediate files.
        """
        written_words = set()

        with open(self.output_file, "w") as output_handle:
            input_handles = [open(f"{temp_file}.{i}", "r")
                             for i in range(number_of_intermediate)]
            input_iters = [iter(handle) for handle in input_handles]
            sorted_lines = sorted(heapq.merge(
                *input_iters, key=lambda x: x.strip()))
            for word in sorted_lines:
                word = word.strip()
                if word not in written_words:
                    output_handle.write(word + "\n")
                    written_words.add(word)

            for handle in input_handles:
                handle.close()
                os.remove(handle.name)

    def merge_files(self) -> None:
        raise NotImplementedError("Subclasses should implement this method.")
