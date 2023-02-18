import asyncio
import multiprocessing
import shutil
from typing import List

from .base import FileMerger


class ParallelFileMerger(FileMerger):

    def __init__(self, input_dir: str, output_dir: str, filename: str = "output.txt", file_chunk_size: int = 1024, line_chunk_size: int = 1024, num_processes: int = 4) -> None:
        super().__init__(input_dir, output_dir, filename, file_chunk_size, line_chunk_size)
        self.num_processes = num_processes

    async def _merge_chunks_async(self, chunk: List[str], output_file: str) -> None:
        """
        Merges a subset of input files into an intermediate file using an async process.

        Args:
            chunk (list): List of input file paths.
            output_file (str): Path and filename of intermediate output file.
        """
        await self._create_intermediate(chunk, output_file)

    def _merge_chunks(self, chunk: List[str], output_file: str):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._merge_chunks_async(chunk, output_file))
        loop.close()

    def merge_files(self) -> None:
        """
        Merges all input files into a single sorted output file using multiprocessing.
        """
        chunks = self._divide_files_into_chunks()

        try:
            with multiprocessing.Pool(self.num_processes) as pool:
                results = []
                for i, chunk in enumerate(chunks):
                    output_file_chunk = f"{self.temp_file}.{i}"
                    result = pool.apply_async(self._merge_chunks, args=(
                        chunk, output_file_chunk))
                    results.append(result)

                for result in results:
                    result.get()

            self._merge_intermediate_files(len(chunks), self.temp_file)
        finally:
            shutil.rmtree(self.temp_dir)
