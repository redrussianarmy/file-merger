import asyncio
import shutil

from merge_files.mergers.base import FileMerger


class AsyncFileMerger(FileMerger):
    async def _split_into_files(self) -> int:
        """
        Creates intermediate files using asyncio.

        Returns:
        - list of chunks
        """
        tasks = []
        output_chunks = []
        for i in range(0, len(self.input_files), self.chunk_size_file):
            chunk = self.input_files[i:i+self.chunk_size_file]
            output_file_chunk = f"{self.temp_file}.{i//self.chunk_size_file}"
            output_chunks.append(output_file_chunk)
            task = asyncio.create_task(self._create_intermediate(chunk, output_file_chunk))
            tasks.append(task)
        await asyncio.gather(*tasks)

        return output_chunks

    def merge_files(self) -> None:
        """
        Merges all input files into a single sorted output file using asyncio.
        """
        try:
            chunks = asyncio.run(self._split_into_files())
            self._merge_intermediate_files(chunks, delete=True)
        finally:
            shutil.rmtree(self.temp_dir)
