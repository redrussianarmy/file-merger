# File Merger

## How does it work?
A command-line tool was developed for merging multiple sorted text files into a single, sorted output file. The tool supports three different strategies for merging files, depending on the size of the input files and the desired performance characteristics:

**Basic strategy**: This strategy reads all input files into memory, merges the contents, and writes them to the output file. It is suitable for small inputs and performs all operations sequentially.

**Async strategy**: This strategy splits the input files into chunks and processes each chunk in a separate coroutine using asyncio. This allows for concurrent execution of the file processing, but does not use multiple threads. The sorted results from each chunk are then written to intermediate files that are merged at the end. This approach can be more efficient than the basic strategy for larger inputs, and can help reduce memory usage compared to the parallel strategy.

**Parallel strategy**: The parallel strategy uses multiprocessing to process each input file in a separate process. In this strategy, each input file is divided into chunks, and each chunk is processed by a separate subprocess in parallel. The results of the subprocesses are then combined at the end to create the final output file. The parallel strategy is suitable for very large inputs where the basic and async strategies may not be efficient due to the limitations of single-threaded or single-process approaches. By using parallel processing, this strategy can distribute the workload across multiple CPU cores, which can greatly improve the overall performance. The parallel strategy provides the best performance for very large inputs, while the async strategy offers a good compromise between performance and memory usage.

### Merge Algorithm

`heapq.merge` is a Python function that takes multiple sorted input iterables and merges them into a single sorted iterable. It works by creating a heap of the first item from each iterable, and repeatedly popping the smallest item from the heap and adding it to the output. When an iterable is exhausted, its next item is automatically pulled from the next iterable in the list. This process continues until all input iterables have been exhausted and the entire output is produced. The algorithm used by heapq.merge is a variation of the merge step in merge sort. It has a time complexity of O(n log k), where n is the total number of items in all input iterables and k is the number of input iterables. It does not hold all items in memory at once. It uses a heap data structure to merge the items from the input iterables one at a time, only keeping a small number of items in memory at any given time. This means that heapq.merge() is memory-efficient and can handle very large iterables without running out of memory. However, heapq.merge is a blocking operation that is run synchronously and cannot be run asynchronously.

         Input Iterable 1               Input Iterable 2           Input Iterable 3
          ┌───────────┐                 ┌─────────┐                ┌───────────┐
          │     A     │                 │   C     │                │     F     │
          ├───────────┤                 ├─────────┤                ├───────────┤
          │     B     │                 │   D     │                │     H     │
          ├───────────┤                 ├─────────┤                ├───────────┤
          │     E     │                 │   G     │                │     J     │
          └───────────┘                 └─────────┘                └───────────┘

                                       heapq.merge()
                                            │
                                            ▼
                                   ┌─────────────────┐
                                   │ Output Iterable │
                                   └─────────────────┘
                                            │
                                            ▼
          Output Iterable:    A     B     C     D     E     F     G     H     J

In general, the solution should be efficient and scalable for most use cases. The basic strategy is suitable for small inputs, while the async and parallel strategies provide improved performance for larger inputs. The parallel strategy provides the best performance, but requires more memory and may not be suitable for extremely large inputs. The async strategy provides a good compromise between performance and memory usage, and should be suitable for most inputs. However, the performance of each strategy will depend on the specifics of the input data, so it is always a good idea to test different strategies with different inputs to find the best approach for a given situation.

### Performance Comparison

| Input File Size | Number of Files | Basic         | Async  | Parallel |
| --------------- | --------------- | ------------- | ------ | -------- |
| 16 KB           | 5               | 0.02s         | 0.02s  | 0.26s    |
| 1.27 MB         | 500             | 1.72s         | 0.21s  | 0.44s    |
| 11.4 MB         | 4000            | 1.02s         | 1.38s  | 0.95s    |
| 39 MB           | 10000           | Out of memory | 8.5s   | 4.71s    |
| 195 MB          | 50000           | Out of memory | 46.30s | 27.39s   |

*Default parameters are used in performance measurements. File and Line chunk sizes are 1024, number of processes is 4.*

---
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
test_merge_files_w_chunks (tests.test_async.TestAsyncFileMerger)
Test that files are merged and intermediate files are merged with the expected argument ... ok
test_split_into_files (tests.test_async.TestAsyncFileMerger)
Test that files are merged asynchronously and intermediate files are created ... ok
test_create_intermediate (tests.test_base.TestFileMerger)
Test that intermediate files are correctly created and written. ... Created intermediate file in C:\Users\hboga\AppData\Local\Temp\tmpns033uvw\test_output.dat.0
ok
test_divide_files_into_chunks (tests.test_base.TestFileMerger)
Test that files are correctly divided into chunks. ... ok
test_merge_files_raises_not_implemented_error (tests.test_base.TestFileMerger)
Test that merge_files() raises a NotImplementedError. ... ok
test_merge_intermediate_files (tests.test_base.TestFileMerger)
Test that intermediate files are merged and sorted correctly. ... Started to merge intermediate files
ok
test_merge_files_calls_merge_intermediate_files (tests.test_basic.BasicFileMergerTestCase) ... ok
test_list_files_excludes_subdirectories (tests.test_list_files.ListFilesTestCase) ... ok
test_list_files_returns_correct_files (tests.test_list_files.ListFilesTestCase) ... ok
test_list_files_returns_list (tests.test_list_files.ListFilesTestCase) ... ok
test_list_files_with_empty_dir (tests.test_list_files.ListFilesTestCase) ... C:\Users\hboga\AppData\Local\Programs\Python\Python310\lib\tempfile.py:837: ResourceWarning: Implicitly cleaning up <TemporaryDirectory 'C:\\Users\\hboga\\AppData\\Local\\Temp\\tmp_axpcvx6'>
  _warnings.warn(warn_message, ResourceWarning)
ok
test_list_files_with_file (tests.test_list_files.ListFilesTestCase) ... ok
test_list_files_with_file_path (tests.test_list_files.ListFilesTestCase) ... ok
test_list_files_with_invalid_dir (tests.test_list_files.ListFilesTestCase) ... ok
test_list_files_with_nonexistent_dir (tests.test_list_files.ListFilesTestCase) ... ok
test_list_files_with_subdirectories (tests.test_list_files.ListFilesTestCase) ... ok
test_async_file_merger_when_use_parallel_is_false (tests.test_main.TestMainFunction) ... ok
test_basic_file_merger_when_chunk_file_greater_than_num_files (tests.test_main.TestMainFunction) ... ok
test_parallel_file_merger_when_use_parallel_is_true (tests.test_main.TestMainFunction) ... ok
test_raise_exception (tests.test_main.TestMainFunction) ... ok
test_merge_files_w_chunks (tests.test_parallel.TestParallelFileMerger)
Test the merge_files() method of ParallelFileMerger with multiple processes. ... C:\Users\hboga\AppData\Local\Programs\Python\Python310\lib\asyncio\base_events.py:680: ResourceWarning: unclosed event loop <ProactorEventLoop running=False closed=False debug=False>
  _warn(f"unclosed event loop {self!r}", ResourceWarning, source=self)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_merge_files_with_fewer_processes (tests.test_parallel.TestParallelFileMerger)
test_split_into_files_async (tests.test_parallel.TestParallelFileMerger)
Test the _split_into_files_async() method of ParallelFileMerger. ... ok
test_check_valid_path_with_folder (tests.test_valid_path.TestCheckValidPath) ... ok
test_check_valid_path_with_invalid_path (tests.test_valid_path.TestCheckValidPath) ... ok
test_check_valid_path_with_tar_file (tests.test_valid_path.TestCheckValidPath) ... ok
test_check_valid_path_with_zip_file (tests.test_valid_path.TestCheckValidPath) ... ok

----------------------------------------------------------------------
Ran 28 tests in 0.143s

OK
```

---

## Improvements for the Future

1. **Compression:** The ability to compress input files and decompress the merged output file can greatly reduce storage and transfer costs for large files.
2. **Advanced merging algorithms:** The current implementation of the merging algorithm in the tool is a simple algorithm that uses heapq.merge(). Investigating and implementing more advanced merging algorithms can help to further improve the performance of the tool for certain use cases.
3. **User-friendly CLI:** The current command-line interface (CLI) is suitable for experienced users, but it can be improved for ease of use by novice users. Adding more descriptive error messages, help texts, and examples could make the tool more accessible to a wider range of users.
4. **Progress monitoring:** Providing a progress bar or other status updates during processing can help users to better understand the progress of the tool and make it more user-friendly.
5. **Integration with other tools:** Integrating the tool with other tools, such as a file transfer or backup tool, can provide a more complete solution for users.
6. **Performance profiling and optimization:** Conducting performance profiling and optimization on the codebase can help identify and fix bottlenecks, and further improve the performance of the tool.