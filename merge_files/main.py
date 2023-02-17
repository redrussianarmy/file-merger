"""File Merger CLI Tool"""
import argparse
import os
from .mergers.async_ import AsyncFileMerger
from .mergers.parallel import ParallelFileMerger
from .utils import check_valid_path


def main(input_dir: str, output_dir: str, filename: str, chunk_file: int, chunk_line: int,
         use_parallel: bool, n_of_process: int,) -> None:

    input_dir = check_valid_path(input_dir)
    if use_parallel:
        file_merger = ParallelFileMerger(input_dir, output_dir, filename, chunk_file,
                                         chunk_line, n_of_process)
    else:
        file_merger = AsyncFileMerger(input_dir, output_dir, filename, chunk_file,
                                      chunk_line)
    file_merger.merge_files()


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
