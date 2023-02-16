"""This module enables usage such as
python -m mergefiles

This is needed for standard behaviour compliance
with packages such as pip and other builtins.
"""

from .merge_files import cli_main


if __name__ == "__main__":
    cli_main()
