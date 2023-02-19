# File Merger

## Instructions

A directory containing hundreds of files is given. Each file contains a sorted list of hundreds of words, one word per line.

A python command line tool that aims to find an efficient and scalable solution that combines the contents of all files into a single sorted file.
An example output:

```
./file_merger.py -i C:/Users/hboga/Documents/Mendix/small_example
```

1. word1
2. word2
......
10. word10

---

## Package Installation (optional)

If desired, the application can be installed with the following command:

```bash
pip install .
```

*Note: The installation is not necessary to run the application*.

---
## Usage

### With Installation

Once `filemerger` is installed, it can be run in one of two ways.

```filemerger --help```

### Without Installation

`filemerger` can also be run without installation. The method below can be followed:

Either modify permissions to make it executable and use a version of python3 to run it:

```bash
chmod +x file_merger.py
./file_merger.py --help
```

Or, the python command directly can run the tool.

```bash
python file_merger.py
```
---

## `filemerger` CLI

Command line tool has a help feature that shows all the operations that can be done.

```
$ python file_merger.py --help
usage: file_merger.py [-h] [-i INPUT_DIR] [-o OUTPUT_DIR] [-f FILENAME] [-p] [-np N_OF_PROCESS] [-cf CHUNK_FILE] [-cl CHUNK_LINE]

A tool that merges all input files into a single sorted output file

options:
  -h, --help            show this help message and exit
  -i INPUT_DIR, --input-dir INPUT_DIR
                        A directory of files to be merged.
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        A directory where the merged file will be saved. DEFAULT <current-directory>
  -f FILENAME, --filename FILENAME
                        A name of output file. DEFAULT output.txt
  -p, --parallel        Use multiprocessing for merging operations. DEFAULT False
  -np N_OF_PROCESS, --n_of_process N_OF_PROCESS
                        Number of processes to use. DEFAULT 4
  -cf CHUNK_FILE, --chunk-file CHUNK_FILE
                        Number of files to process at once. DEFAULT 1024
  -cl CHUNK_LINE, --chunk-line CHUNK_LINE
                        Number of lines to process at once. DEFAULT 1024
```
---

## Examples

### Merge Multiple Files in Input Folder
Consider the input files in the following structure.
```
input_dir/
    ├── file1.dat
    ├── file2.dat
    ├── file3.dat
    ├── file4.dat
    └── file5.dat
```
The folder directory where the files are located is given as Input Directory.
```
$ filemerger -i input_dir

Operation is successful. The output file has been saved here: /path/to/package/folder/output.txt
```
---
### Merge Multiple Files in Compressed File
Compressed file directory can be given as Input Directory. In this case, the files in the compressed file are extracted to the folder created in the same directory and the directory of that folder is given.
```
$ filemerger -i compressed_file_dir

Operation is successful. The output file has been saved here: /path/to/package/folder/output.txt
```

---
### Custom Output Path
Specify a custom directory.
```
$ filemerger -i input_dir -o output_dir

Operation is successful. The output file has been saved here: /path/to/custom/folder/output.txt
```
---
### Custom Output File Name

```
$ filemerger -i input_dir -o output_dir -f merged_file.txt

Operation is successful. The output file has been saved here: /path/to/custom/folder/merged_file.txt
```
---
### Use Multiprocessing
Use multiple processes during the merge process
```
$ filemerger -i input_dir -p

Operation is successful. The output file has been saved here: /path/to/package/folder/output.txt
```
---
### Use Multiprocessing with Custom Number of Processes
Use custom number of processes
```
$ filemerger -i input_dir -p -np 8

Operation is successful. The output file has been saved here: /path/to/package/folder/output.txt
```
---
### Custom File Chunk Size
Set custom number of files to process at once
```
$ filemerger -i input_dir -cf 100

Operation is successful. The output file has been saved here: /path/to/package/folder/output.txt
```
---
### Custom Line Chunk Size
Set custom number of lines to process at once
```
$ filemerger -i input_dir -cl 250

Operation is successful. The output file has been saved here: /path/to/package/folder/output.txt
```
---
### Attempting to Enter an Invalid Input Directory
If the user enters an invalid input directory, the following error will be raised.

```
$ filemerger -i invalid_dir
Traceback (most recent call last):
  File "C:\Users\hboga\AppData\Local\Programs\Python\Python310\Scripts\filemerger-script.py", line 33, in <module>
    sys.exit(load_entry_point('filemerger==1.0.0', 'console_scripts', 'filemerger')())
  File "C:\Users\hboga\AppData\Local\Programs\Python\Python310\lib\site-packages\merge_files\main.py", line 64, in cli_main
    main(
  File "C:\Users\hboga\AppData\Local\Programs\Python\Python310\lib\site-packages\merge_files\main.py", line 12, in main
    input_dir = check_valid_path(input_dir)
  File "C:\Users\hboga\AppData\Local\Programs\Python\Python310\lib\site-packages\merge_files\utils.py", line 36, in check_valid_path
    raise ValueError(f"Please enter a valid path: {path}")
ValueError: Please enter a valid path: invalid_dir
```
---
### Attempting to Not Enter a Input Directory
If the user doesn't enter any input directory, the following error will be raised.
```
$ filemerger
Traceback (most recent call last):
  File "C:\Users\hboga\AppData\Local\Programs\Python\Python310\Scripts\filemerger-script.py", line 33, in <module>
    sys.exit(load_entry_point('filemerger==1.0.0', 'console_scripts', 'filemerger')())
  File "C:\Users\hboga\AppData\Local\Programs\Python\Python310\lib\site-packages\merge_files\main.py", line 64, in cli_main
    main(
  File "C:\Users\hboga\AppData\Local\Programs\Python\Python310\lib\site-packages\merge_files\main.py", line 12, in main
    input_dir = check_valid_path(input_dir)
  File "C:\Users\hboga\AppData\Local\Programs\Python\Python310\lib\site-packages\merge_files\utils.py", line 10, in check_valid_path
    raise ValueError(
ValueError: Path cannot be None. Please enter a valid path: None
```
---

## Tests

The core functions of `filemerger` have tests.

```
$ python setup.py test
running test
running egg_info
writing filemerger.egg-info\PKG-INFO
writing dependency_links to filemerger.egg-info\dependency_links.txt
writing entry points to filemerger.egg-info\entry_points.txt
writing top-level names to filemerger.egg-info\top_level.txt
reading manifest file 'filemerger.egg-info\SOURCES.txt'
writing manifest file 'filemerger.egg-info\SOURCES.txt'
running build_ext
test_merge_files (tests.test_async.TestAsyncFileMerger)
Test that files are merged and intermediate files are merged with the expected argument ... ok
test_split_into_files (tests.test_async.TestAsyncFileMerger)
Test that files are merged asynchronously and intermediate files are created ... ok
test_create_intermediate (tests.test_base.TestFileMerger)
Test that intermediate files are correctly created and written. ... ok
test_divide_files_into_chunks (tests.test_base.TestFileMerger)
Test that files are correctly divided into chunks. ... ok
test_merge_files_raises_not_implemented_error (tests.test_base.TestFileMerger)
Test that merge_files() raises a NotImplementedError. ... ok
test_merge_intermediate_files (tests.test_base.TestFileMerger)
Test that intermediate files are merged and sorted correctly. ... ok
test_split_into_files (tests.test_parallel.TestParallelFileMerger)
Test the _split_into_files() method of ParallelFileMerger. ... ok
test_split_into_files_async (tests.test_parallel.TestParallelFileMerger)
Test the _split_into_files() method of ParallelFileMerger. ... ok
test_merge_files (tests.test_parallel.TestParallelFileMerger)
Test the merge_files() method of ParallelFileMerger with multiple processes. ... ok
test_merge_files_with_fewer_processes (tests.test_parallel.TestParallelFileMerger)
Test the merge_files method of the ParallelFileMerger class with fewer processes ... ok
test_check_valid_path_with_folder (tests.test_utils.TestCheckValidPath) ... ok
test_check_valid_path_with_invalid_path (tests.test_utils.TestCheckValidPath) ... ok
test_check_valid_path_with_tar_file (tests.test_utils.TestCheckValidPath) ... ok
test_check_valid_path_with_zip_file (tests.test_utils.TestCheckValidPath) ... ok

----------------------------------------------------------------------
Ran 14 tests in 0.101s

OK
```