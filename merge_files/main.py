"""File Merger CLI Tool"""
import argparse
import os
import time
from .mergers.async_ import AsyncFileMerger
from .mergers.parallel import ParallelFileMerger
from .mergers.basic import BasicFileMerger
from .utils import (check_valid_path,
                    list_files)


def main(input_dir: str, output_dir: str, filename: str, chunk_file: int, chunk_line: int,
         use_parallel: bool, n_of_process: int,) -> None:
    """
    Merges text files from a given directory and saves the merged file to an output directory.

    Args:
        input_dir (str): Path to the directory containing input files to be merged.
        output_dir (str): Path to the directory where the output file will be saved.
        filename (str): Name of the output file.
        chunk_file (int): Maximum number of files to merge at once.
        chunk_line (int): Maximum number of lines to read at once from each file.
        use_parallel (bool): Whether to use parallel processing for the merging.
        n_of_process (int): Number of processes to use if parallel processing is enabled.

    Returns:
        None: The function does not return anything, but prints information about the operation
        to the console.
    """
    input_dir = check_valid_path(input_dir)
    input_files = list_files(input_dir)
    if chunk_file < len(input_files):
        if use_parallel:
            file_merger = ParallelFileMerger(input_files, output_dir, filename, chunk_file,
                                             chunk_line, n_of_process)
        else:
            file_merger = AsyncFileMerger(input_files, output_dir, filename, chunk_file,
                                          chunk_line)
    else:
        file_merger = BasicFileMerger(input_files, output_dir, filename, chunk_file,
                                      chunk_line)
    try:
        tic = time.monotonic()
        file_merger.merge_files()
        tac = time.monotonic()
        print("Elapsed time:", (tac-tic), "s")
    except Exception as e:
        raise Exception(f"Something went wrong: {e}")
    else:
        print("Operation is successful. The output file has been saved here:",
              os.path.join(output_dir, filename))


def cli_main() -> None:
    """Command line interface"""
    parser = argparse.ArgumentParser(
        description=(
            "A tool that merges all input files into a single sorted output file"
        )
    )
    parser.add_argument(
        "-i", "--input-dir", type=str,
        help=("A directory of files to be merged.")
    )
    parser.add_argument(
        "-o", "--output-dir", type=str, default=f"{os.getcwd()}",
        help=("A directory where the merged file will be saved. "
              "DEFAULT <current-directory>")
    )
    parser.add_argument(
        "-f", "--filename", type=str, default="output.txt",
        help=("A name of output file. "
              "DEFAULT output.txt")
    )
    parser.add_argument(
        "-p", "--parallel", action="store_true",
        help=("Use multiprocessing for merging operations. "
              "DEFAULT False")
    )
    parser.add_argument(
        "-np", "--n_of_process", type=int, default=4,
        help="Number of processes to use. DEFAULT 4")
    parser.add_argument(
        "-cf", "--chunk-file", type=int, default=1024,
        help="Number of files to process at once. DEFAULT 1024")
    parser.add_argument(
        "-cl", "--chunk-line", type=int, default=1024,
        help="Number of lines to process at once. DEFAULT 1024")
    args = parser.parse_args()
    main(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        filename=args.filename,
        use_parallel=args.parallel,
        n_of_process=args.n_of_process,
        chunk_file=args.chunk_file,
        chunk_line=args.chunk_line,
    )
