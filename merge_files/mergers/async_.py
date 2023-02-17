import asyncio

from .base import FileMerger


class AsyncFileMerger(FileMerger):
    async def merge_files_async(self) -> int:
        """
        Creates intermediate files using asyncio.

        Returns:
        - An integer representing the number of tasks created.
        """
        tasks = []
        for i in range(0, len(self.input_files), self.chunk_size_file):
            chunk = self.input_files[i:i+self.chunk_size_file]
            output_file_chunk = f"{self.output_file}.{i//self.chunk_size_file}"
            task = asyncio.create_task(self.create_intermediate(
                chunk, output_file_chunk))
            tasks.append(task)
        await asyncio.gather(*tasks)

        return len(tasks)

    def merge_files(self) -> None:
        """
        Merges all input files into a single sorted output file using asyncio.
        """
        number_of_intermediate = asyncio.run(self.merge_files_async())

        self.merge_intermediate_files(number_of_intermediate)