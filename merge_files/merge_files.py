"""File Merger CLI Tool"""
import argparse
import os


def main(input_dir: str, output_dir: str, multiprocessing: bool, n_of_process: int,
         chunk_file: int, chunk_line: int) -> None:
    pass


def cli_main():
    """Command line interface"""
    parser = argparse.ArgumentParser(
        description=(
            "A tool that merges all input files into a single sorted output file"
        )
    )
    parser.add_argument(
        "-i", "--input-dir", type=str, default=os.getcwd(),
        help=("A directory of files to be merged."
              "DEFAULT <current-directory>")
    )
    parser.add_argument(
        "-o", "--output-dir", type=str, default=os.getcwd(),
        help=("A directory where the merged file will be saved."
              "DEFAULT <current-directory>")
    )
    parser.add_argument(
        "-m", "--multiprocessing", action="store_true",
        help=("Use multiprocessing for merging operations"
              "DEFAULT False")
    )
    parser.add_argument(
        "-p", "--n_of_process", type=int, default=4,
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
        multiprocessing=args.multiprocessing,
        n_of_process=args.n_of_process,
        chunk_file=args.chunk_file,
        chunk_line=args.chunk_line,
    )
